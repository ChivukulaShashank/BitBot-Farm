import json
from core.discovery_factory.axioms import AxiomaticSeed, AxiomViolationError

# 1. Load the Schema
with open("assets/schemas/manifest_schema.json", "r") as f:
    schema = json.load(f)

# 2. Initialize the Constitution
seed = AxiomaticSeed(schema=schema)

print("--- INITIALIZING C.A.D.A FIREWALL TEST ---")

# --- TEST 1: The Perfect Rule ---
valid_rule = {
    "id": "ANM-001",
    "feature": "hemoglobin",
    "threshold": 11.5,
    "operator": "lt",
    "output": 1,
    "inputs": ["hemoglobin"],
    "pure": True
}

try:
    seed.validate_rule(valid_rule, new_version=1)
    print("✅ TEST 1 PASSED: Valid rule accepted.")
    # Add to registry to test A2 (Overlap) later
    seed.rules_registry.append(valid_rule) 
except AxiomViolationError as e:
    print(f"❌ TEST 1 FAILED: {e}")

# --- TEST 2: The Lethal Mutation (A1 & A3 Violation) ---
lethal_rule = {
    "id": "ANM-002",
    "feature": "mcv",
    "threshold": 80.0,
    "operator": "gt",
    "output": 0.85,          # VIOLATION: Not binary (0 or 1)
    "inputs": ["mcv"],
    "pure": True,
    "random_seed": 42        # VIOLATION: Stochastic element
}

try:
    seed.validate_rule(lethal_rule, new_version=1)
    print("❌ TEST 2 FAILED: Firewall breached! Lethal rule was accepted.")
except AxiomViolationError as e:
    print(f"✅ TEST 2 PASSED (QUARANTINED): {e}")
    seed.quarantine(e, lethal_rule)
    print("   -> Offending rule successfully written to quarantine log.")