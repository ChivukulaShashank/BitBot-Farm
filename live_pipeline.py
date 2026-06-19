import sys
from core.inference_swarm.engine import BitSwarmInferenceEngine

def execute_live_clinical_demo():
    print("================================================================")
    # The Terminal UI reference initialization
    print("🔬 C.A.D.A LIVE DETERMINISTIC INFERENCE TESTING FRAMEWORK") 
    print("================================================================\n")

    # 1. Initialize Engine and run automatic SHA-256 validation checks
    try:
        swarm_engine = BitSwarmInferenceEngine(
            manifest_path="data/logic_manifest.json",
            schema_path="assets/schemas/manifest_schema.json"
        )
    except Exception as e:
        print(f"❌ Initialization Failed: {str(e)}")
        sys.exit(1)

    # 2. Mock live patient data streams for evaluation
    mock_patient_anemic = {
        "Hemoglobin": 8.2,   # Drastically low
        "MCV": 74.5,         # Microcytic marker
        "MCH": 21.0,         # Hypochromic marker
        "MCHC": 28.2
    }

    mock_patient_healthy = {
        "Hemoglobin": 14.5,  # Robust normal
        "MCV": 88.0,         # Safe zone
        "MCH": 29.5,         # Safe zone
        "MCHC": 33.5
    }

    # 3. Process Patients through the Swarm
    print("\n[RUNNING STREAM 1: Evaluating High-Risk Clinical Vector...]")
    res_anemic = swarm_engine.execute_deterministic_swarm(mock_patient_anemic)
    print(f" -> Diagnosis Result  : {res_anemic['diagnosis_string']}")
    print(f" -> Swarm Rule Density: {res_anemic['swarm_density_pct']}% of rules activated.")
    print(f" -> Active Fired Rules: {res_anemic['rules_fired_count']} logic nodes tripped.")

    print("\n[RUNNING STREAM 2: Evaluating Normal Clinical Vector...]")
    res_healthy = swarm_engine.execute_deterministic_swarm(mock_patient_healthy)
    print(f" -> Diagnosis Result  : {res_healthy['diagnosis_string']}")
    print(f" -> Swarm Rule Density: {res_healthy['swarm_density_pct']}% of rules activated.")
    print(f" -> Active Fired Rules: {res_healthy['rules_fired_count']} logic nodes tripped.")

    print("\n================================================================")
    print("✅ LIVE INTERACTIVE INFERENCE PROCESSING SUCCESSFUL")
    print("📝 Forensic audit logs written locally to: logs/audit/trace_ledger.log")
    print("================================================================")

if __name__ == "__main__":
    execute_live_clinical_demo()