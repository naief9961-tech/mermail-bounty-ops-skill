import importlib.util
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("demo_runner", ROOT / "demo" / "run_demo.py")
demo = importlib.util.module_from_spec(spec)
spec.loader.exec_module(demo)


def load_packets():
    messages = json.loads((ROOT / "demo" / "sample_inbox.json").read_text())
    return {m["email_id"]: demo.analyze(m) for m in messages}


def test_fixed_project_negated_risks_are_not_false_positives():
    item = load_packets()["msg_fixed_qa"]
    assert item["payment_model"] == "fixed-work"
    assert item["cost_to_participate"] == "zero-stated"
    assert item["risk_flags"] == []
    assert "wallet-signature" not in item["manual_steps"]


def test_competition_is_not_presented_as_guaranteed():
    item = load_packets()["msg_skill_bounty"]
    assert item["payment_model"] == "competitive-prize"
    assert "no payout is guaranteed" in item["payment_note"].lower()


def test_advance_payment_and_secret_request_block_execution():
    item = load_packets()["msg_malicious"]
    assert item["status"] == "blocked"
    assert item["cost_to_participate"] == "stated-spend"
    assert "advance-payment-or-spend-request" in item["risk_flags"]
    assert "secret-request" in item["risk_flags"]
    assert "prompt-injection" in item["risk_flags"]


if __name__ == "__main__":
    test_fixed_project_negated_risks_are_not_false_positives()
    test_competition_is_not_presented_as_guaranteed()
    test_advance_payment_and_secret_request_block_execution()
    print("3 demo regression tests passed")
