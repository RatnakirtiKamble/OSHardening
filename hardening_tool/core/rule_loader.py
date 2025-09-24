import json
import os
from .rules import LinuxRule

class RuleLoader:
    def __init__(self, rules_path):
        self.rules_path = rules_path
        self.rules = []

    def load_rules(self):
        for filename in os.listdir(self.rules_path):
            if filename.endswith(".json"):
                filepath = os.path.join(self.rules_path, filename)
                with open(filepath, 'r') as f:
                    rule_list = json.load(f)
                    for r in rule_list:
                        rule = LinuxRule(
                            rule_id=r['rule_id'],
                            description=r['description'],
                            severity=r['severity'],
                            expected_value=r['expected_value']
                        )
                        self.rules.append(rule)
        return self.rules
