# src/aegisswarm/cli/controls.py
import argparse
import json
import sys
import threading
import time

from ..audit import AegisSwarmAuditLogger
from ..engine.defender import AegisSwarmShield, ThreatInterceptedException
from .telemetry_ui import run_telemetry_console, LIVE_THREAT_FEED


def cmd_start(args):
    shield = AegisSwarmShield()
    audit = AegisSwarmAuditLogger(path="aegisswarm_audit.jsonl")
    print("🔌 [AegisSwarm] Active monitoring hooks attached to system runtime infrastructure...", file=sys.stderr)

    try:
        shield.audit_process_activity(
            process_id=8812,
            binary_comm="EXECUTE: dump_environment_memory",
            file_path="/etc/root_auth.env",
        )
    except ThreatInterceptedException as warning:
        incident = {"timestamp": time.time(), "alert_summary": str(warning)}
        LIVE_THREAT_FEED.append(incident)
        audit.log("threat_trapped", incident, severity="critical")
        print(warning)
        return 0
    return 1


def cmd_ui(args):
    run_telemetry_console(port=args.port, feed_store=LIVE_THREAT_FEED)
    print(f"📡 [AegisSwarm] Dashboard active at http://localhost:{args.port}")
    threading.Thread(target=cmd_start, args=(args,), daemon=True).start()
    threading.Event().wait()


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="aswarm", description="Behavioral Contextual Decoy Matrix & Autonomous Response Engine")
    sub = parser.add_subparsers(dest="command", required=True)

    p_start = sub.add_parser("start", help="Execute threat simulation loop")
    p_start.set_defaults(func=cmd_start)

    p_ui = sub.add_parser("ui", help="Launch telemetry web dashboard console")
    p_ui.add_argument("--port", type=int, default=9999)
    p_ui.set_defaults(func=cmd_ui)

    return parser


def main(argv=None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    try:
        return args.func(args) or 0
    except Exception as error:
        print(f"[aswarm] fatal: {error}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())