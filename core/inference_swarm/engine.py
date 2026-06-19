import json
import os
from datetime import datetime
from typing import Dict, Any, List
from core.discovery_factory.axioms import AxiomaticSeed

class BitSwarmInferenceEngine:
    """
    Phase 4 Component: Inference Environment (The "Bit Swarm")
    A pure deterministic execution engine that validates manifests via 
    SHA-256 fingerprints and runs patient data through the rule board.
    """
    def __init__(self, manifest_path: str, schema_path: str = "assets/schemas/manifest_schema.json"):
        self.manifest_path = manifest_path
        self.schema_path = schema_path
        self.rules: List[Dict[str, Any]] = []
        self.seed_validator = AxiomaticSeed()
        
        # Automatically trigger cryptographic signature audit upon instantiation
        self._load_and_verify_manifest()

    def _load_and_verify_manifest(self):
        """Loads logic manifest and executes a structural/cryptographic integrity check."""
        if not os.path.exists(self.manifest_path):
            raise FileNotFoundError(f"Inference Failure: Missing Logic Manifest asset at {self.manifest_path}")

        with open(self.manifest_path, "r") as f:
            manifest_data = json.load(f)

        # Enforce strict axiomatic signature gating before unpacking payload rules
        expected_hash = manifest_data.get("hash")
        self.seed_validator.validate_manifest(manifest_data, schema_file_path=self.schema_path)
        
        self.rules = manifest_data.get("rules", [])
        print(f"🔒 Cryptographic Audit Passed. Bit Swarm successfully armed with {len(self.rules)} verified rules.")

    def execute_deterministic_swarm(self, patient_metrics: Dict[str, float]) -> Dict[str, Any]:
        """
        Runs patient parameters down the deterministic 'Pachinko' board logic.
        Guarantees identical categorical output for identical vectors with zero probability.
        """
        fired_rules = []
        
        # 1. Evaluate every active rule independently 
        for rule in self.rules:
            feature = rule["feature"]
            operator = rule["operator"]
            threshold = rule["threshold"]
            
            # Skip evaluation gracefully if the metrics structure is missing a required column
            if feature not in patient_metrics:
                continue
                
            patient_value = patient_metrics[feature]
            
            # Execute exact conditional match boundaries
            is_triggered = False
            if operator == "lt": 
                is_triggered = patient_value < threshold
            elif operator == "gt": 
                is_triggered = patient_value > threshold
            elif operator == "lte": 
                is_triggered = patient_value <= threshold
            elif operator == "gte": 
                is_triggered = patient_value >= threshold
            elif operator == "eq": 
                is_triggered = patient_value == threshold

            if is_triggered:
                fired_rules.append(rule["id"])

        # 2. Determine consensus output via strict operational majority density thresholds
        total_rules_count = len(self.rules)
        fired_count = len(fired_rules)
        
        # Firing Density Ratio calculation
        swarm_density = fired_count / total_rules_count if total_rules_count > 0 else 0.0
        
        # Deterministic boundary: if more than 35% of your specialized rule pool fires, output positive classification
        final_diagnosis_output = 1 if swarm_density >= 0.35 else 0
        diagnosis_label = "Positive (Anemia Detected)" if final_diagnosis_output == 1 else "Negative (Healthy Profile)"

        result_payload = {
            "diagnosis_code": final_diagnosis_output,
            "diagnosis_string": diagnosis_label,
            "swarm_density_pct": round(swarm_density * 100, 2),
            "rules_fired_count": fired_count,
            "fired_rule_identifiers": fired_rules
        }

        # 3. Commit transactions permanently to the immutable trace ledger
        self._write_to_trace_ledger(patient_metrics, result_payload)
        return result_payload

    def _write_to_trace_ledger(self, metrics: Dict[str, float], result: Dict[str, Any], ledger_path: str = "logs/audit/trace_ledger.log"):
        """Generates local forensic reconstruction trails for diagnostic tracking."""
        directory_prefix = os.path.dirname(ledger_path)
        if directory_prefix:
            os.makedirs(directory_prefix, exist_ok=True)

        timestamp = datetime.now().isoformat()
        log_entry = {
            "timestamp": timestamp,
            "input_clinical_vector": metrics,
            "output_consequent": result["diagnosis_code"],
            "swarm_density_pct": result["swarm_density_pct"],
            "activated_rule_ids": result["fired_rule_identifiers"]
        }

        with open(ledger_path, "a") as f:
            f.write(json.dumps(log_entry) + "\n")