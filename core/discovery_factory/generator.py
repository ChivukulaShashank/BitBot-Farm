import pandas as pd
import random
import uuid
from typing import List, Dict, Any

# =====================================================================
# ABSTRACT SYNTAX TREE (AST) COMPONENT DEFINITIONS
# =====================================================================
class ASTNode:
    """Base class for all Abstract Syntax Tree nodes."""
    def to_dict(self) -> Dict[str, Any]:
        raise NotImplementedError


class FeatureNode(ASTNode):
    """AST leaf node representing a clinical measurement column."""
    def __init__(self, name: str):
        self.name = name

    def to_dict(self) -> str:
        return self.name


class ThresholdNode(ASTNode):
    """AST leaf node representing a static numerical boundary value."""
    def __init__(self, value: float):
        self.value = value

    def to_dict(self) -> float:
        return self.value


class ExpressionAST(ASTNode):
    """
    Root AST structure that binds a Feature node and Threshold node 
    together via a strict logical conditional operator.
    """
    def __init__(self, rule_id: str, feature: FeatureNode, operator: str, threshold: ThresholdNode):
        self.rule_id = rule_id
        self.feature = feature
        self.operator = operator  # 'lt', 'gt', 'lte', 'gte'
        self.threshold = threshold

    def to_dict(self) -> Dict[str, Any]:
        """Serializes the syntax tree structure into a standardized manifest map."""
        return {
            "rule_id": self.rule_id,
            "ast": {
                "node_type": "BinaryExpression",
                "left": {"node_type": "Feature", "value": self.feature.to_dict()},
                "operator": self.operator,
                "right": {"node_type": "Threshold", "value": self.threshold.to_dict()}
            },
            "metadata": {
                "pure": True,
                "output_consequent": 1
            }
        }


# =====================================================================
# LOGICAL INFERENCE FACTORY COMPONENT
# =====================================================================
class LogicalRuleFactory:
    """
    Stage 2 Component: Ruleset Generation
    Uses statistical data profiles to infer mining constraints and generates
    large, schema-compliant candidate AST populations.
    """
    @staticmethod
    def infer_data_boundaries(df: pd.DataFrame, features: List[str], target_col: str, target_val: Any) -> Dict[str, Any]:
        """
        Performs logical inference by matching metric skews against targeted patient outcomes.
        Establishes high-probability exploration 'hot zones'.
        """
        positive_cases = df[df[target_col] == target_val]
        if positive_cases.empty:
            raise ValueError(f"Inference Failure: Zero rows found where {target_col} == {target_val}")

        inferred_schema = {}
        for feature in features:
            global_median = df[feature].median()
            positive_median = positive_cases[feature].median()
            
            # Infer operational direction based on median value distance shifts
            op_direction = "lt" if positive_median < global_median else "gt"
            
            # Use 10th and 90th percentiles to define robust search zone windows
            inferred_schema[feature] = {
                "default_operator": op_direction,
                "search_min": float(positive_cases[feature].quantile(0.10)),
                "search_max": float(positive_cases[feature].quantile(0.90))
            }
        return inferred_schema

    @classmethod
    def generate_ast_population(cls, inferred_schema: Dict[str, Any], pool_size: int = 10000) -> List[Dict[str, Any]]:
        """
        Generates an immutable structural population pool of completely UNIQUE AST rulesets.
        Guards against duplicate collisions using logical signature tracking.
        """
        features = list(inferred_schema.keys())
        generated_ruleset = []
        seen_signatures = set()  # Tracks uniqueness: (feature, operator, threshold)

        max_attempts = pool_size * 3  # Circuit breaker to prevent infinite loops if pool size is physically impossible
        attempts = 0

        while len(generated_ruleset) < pool_size and attempts < max_attempts:
            attempts += 1
            
            # 1. Select random isolated feature
            feature_name = random.choice(features)
            constraints = inferred_schema[feature_name]
            
            # 2. Extract operational constraint with a 15% exploration mutation offset
            operator = constraints["default_operator"]
            if random.random() > 0.85:
                operator = "gt" if operator == "lt" else "lt"

            # 3. Calculate randomized metric boundary within target parameters (4 decimals to allow density)
            threshold_val = round(random.uniform(constraints["search_min"], constraints["search_max"]), 4)

            # Check for duplicate rule combinations before instantiating components
            rule_signature = (feature_name, operator, threshold_val)
            if rule_signature in seen_signatures:
                continue
                
            seen_signatures.add(rule_signature)

            # 4. Construct structural AST tree nodes
            rule_id = f"RULE-{uuid.uuid4().hex[:6].upper()}"
            feature_node = FeatureNode(feature_name)
            threshold_node = ThresholdNode(threshold_val)
            
            ast_structure = ExpressionAST(
                rule_id=rule_id,
                feature=feature_node,
                operator=operator,
                threshold=threshold_node
            )

            # 5. Serialize syntax block to master pool array
            generated_ruleset.append(ast_structure.to_dict())

        if len(generated_ruleset) < pool_size:
            print(f"⚠️ Population ceiling reached: Generated {len(generated_ruleset)} unique rules out of requested {pool_size}.")

        return generated_ruleset