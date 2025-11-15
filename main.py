"""
Rural Healthcare Access Agent - Main Application
"""

from agents.healthcare_agents import coordinator
from utils.logger import logger, tracer, metrics


def print_separator():
    print("\n" + "=" * 80 + "\n")


def display_results(result: dict):
    print_separator()
    print("RURAL HEALTHCARE ACCESS AGENT - RESULTS")
    print_separator()
    
    print(f"Patient ID: {result['patient_id']}")
    print(f"Response Time: {result['response_time_seconds']} seconds")
    
    print("\nINTAKE SUMMARY:")
    print(result['workflow_steps']['1_intake']['summary'])
    
    print("\nURGENCY ASSESSMENT:")
    triage = result['workflow_steps']['2_triage']
    urgency_data = triage['urgency_data']
    print(f"   Level: {urgency_data['urgency_level']}/5")
    print(f"   Priority: {urgency_data['priority']}")
    print(f"   Recommendation: {urgency_data['recommendation']}")
    print(f"\n   {triage['explanation']}")
    
    print("\nNEARBY FACILITIES:")
    facilities = result['workflow_steps']['3_resources']['facilities']['facilities']
    for i, facility in enumerate(facilities, 1):
        print(f"\n   {i}. {facility['name']}")
        print(f"      Type: {facility['type']}")
        print(f"      Distance: {facility['distance_km']} km")
        print(f"      24x7: {'Yes' if facility['available_24x7'] else 'No'}")
    
    print(f"\n   Recommendation:")
    print(f"   {result['workflow_steps']['3_resources']['recommendation']}")
    
    print("\nTELEMEDICINE OPTIONS:")
    tele_result = result['workflow_steps']['4_telemedicine']
    print(f"   {tele_result['recommendation']}")
    
    print_separator()


def run_example_cases():
    print("\nEXAMPLE CASE 1: URGENT (Chest Pain)")
    result1 = coordinator.process_patient(
        patient_id="PATIENT_001",
        location="Jabalpur, Madhya Pradesh",
        symptoms="I have severe chest pain and difficulty breathing",
        age=55
    )
    display_results(result1)
    
    print("\nEXAMPLE CASE 2: MEDIUM (Fever)")
    result2 = coordinator.process_patient(
        patient_id="PATIENT_002",
        location="Jabalpur, Madhya Pradesh",
        symptoms="Fever and cough for 3 days",
        age=8
    )
    display_results(result2)


def main():
    print_separator()
    print("RURAL HEALTHCARE ACCESS AGENT")
    print("Capstone Project - Agents for Good Track")
    print_separator()
    
    print("Choose mode:")
    print("1. Run example cases")
    print("2. Interactive mode")
    
    choice = input("\nEnter choice (1/2): ").strip()
    
    if choice == "1":
        run_example_cases()
    elif choice == "2":
        print_separator()
        patient_id = input("Patient ID: ").strip()
        location = input("Location: ").strip()
        symptoms = input("Symptoms: ").strip()
        age = int(input("Age: ").strip())
        
        result = coordinator.process_patient(patient_id, location, symptoms, age)
        display_results(result)
    else:
        print("Invalid choice")
        return
    
    print("\nExporting logs...")
    tracer.export_traces()
    metrics.print_summary()
    
    print("\nDone! Check:")
    print("   - rural_healthcare_agent.log")
    print("   - agent_traces.json")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nInterrupted by user")
    except Exception as e:
        logger.error(f"Error: {e}", exc_info=True)
        print(f"\nError: {e}")
