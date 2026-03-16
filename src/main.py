"""
NovaCare Main Application Entry Point
"""
import os
import sys

# Add src to the path so we can import packages
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.orchestrator.workflow import HealthcareOrchestrator

def initialize_agentic_system():
    """
    I am setting up the primary orchestrator that coordinates the different specialized agents.
    This will initialize the Bed Management Agent, the Patient Logistics Agent, and the Insurance Pre-Auth Agent.
    """
    print("Initializing NovaCare Autonomous Healthcare Logistics Network")
    print("Loading Amazon Nova 2 Lite models for fast reasoning tasks...")
    
    orchestrator = HealthcareOrchestrator()
    print(f"Orchestrator State: {orchestrator.state}")
    
    patient_data = {"id": "12345", "condition": "critical"}
    print(f"Triggering admission for patient: {patient_data['id']}")
    
    result = orchestrator.handle_patient_admission(patient_data)
    print(f"Result: {result}")
    print(f"New Orchestrator State: {orchestrator.state}")
    
    print("System initialization and mock workflow execution complete.")

if __name__ == "__main__":
    initialize_agentic_system()

