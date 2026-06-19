import pandas as pd
import random
import copy
from typing import List, Dict, Any, Tuple
from core.discovery_factory.axioms import AxiomaticSeed, AxiomViolationError

class GenerationalGeneticVerifier:
    """
    Stage 3 Component: Verification Sandbox
    Executes a Generational Genetic Algorithm (GGA) to parse, score, and 
    refine a population of AST rules[cite: 11, 49, 68]. Purges underperforming rules 
    and archives failures into a graveyard.
    """
    def __init__(self, training_dataframe: pd.DataFrame, target_col: str, target_val: Any):
        self.df = training_dataframe
        self.target_col = target_col
        self.target_val = target_val
        # Instantiate an active axiom validation seed registry to protect data mutations
        self.axiom_validator = AxiomaticSeed(current_version="0.1")

    def evaluate_ast_fitness(self, rule_manifest: Dict[str, Any]) -> float:
        """
        Parses the Abstract Syntax Tree structure and executes vectorized 
        boolean logic to determine its exact accuracy across the dataset.
        """
        ast = rule_manifest["ast"]
        feature = ast["left"]["value"]
        operator = ast["operator"]
        threshold = ast["right"]["value"]

        if operator == "lt":
            mask = self.df[feature] < threshold
        elif operator == "gt":
            mask = self.df[feature] > threshold
        elif operator == "lte":
            mask = self.df[feature] <= threshold
        elif operator == "gte":
            mask = self.df[feature] >= threshold
        else:
            mask = self.df[feature] == threshold

        predictions = mask.astype(int)
        actuals = (self.df[self.target_col] == self.target_val).astype(int)

        accuracy = (predictions == actuals).sum() / len(self.df)
        return float(accuracy)

    def refine_population(
        self, 
        initial_population: List[Dict[str, Any]], 
        generations: int = 5, 
        purge_threshold: float = 0.70
    ) -> Tuple[List[Dict[str, Any]], List[Dict[str, Any]]]:
        """
        Runs the main GGA optimization loop[cite: 11, 68]. 
        Subjects all structural mutations to the Axiomatic Firewall before grading.
        """
        current_pool = [copy.deepcopy(rule) for rule in initial_population]
        graveyard = []
        surviving_swarm = []

        print(f"🧬 Initializing GGA Sandbox across {generations} generational cascades... [cite: 11, 49]")

        for gen in range(generations):
            scored_population = []
            
            # 1. Score all rules in the current generation
            for rule in current_pool:
                accuracy = self.evaluate_ast_fitness(rule)
                rule["metadata"]["validation_accuracy"] = round(accuracy, 4)
                rule["metadata"]["generation_evaluated"] = gen
                scored_population.append(rule)

            # 2. Sort by performance
            scored_population.sort(key=lambda x: x["metadata"]["validation_accuracy"], reverse=True)
            peak_accuracy = scored_population[0]["metadata"]["validation_accuracy"]
            print(f" -> Generation {gen + 1} complete. Current Peak Accuracy: {peak_accuracy * 100:.2f}%")

            # Update the global axiom check registry with elite rule structures discovered so far
            self.axiom_validator.rules_registry = scored_population[:50]

            # 3. Apply parametric drift mutation to keep the population evolving
            next_pool = []
            for rule in scored_population:
                # Deepcopy isolates nested references to preserve memory boundaries
                mutated_rule = copy.deepcopy(rule)
                drift_factor = random.uniform(0.95, 1.05)
                
                current_threshold = mutated_rule["ast"]["right"]["value"]
                mutated_rule["ast"]["right"]["value"] = round(current_threshold * drift_factor, 4)

                # Axiomatic Firewall Filter Guard: Ensure mutated parameters remain valid 
                try:
                    self.axiom_validator.validate_rule(mutated_rule, new_version="0.1")
                    next_pool.append(mutated_rule)
                except AxiomViolationError as violation:
                    # Capture and isolate illegal mutations safely into quarantine telemetry
                    mutated_rule["metadata"]["purge_reason"] = f"Axiom Drift Violation: {str(violation)}"
                    graveyard.append(mutated_rule)

            # Fallback if an aggressive constraint configuration completely clears the pool [cite: 33, 34]
            if not next_pool:
                print("⚠️ Critical Constraint Collision: Pool depleted by firewall rules. Reverting to parent pool[cite: 33].")
                current_pool = [copy.deepcopy(r) for r in scored_population]
            else:
                current_pool = next_pool

        # === THE FINAL PURGE ===
        for rule in current_pool:
            final_accuracy = self.evaluate_ast_fitness(rule)
            rule["metadata"]["validation_accuracy"] = round(final_accuracy, 4)
            
            if final_accuracy >= purge_threshold:
                surviving_swarm.append(rule)
            else:
                rule["metadata"]["purge_reason"] = f"Failed accuracy threshold ({final_accuracy:.4f} < {purge_threshold})"
                graveyard.append(rule)

        print("\n Purge Complete.")
        print(f"   - Surviving Swarm Ruleset: {len(surviving_swarm)} rules retained.")
        print(f"   - Banished to Graveyard: {len(graveyard)} rules purged.")

        return surviving_swarm, graveyard