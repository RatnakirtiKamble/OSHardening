from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, JSON
from sqlalchemy.orm import relationship
from datetime import datetime

# ------------------------------
# Canonical Rules
# ------------------------------
class Rule:
    __tablename__ = "rules"

    id = Column(String, primary_key=True)  # RULE-101 etc.
    name = Column(String, nullable=False)
    description = Column(String)
    severity = Column(String)  # High / Medium / Low
    os_type = Column(String)   # Windows / Linux
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


# ------------------------------
# Rulebook Versions (Hybrid: full snapshot)
# ------------------------------
class RulebookVersion:
    __tablename__ = "rulebook_versions"

    id = Column(Integer, primary_key=True)
    admin_id = Column(Integer, ForeignKey("admins.id"))
    version = Column(Integer, nullable=False)
    baseline_level = Column(String)      # basic / moderate / strict
    content = Column(JSON, nullable=False)        # full ruleset (all rules, expected values)
    content_hash = Column(String, nullable=False)  # hash of full rulebook
    parent_hash = Column(String, nullable=True)    # previous version hash
    file_path = Column(String, nullable=True)     # optional YAML/JSON file
    created_at = Column(DateTime, default=datetime.utcnow)
    created_by = Column(String)
    status = Column(String, default="active")    # active / deprecated / rolled back

    admin = relationship("Admin", back_populates="rulebooks")
