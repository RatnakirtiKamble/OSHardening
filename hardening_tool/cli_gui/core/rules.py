class HardeningRule:
    def __init__(self, rule_id, description, severity, expected_value, target_os):
        self.rule_id = rule_id
        self.description = description
        self.severity = severity
        self.expected_value = expected_value
        self.target_os = target_os
        self.current_value = None
        self.rollback_value = None
        self.status = "Not Checked"

    
    def check(self):
        """Override in subclasses"""
        raise NotImplementedError
    
    def apply(self):
        """Override in subclasses"""
        raise NotImplementedError
    
    def rollback(self):
        """Restore previous value"""
        if self.rollback_value is not None:
            self.current_value = self.rollback_value
            self.status = "Rolled Back"

class LinuxRule(HardeningRule):
    def __init__(self, rule_id, description, severity, expected_value):
        super().__init__(rule_id, description, severity, expected_value, "Linux")

    def check(self):
        print("Not implemented yet")
    
    def apply(self):
        print("Not implemented yet")

class WindowsRule(HardeningRule):
    def __init__(self, rule_id, description, severity, expected_value):
        super().__init__(rule_id, description, severity, expected_value, "Windows")

    def check(self):
        print("Not implemented yet")
    
    def apply(self):
        print("Not implemented yet")
