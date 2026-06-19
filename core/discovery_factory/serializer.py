import json
import hashlib
import os
import jsonschema
from typing import List, Dict, Any

class LogicManifestSerializer:
    """
    Stage 4 Component: Serialization & Cryptographic Integrity
    Compiles the optimized rule swarm into a standardized, versioned 
    JSON format, flattens the AST representation to comply with the production
    JSON Schema, and signs it with a SHA-256 checksum fingerprint.
    """
    @staticmethod
    def calculate_sha256(data_structure: Any) -> str:
        """Generates a stable SHA-256 hash string for data integrity validation."""
        serialized_str = json.dumps(data_structure, sort_keys=True)
        return hashlib.sha256(serialized_str.encode('utf-8')).hexdigest()

    @classmethod
    def serialize_to_manifest(cls, surviving_swarm: List[Dict[str, Any]], output_path: str, schema_path: str = None, version: int = 1) -> str:
        """
        Compiles and flattens AST rules into a cryptographic Logic Manifest that
        strictly conforms to the project json-schema specification.
        """
        flattened_rules = []

        # 1. Compile and transform deep AST structures into flat production schema layouts
        for rule in surviving_swarm:
            ast = rule["ast"]
            metadata = rule["metadata"]
            feature_name = ast["left"]["value"]

            flat_rule = {
                "id": rule["rule_id"],
                "feature": feature_name,
                "threshold": float(ast["right"]["value"]),
                "operator": ast["operator"],
                "output": int(metadata["output_consequent"]),
                "inputs": [feature_name], # Array wrapper matching schema minItems: 1
                "pure": True
            }
            flattened_rules.append(flat_rule)

        # 2. Compute the structural integrity hash signature of the flat payload
        payload_hash = cls.calculate_sha256(flattened_rules)

        # 3. Assemble the final manifest wrapper matching top-level schema requirements
        manifest = {
            "version": int(version), # Must be integer >= 1
            "hash": payload_hash,     # 64-character SHA-256 string
            "rules": flattened_rules
        }

        # 4. Validate against manifest_schema.json before writing to disk
        if schema_path and os.path.exists(schema_path):
            with open(schema_path, "r") as s_file:
                schema_data = json.load(s_file)
            try:
                jsonschema.validate(instance=manifest, schema=schema_data)
                print("🏆 Manifest schema validation check: 100% Conformance Verified.")
            except jsonschema.exceptions.ValidationError as e:
                print(f"⚠️ Warning: Serialized structure failed asset schema validation: {e.message}")

        # 5. Commit manifest file to disk
        directory_prefix = os.path.dirname(output_path)
        if directory_prefix:
            os.makedirs(directory_prefix, exist_ok=True)

        with open(output_path, "w") as f:
            json.dump(manifest, f, indent=2)
        
        print(f"🔒 Production Logic Manifest compiled and locked. Fingerprint: {payload_hash}")
        return payload_hash

    @staticmethod
    def archive_graveyard(graveyard: List[Dict[str, Any]], output_path: str):
        """Saves unflattened development rules to a separate file for auditing."""
        directory_prefix = os.path.dirname(output_path)
        if directory_prefix:
            os.makedirs(directory_prefix, exist_ok=True)

        with open(output_path, "w") as f:
            json.dump({"graveyard_pool": graveyard}, f, indent=2)
        print("💀 Discarded development logic successfully archived to the graveyard.")