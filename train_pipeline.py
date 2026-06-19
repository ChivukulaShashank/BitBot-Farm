from core.discovery_factory.extractor import CSVDataExtractor
from core.discovery_factory.generator import LogicalRuleFactory
from core.inference_swarm.verifier import GenerationalGeneticVerifier
from core.discovery_factory.serializer import LogicManifestSerializer

# === PIPELINE PROFILE CONFIGURATION PANEL ===
INPUT_DATA_FILE = "data/raw_blood_tests.csv"
OUTPUT_MANIFEST_FILE = "data/logic_manifest.json"
OUTPUT_GRAVEYARD_FILE = "data/graveyard.json"
SCHEMA_ASSET_FILE = "assets/schemas/manifest_schema.json"

# Features and target variables aligned to match preprocessed data schemas
TARGET_FEATURES = ["Hemoglobin", "MCV", "MCH", "MCHC"]
TARGET_COLUMN = "Result"
TARGET_FLAG_POSITIVE = 1

POOL_SIZE = 10000
GENETIC_GENERATIONS = 5
ACCURACY_PURGE_THRESHOLD = 0.75  # Retain rules hitting 75%+ accuracy
MANIFEST_VERSION = 1             # Strict integer matching JSON schema specs
# ============================================

def run_complete_train_pipeline():
    print("================================================================")
    print("🚀 STARTING CAUSAL ANEMIA DIAGNOSING AGENT (C.A.D.A) PIPELINE")
    print("================================================================\n")

    # ------------------------------------------------------------------
    # STAGE 1: Data Extraction and Matrix Sanitization
    # ------------------------------------------------------------------
    print("[STAGE 1] Running Data Matrix Extractor...")
    extractor = CSVDataExtractor(INPUT_DATA_FILE)
    clean_df = extractor.extract_clean_dataframe(
        chosen_features=TARGET_FEATURES,
        target_col=TARGET_COLUMN
    )
    print(f"✅ Data Extraction Complete. Matrix Shape: {clean_df.shape}\n")

    # ------------------------------------------------------------------
    # STAGE 2: Logical Boundaries Inference & Unique Population Spawning
    # ------------------------------------------------------------------
    print("[STAGE 2] Running Statistical Logic Boundary Inference Engine...")
    boundaries = LogicalRuleFactory.infer_data_boundaries(
        df=clean_df,
        features=TARGET_FEATURES,
        target_col=TARGET_COLUMN,
        target_val=TARGET_FLAG_POSITIVE
    )
    
    print(" -> Inferred Exploration Ranges:")
    for feat, limits in boundaries.items():
        print(f"    * {feat}: Direction=[{limits['default_operator']}], Range=[{limits['search_min']} - {limits['search_max']}]")
        
    print(f"\n Spawning collision-free collection of {POOL_SIZE} structural AST candidate rules...")
    raw_rule_pool = LogicalRuleFactory.generate_ast_population(boundaries, pool_size=POOL_SIZE)
    print("✅ Seed rule array successfully constructed in volatile memory.\n")

    # ------------------------------------------------------------------
    # STAGE 3: Verification Sandbox, Axiomatic Firewall & Generational Purge
    # ------------------------------------------------------------------
    print("[STAGE 3] Loading Verification Sandbox & Initiating GGA Optimization...")
    verifier = GenerationalGeneticVerifier(
        training_dataframe=clean_df,
        target_col=TARGET_COLUMN,
        target_val=TARGET_FLAG_POSITIVE
    )
    
    surviving_swarm, graveyard = verifier.refine_population(
        initial_population=raw_rule_pool,
        generations=GENETIC_GENERATIONS,
        purge_threshold=ACCURACY_PURGE_THRESHOLD
    )

    if not surviving_swarm:
        print("\n❌ Pipeline Halt: No candidate rules passed your accuracy threshold.")
        return

    # ------------------------------------------------------------------
    # STAGE 4: Immutable Logic Manifest Serialization
    # ------------------------------------------------------------------
    print("\n[STAGE 4] Executing Final Cryptographic Logic Manifest Commit...")
    
    # Compile elite rules with automated json-schema validation
    manifest_hash = LogicManifestSerializer.serialize_to_manifest(
        surviving_swarm=surviving_swarm,
        output_path=OUTPUT_MANIFEST_FILE,
        schema_path=SCHEMA_ASSET_FILE,
        version=MANIFEST_VERSION
    )
    
    # Archive failed rule paths for telemetry and log audit checks
    LogicManifestSerializer.archive_graveyard(
        graveyard=graveyard,
        output_path=OUTPUT_GRAVEYARD_FILE
    )

    print("\n================================================================")
    print("🎉 COMPREHENSIVE TRAINING PIPELINE RUN SUCCESSFUL")
    print(f"💾 Logic Manifest Location: {OUTPUT_MANIFEST_FILE}")
    print(f"🔑 Verification Fingerprint: {manifest_hash}")
    print("================================================================")

if __name__ == "__main__":
    run_complete_train_pipeline()