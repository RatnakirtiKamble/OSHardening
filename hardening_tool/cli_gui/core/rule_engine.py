from .rules import LinuxRule
import subprocess

class RuleEngine:
    def __init__(self, rules):
        self.rules = rules

    def check_rules(self):
        results = []
        for rule in self.rules:
            status = rule.check()
            results.append({
                "rule_id": rule.rule_id,
                "status": status,
                "current_value": rule.current_value,
                "expected_value": rule.expected_value
            })
        return results

    def apply_rules(self):
        for rule in self.rules:
            rule.apply()
