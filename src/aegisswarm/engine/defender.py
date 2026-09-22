# src/aegisswarm/engine/defender.py
"""
AegisSwarm Defender Engine
Integrates AI Stealer token canaries, behavioral heuristics, and autonomous sandboxing.
"""

import re
from .sandbox import ProcessSandbox


class ThreatInterceptedException(Exception):
    def __init__(self, message, category="[AUTONOMOUS_VIRUS]"):
        super().__init__(f"{category} {message}")
        self.category = category


class AegisSwarmShield:
    def __init__(self):
        # AI Stealer Token Canary Engine: honeypot credentials and files
        # designed specifically to trap credential-harvesting AI agents and malware.
        self.decoy_assets = {
            "/etc/root_auth.env": ("MOCK_ROOT_TOKEN_0x88AF34CE", "[AI_CREDENTIAL_STEALER]"),
            "/var/secure/database.cfg": ("MOCK_DB_PASS=sk_live_zerohack_fake_key", "[AI_CREDENTIAL_STEALER]"),
            "/tmp/canary_credentials.json": ('{"openai_api_key": "sk-ant-api03-FAKE_CANARY_TOKEN_TRAP"}', "[AI_CREDENTIAL_STEALER]"),
            "/root/.aws/credentials": ("[default]\naws_access_key_id=AKIATRAPFAKEKEY\naws_secret_access_key=CANARY_SECRET", "[AI_CREDENTIAL_STEALER]"),
        }
        self.adversarial_heuristics = [
            (r"dump_environment_memory", "[MEMORY_DUMP_ATTACK]"),
            (r"exfiltrate_network_nodes", "[AUTONOMOUS_VIRUS]"),
            (r"bypass_local_antivirus", "[AUTONOMOUS_VIRUS]"),
            (r"harvest_llm_keys", "[AI_CREDENTIAL_STEALER]"),
        ]

    def audit_process_activity(self, process_id: int, binary_comm: str, file_path: str) -> bool:
        print(f"[AegisSwarm Core] Evaluating activity metrics for PID: {process_id} [{binary_comm}]", file=__import__("sys").stderr)

        if file_path in self.decoy_assets:
            decoy_val, category = self.decoy_assets[file_path]
            ProcessSandbox.isolate_pid(process_id)
            raise ThreatInterceptedException(
                f"Process '{binary_comm}' (PID: {process_id}) touched AI canary/decoy asset: '{file_path}'! "
                f"AI stealer trap triggered. Process instantly quarantined.",
                category=category
            )

        lowered_comm = binary_comm.lower()
        for signature, category in self.adversarial_heuristics:
            if re.search(signature, lowered_comm):
                ProcessSandbox.isolate_pid(process_id)
                raise ThreatInterceptedException(
                    f"Automated threat strategy matched: '{signature}'! "
                    f"Terminating target session authorization.",
                    category=category
                )

        print("Process validation profile clean. Authorizing interaction with physical hardware layer.", file=__import__("sys").stderr)
        return True
