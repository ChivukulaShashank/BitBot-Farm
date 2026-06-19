import hashlib
import json
import jsonschema
from typing import Dict, Any, List

class AxiomViolationError(Exception):
    """Custom exception raised when a rule or manifest violates C.A.D.A Laws."""
    pass

class AxiomaticSeed:
    """
    Laws that govern all rules. Acts as the functional foundation for 
    the Z3 Axiomatic Firewall and rule verification structures.
    """
    def __init__(self, current_version: str = "0.1", rules_registry: List[Dict[str, Any]] = None):
        self.last_version = current_version
        self.rules_registry = rules_registry if rules_registry is not None else []
        
        # Stochastic keywords prohibited to enforce 100% determinism (SDD Section 1 & 7)
        self.FORBIDDEN_KEYS = ["random", "sample", "shuffle", "probabilistic", "seed", "dropout"]
        
        # Clinical safety guardrails for hematological features
        self.PHYSIO_BOUNDS = {
            "Hemoglobin": (2.0, 25.0),
            "MCV": (30.0, 150.0),
            "MCH": (10.0, 50.0),
            "MCHC": (15.0, 60.0)
        }
        
        # Basic Structural Meta-Schema for fallback validation
        self.schema = {
            "type": "object",
            "required": ["manifest_metadata", "rules"],
            "properties": {
                "manifest_metadata": {"type": "object"},
                "rules": {"type": "array"}
            }
        }

    def validate_manifest(self, manifest_data: Dict[str, Any], expected_hash: str) -> bool:
        """
        Runs validation during file input/output transactions to guarantee
        unaltered logic chain configurations (SDD Section 7).
        """
        # Schema conformance 
        if self.schema:
            try:
                jsonschema.validate(instance=manifest_data, schema=self.schema)
            except jsonschema.exceptions.ValidationError as e:
                raise AxiomViolationError(f"B3 Violation: Schema mismatch -> {e.message}")

        # Core payload data integrity verification
        rules_payload = manifest_data.get("rules", [])
        manifest_str = json.dumps(rules_payload, sort_keys=True)
        actual_hash = hashlib.sha256(manifest_str.encode('utf-8')).hexdigest()
        
        if actual_hash != expected_hash:
            raise AxiomViolationError(f"Hash mismatch. Expected {expected_hash}, got {actual_hash}.")

        return True

    def validate_rule(self, candidate: Dict[str, Any], new_version: str) -> bool:
        """
        DOMAIN A: Rule Structure & Output Format.
        Executes validation within the evolutionary engine loop to preserve causal integrity.
        """
        # Extract metadata and AST components safely
        metadata = candidate.get("metadata", {})
        ast = candidate.get("ast", {})
        
        if not ast or not metadata:
            raise AxiomViolationError("Violation: Missing malformed AST blocks or metadata fields.")

        # Extract nested elements from the AST node layout
        feature = ast.get("left", {}).get("value")
        threshold = ast.get("right", {}).get("value")
        operator = ast.get("operator")
        output_consequent = metadata.get("output_consequent")

        # A1: Deterministic Binary Consequent Output
        if output_consequent not in [0, 1]:
            raise AxiomViolationError("Violation: Every rule must emit exactly 0 or 1.")

        # A4: Explicit input declaration
        if not feature or not isinstance(feature, str):
            raise AxiomViolationError("Violation: Rule must explicitly declare a string feature input.")

        # A2: Single responsibility / Collision Avoidance
        # Ensured by checking that a rule does not completely duplicate an existing rule's operational logic
        for existing_rule in self.rules_registry:
            ex_ast = existing_rule.get("ast", {})
            if (ex_ast.get("left", {}).get("value") == feature and 
                ex_ast.get("operator") == operator and 
                ex_ast.get("right", {}).get("value") == threshold):
                raise AxiomViolationError("Violation: Redundant duplicate rule logic detected in active registry.")

        # A3: Strict Causal Determinism
        candidate_str = str(candidate).lower()
        if any(forbidden in candidate_str for forbidden in self.FORBIDDEN_KEYS):
            raise AxiomViolationError("Violation: Stochastic elements are strictly prohibited.")

        # A5: Pure Functions with Zero Side Effects
        if "side_effects" in candidate or metadata.get("pure") is not True:
            raise AxiomViolationError("Violation: Rules must be pure expressions with no side effects.")

        # Biological Feasibility Bounds Checking
        if feature in self.PHYSIO_BOUNDS:
            min_val, max_val = self.PHYSIO_BOUNDS[feature]
            if not (min_val <= threshold <= max_val):
                raise AxiomViolationError(f"Physiological Violation: {feature} at {threshold} is clinically impossible.")

        return True

    def quarantine(self, error: Exception, offending_item: Dict[str, Any], log_path: str = "logs/quarantine/violations.log"):
        """
        VIOLATION HANDLING: Captures and isolates anomalies safely.
        """
        import os
        directory_prefix = os.path.dirname(log_path)
        if directory_prefix:
            os.makedirs(directory_prefix, exist_ok=True)
            
        with open(log_path, "a") as f:
            f.write(f"VIOLATION: {str(error)}\n")
            f.write(f"PAYLOAD: {json.dumps(offending_item)}\n")
            f.write("-" * 50 + "\n")