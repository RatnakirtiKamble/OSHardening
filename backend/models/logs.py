from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from datetime import datetime


# ------------------------------
# Compliance Reports
# ------------------------------
class ComplianceReport:
    __tablename__ = "compliance_reports"

    id = Column(Integer, primary_key=True)
    rulebook_version_id = Column(Integer, ForeignKey("rulebook_versions.id"))
    rule_id = Column(String, ForeignKey("rules.id"))
    employee_id = Column(Integer, ForeignKey("employees.id"))
    previous_value = Column(String)
    applied_value = Column(String)
    status = Column(String)  # Successful / Unsuccessful
    timestamp = Column(DateTime, default=datetime.utcnow)
