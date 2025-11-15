"""
Rural Healthcare Access Agent System
"""

import os
from dotenv import load_dotenv
import google.generativeai as genai
from tools.urgency_tool import assess_urgency
from tools.search_tool import search_healthcare_facilities, search_telemedicine_services
from utils.logger import logger, tracer, metrics
from utils.session_manager import session_manager
import time

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if not GEMINI_API_KEY:
    raise ValueError("GEMINI_API_KEY not found in .env file!")

genai.configure(api_key=GEMINI_API_KEY)


class IntakeAgent:
    def __init__(self):
        self.name = "IntakeAgent"
        # Using Gemini 2.5 Flash - fast, efficient, and cost-effective
        self.model = genai.GenerativeModel('models/gemini-2.5-flash')
        logger.info(f"{self.name} initialized")
    
    def process(self, patient_data: dict) -> dict:
        logger.info(f"{self.name}: Processing patient intake")
        
        prompt = f"""
You are a healthcare intake assistant for rural Madhya Pradesh.

Patient Information:
- Location: {patient_data['location']}
- Symptoms: {patient_data['symptoms']}

Task: Extract and organize patient information.

Return a brief summary (2-3 sentences) of the chief complaint and key details.
"""
        
        response = self.model.generate_content(prompt)
        result = {
            "agent": self.name,
            "summary": response.text,
            "symptoms": patient_data['symptoms'],
            "location": patient_data['location']
        }
        
        tracer.log_agent_response(self.name, result)
        return result


class TriageAgent:
    def __init__(self):
        self.name = "TriageAgent"
        self.model = genai.GenerativeModel('models/gemini-2.5-flash')
        logger.info(f"{self.name} initialized")
    
    def process(self, intake_data: dict, patient_age: int = 30) -> dict:
        logger.info(f"{self.name}: Assessing urgency")
        
        symptoms = intake_data['symptoms']
        urgency_result = assess_urgency(symptoms, patient_age)
        
        tracer.log_tool_usage(self.name, "UrgencyAssessor", urgency_result)
        
        prompt = f"""
Symptoms: "{symptoms}"
Urgency Level: {urgency_result['urgency_level']}/5
Priority: {urgency_result['priority']}

Provide a brief explanation (2-3 sentences) about this urgency level.
"""
        
        response = self.model.generate_content(prompt)
        
        result = {
            "agent": self.name,
            "urgency_data": urgency_result,
            "explanation": response.text
        }
        
        metrics.record_urgency(urgency_result['priority'])
        tracer.log_agent_response(self.name, result)
        return result


class ResourceFinderAgent:
    def __init__(self):
        self.name = "ResourceFinderAgent"
        self.model = genai.GenerativeModel('models/gemini-2.5-flash')
        logger.info(f"{self.name} initialized")
    
    def process(self, triage_data: dict, location: str) -> dict:
        logger.info(f"{self.name}: Searching for facilities")
        
        urgency = triage_data['urgency_data']['priority']
        facilities_result = search_healthcare_facilities(location, urgency)
        
        tracer.log_tool_usage(self.name, "HealthcareFacilitySearch", facilities_result)
        
        facilities_text = "\n".join([
            f"- {f['name']} ({f['type']}, {f['distance_km']}km)"
            for f in facilities_result['facilities']
        ])
        
        prompt = f"""
Patient urgency: {urgency}
Location: {location}

Available facilities:
{facilities_text}

Provide a brief recommendation (2-3 sentences) on which facility to visit.
"""
        
        response = self.model.generate_content(prompt)
        
        result = {
            "agent": self.name,
            "facilities": facilities_result,
            "recommendation": response.text
        }
        
        metrics.metrics["facilities_found"] += len(facilities_result['facilities'])
        tracer.log_agent_response(self.name, result)
        return result


class TelemedicineAgent:
    def __init__(self):
        self.name = "TelemedicineAgent"
        self.model = genai.GenerativeModel('models/gemini-2.5-flash')
        logger.info(f"{self.name} initialized")
    
    def process(self, triage_data: dict) -> dict:
        logger.info(f"{self.name}: Searching for telemedicine")
        
        urgency = triage_data['urgency_data']['priority']
        
        if urgency == "HIGH":
            result = {
                "agent": self.name,
                "recommendation": "Emergency case - In-person visit required.",
                "services": []
            }
        else:
            telemedicine_result = search_telemedicine_services()
            tracer.log_tool_usage(self.name, "TelemedicineSearch", telemedicine_result)
            
            prompt = f"""
Patient urgency: {urgency}

Available telemedicine: eSanjeevani (Free, 24x7)

Explain how to use this service (2-3 sentences).
"""
            
            response = self.model.generate_content(prompt)
            
            result = {
                "agent": self.name,
                "services": telemedicine_result,
                "recommendation": response.text
            }
            
            metrics.metrics["telemedicine_recommended"] += 1
        
        tracer.log_agent_response(self.name, result)
        return result


class CoordinatorAgent:
    def __init__(self):
        self.name = "CoordinatorAgent"
        self.intake_agent = IntakeAgent()
        self.triage_agent = TriageAgent()
        self.resource_finder = ResourceFinderAgent()
        self.telemedicine_agent = TelemedicineAgent()
        logger.info(f"{self.name} initialized")
    
    def process_patient(self, patient_id: str, location: str, symptoms: str, age: int = 30) -> dict:
        start_time = time.time()
        
        logger.info("=" * 60)
        logger.info(f"Starting workflow for patient: {patient_id}")
        logger.info("=" * 60)
        
        tracer.log_patient_query(patient_id, symptoms)
        metrics.increment_patients()
        
        session = session_manager.get_or_create_session(patient_id, location)
        session.update_symptoms(symptoms)
        
        patient_data = {
            "patient_id": patient_id,
            "location": location,
            "symptoms": symptoms,
            "age": age
        }
        
        logger.info("\nSTEP 1: Patient Intake")
        intake_result = self.intake_agent.process(patient_data)
        
        logger.info("\nSTEP 2: Urgency Assessment")
        triage_result = self.triage_agent.process(intake_result, age)
        session.update_urgency(triage_result['urgency_data'])
        
        logger.info("\nSTEP 3: Parallel Search (Facilities + Telemedicine)")
        resource_result = self.resource_finder.process(triage_result, location)
        telemedicine_result = self.telemedicine_agent.process(triage_result)
        
        if resource_result['facilities']['facilities']:
            session.update_facility(resource_result['facilities']['facilities'][0])
        session.update_telemedicine(telemedicine_result)
        
        end_time = time.time()
        response_time = end_time - start_time
        metrics.record_response_time(response_time)
        
        session.add_consultation()
        
        final_response = {
            "patient_id": patient_id,
            "session_id": session.session_id,
            "workflow_steps": {
                "1_intake": intake_result,
                "2_triage": triage_result,
                "3_resources": resource_result,
                "4_telemedicine": telemedicine_result
            },
            "response_time_seconds": round(response_time, 2),
            "session_state": session.get_state()
        }
        
        logger.info("=" * 60)
        logger.info(f"Workflow completed in {response_time:.2f} seconds")
        logger.info("=" * 60)
        
        return final_response


coordinator = CoordinatorAgent()