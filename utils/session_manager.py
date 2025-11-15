"""
Session and Memory Management
"""

from datetime import datetime
import json


class PatientSession:
    """Manages individual patient session with memory"""
    
    def __init__(self, patient_id: str, location: str):
        self.patient_id = patient_id
        self.session_id = f"SESSION_{patient_id}_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        self.created_at = datetime.now().isoformat()
        
        self.state = {
            "patient_id": patient_id,
            "location": location,
            "current_symptoms": "",
            "urgency_level": None,
            "assigned_facility": None,
            "telemedicine_option": None,
            "consultation_status": "IN_PROGRESS"
        }
        
        self.memory = {
            "medical_history": [],
            "past_consultations": []
        }
    
    def update_symptoms(self, symptoms: str):
        self.state["current_symptoms"] = symptoms
    
    def update_urgency(self, urgency_data: dict):
        self.state["urgency_level"] = urgency_data["urgency_level"]
        self.state["urgency_priority"] = urgency_data["priority"]
    
    def update_facility(self, facility_data: dict):
        self.state["assigned_facility"] = facility_data
    
    def update_telemedicine(self, telemedicine_data: dict):
        self.state["telemedicine_option"] = telemedicine_data
    
    def add_consultation(self):
        consultation = {
            "timestamp": datetime.now().isoformat(),
            "symptoms": self.state["current_symptoms"],
            "urgency": self.state.get("urgency_level"),
            "facility": self.state.get("assigned_facility"),
            "status": "COMPLETED"
        }
        self.memory["past_consultations"].append(consultation)
        self.state["consultation_status"] = "COMPLETED"
    
    def get_state(self):
        return self.state
    
    def get_memory(self):
        return self.memory


class SessionManager:
    """Manages multiple patient sessions"""
    
    def __init__(self):
        self.sessions = {}
    
    def create_session(self, patient_id: str, location: str):
        session = PatientSession(patient_id, location)
        self.sessions[patient_id] = session
        print(f"Created session for patient: {patient_id}")
        return session
    
    def get_session(self, patient_id: str):
        return self.sessions.get(patient_id)
    
    def get_or_create_session(self, patient_id: str, location: str):
        session = self.get_session(patient_id)
        if session is None:
            session = self.create_session(patient_id, location)
        return session


session_manager = SessionManager()
