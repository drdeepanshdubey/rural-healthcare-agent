"""
Logging and Observability
"""

import logging
import json
from datetime import datetime

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('rural_healthcare_agent.log'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger("RuralHealthcareAgent")


class AgentTracer:
    """Track agent execution traces"""
    
    def __init__(self):
        self.traces = []
    
    def log_event(self, event_type: str, agent_name: str, data: dict):
        trace = {
            "timestamp": datetime.now().isoformat(),
            "event": event_type,
            "agent": agent_name,
            "data": data
        }
        self.traces.append(trace)
        logger.info(f"{event_type}: {agent_name}")
        return trace
    
    def log_patient_query(self, patient_id: str, query: str):
        self.log_event("PATIENT_QUERY", "System", {
            "patient_id": patient_id,
            "query": query
        })
    
    def log_agent_response(self, agent_name: str, response: dict):
        self.log_event("AGENT_RESPONSE", agent_name, response)
    
    def log_tool_usage(self, agent_name: str, tool_name: str, result: dict):
        self.log_event("TOOL_USAGE", agent_name, {
            "tool": tool_name,
            "result": result
        })
    
    def export_traces(self, filename: str = "agent_traces.json"):
        with open(filename, 'w') as f:
            json.dump(self.traces, f, indent=2)
        logger.info(f"Traces exported to {filename}")
    
    def get_traces(self):
        return self.traces


class AgentMetrics:
    """Track agent performance metrics"""
    
    def __init__(self):
        self.metrics = {
            "total_patients": 0,
            "urgent_cases": 0,
            "medium_cases": 0,
            "low_cases": 0,
            "facilities_found": 0,
            "telemedicine_recommended": 0,
            "total_response_time": 0,
            "responses": []
        }
    
    def increment_patients(self):
        self.metrics["total_patients"] += 1
    
    def record_urgency(self, urgency: str):
        if urgency == "HIGH":
            self.metrics["urgent_cases"] += 1
        elif urgency == "MEDIUM":
            self.metrics["medium_cases"] += 1
        else:
            self.metrics["low_cases"] += 1
    
    def record_response_time(self, time_seconds: float):
        self.metrics["total_response_time"] += time_seconds
        self.metrics["responses"].append(time_seconds)
    
    def get_average_response_time(self):
        if not self.metrics["responses"]:
            return 0.0
        return sum(self.metrics["responses"]) / len(self.metrics["responses"])
    
    def get_metrics(self):
        metrics = self.metrics.copy()
        metrics["average_response_time"] = self.get_average_response_time()
        return metrics
    
    def print_summary(self):
        metrics = self.get_metrics()
        logger.info("=" * 50)
        logger.info("AGENT PERFORMANCE METRICS")
        logger.info("=" * 50)
        logger.info(f"Total Patients: {metrics['total_patients']}")
        logger.info(f"Urgent Cases: {metrics['urgent_cases']}")
        logger.info(f"Medium Cases: {metrics['medium_cases']}")
        logger.info(f"Low Cases: {metrics['low_cases']}")
        logger.info(f"Avg Response Time: {metrics['average_response_time']:.2f}s")
        logger.info("=" * 50)


tracer = AgentTracer()
metrics = AgentMetrics()
