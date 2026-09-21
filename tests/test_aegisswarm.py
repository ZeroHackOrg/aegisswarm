# tests/test_aegisswarm.py
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from aegisswarm.engine.defender import AegisSwarmShield, ThreatInterceptedException
from aegisswarm.audit import AegisSwarmAuditLogger
import pytest


def test_defender_traps_decoy():
    shield = AegisSwarmShield()
    with pytest.raises(ThreatInterceptedException):
        shield.audit_process_activity(100, "cat", "/etc/root_auth.env")


def test_defender_blocks_heuristic():
    shield = AegisSwarmShield()
    with pytest.raises(ThreatInterceptedException):
        shield.audit_process_activity(101, "dump_environment_memory", "/tmp/safe.txt")


def test_audit_logger(tmp_path):
    path = tmp_path / "audit.jsonl"
    logger = AegisSwarmAuditLogger(str(path))
    logger.log("trapped", {"pid": 100}, severity="critical")
    assert logger.verify_chain() is True
    assert len(logger.incidents()) == 1