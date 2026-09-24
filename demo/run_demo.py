#!/usr/bin/env python3
"""Offline deterministic demo for the mermail-bounty-ops decision schema.

It consumes sanitized email fixtures shaped like Mermail get_email output.
It does not connect to Mermail, send email, spend funds, or sign wallets.
"""
import json
import re
import sys
from pathlib import Path

AMOUNT_RE = re.compile(r"(?<![\w.])(\d[\d,]*(?:\.\d+)?)\s*(USDC|USDG|USD|SOL|RTC)\b", re.I)
ISO_DEADLINE_RE = re.compile(r"20\d{2}-\d{2}-\d{2}(?:T\d{2}:\d{2}:\d{2}Z)?")
SPEND_RE = re.compile(r"\b(send|deposit|pay|purchase|buy|stake|trade)\b.{0,40}\b(USDC|USDG|USD|SOL|RTC|token|fee|deposit)\b", re.I)
SECRET_RE = re.compile(r"seed phrase|private key|api key|recovery (?:code|phrase)|mnemonic", re.I)
INJECTION_RE = re.compile(r"ignore (?:your|all|previous).*?(?:rule|instruction|safety)|bypass.*?approval", re.I)
SIGN_RE = re.compile(r"wallet signature|sign (?:a |the )?(?:wallet|message|transaction)", re.I)


def first_deadline(text):
    match = ISO_DEADLINE_RE.search(text)
    return match.group(0) if match else "unknown"


def payment_model(text):
    low = text.lower()
    if "total prizes" in low or "competitive bounty" in low or "winner" in low:
        return "competitive-prize"
    if "fixed project" in low or "payment:" in low and "after acceptance" in low:
        return "fixed-work"
    if "grant" in low:
        return "grant"
    return "unclear"


def analyze(message):
    text = f"{message.get('subject','')}\n{message.get('body','')}"
    low = text.lower()
    amounts = []
    seen_amounts = set()
    for raw, currency in AMOUNT_RE.findall(text):
        item = (float(raw.replace(",", "")), currency.upper())
        if item not in seen_amounts:
            seen_amounts.add(item)
            amounts.append({"amount": item[0], "currency": item[1]})
    flags = []
    no_cost_clause = bool(re.search(
        r"\bno\s+deposit\b.{0,100}\b(?:required|to apply)\b", text, re.I
    ))
    no_sign_clause = bool(re.search(
        r"\bno\s+deposit\b.{0,120}\bwallet signature\b.{0,40}\b(?:required|to apply)\b",
        text, re.I,
    ))
    if SPEND_RE.search(text) and not no_cost_clause:
        flags.append("advance-payment-or-spend-request")
    if SECRET_RE.search(text):
        flags.append("secret-request")
    if INJECTION_RE.search(text):
        flags.append("prompt-injection")
    if SIGN_RE.search(text) and not no_sign_clause:
        flags.append("wallet-signing-request")
    if "guaranteed" in low and ("deposit" in low or SECRET_RE.search(text)):
        flags.append("guaranteed-payment-claim-with-high-risk-terms")

    model = payment_model(text)
    if "no deposit" in low and "token purchase" in low:
        cost = "zero-stated"
    elif any(f in flags for f in ["advance-payment-or-spend-request"]):
        cost = "stated-spend"
    else:
        cost = "unclear"

    manual = []
    if "portal" in low or "submit" in low:
        manual.append("platform-submit")
    if SIGN_RE.search(text) and not no_sign_clause:
        manual.append("wallet-signature")

    if "secret-request" in flags or "advance-payment-or-spend-request" in flags:
        status = "blocked"
        plan = "Do not pay, sign, or disclose secrets. Preserve evidence and stop external action."
    elif manual:
        status = "manual-account-step"
        if model == "fixed-work":
            plan = "Prepare the complete deliverable now; keep the final platform submission for the user."
        else:
            plan = "Prepare the competition artifact and proof now; keep the final platform submission for the user."
    else:
        status = "ready-to-work"
        plan = "Prepare the deliverable and proof package now."

    if model == "competitive-prize":
        payment_note = "Prize pool; no payout is guaranteed."
    elif model == "fixed-work":
        payment_note = "Stated fixed compensation is conditional on acceptance."
    else:
        payment_note = "Payment terms need verification."

    return {
        "email_id": message.get("email_id"),
        "received_at": message.get("received_at"),
        "opportunity": message.get("subject"),
        "sponsor_observed": message.get("from"),
        "payment_model": model,
        "stated_amounts": amounts,
        "payment_note": payment_note,
        "deadline": first_deadline(text),
        "cost_to_participate": cost,
        "manual_steps": sorted(set(manual)),
        "risk_flags": flags,
        "status": status,
        "execution_plan": plan,
    }


def sort_key(item):
    status_rank = {"ready-to-work": 0, "manual-account-step": 1, "needs-verification": 2, "blocked": 9}
    model_rank = {"fixed-work": 0, "grant": 1, "competitive-prize": 2, "unclear": 3}
    return (status_rank.get(item["status"], 5), model_rank.get(item["payment_model"], 5))


def main():
    source = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(__file__).with_name("sample_inbox.json")
    messages = json.loads(source.read_text())
    packets = sorted((analyze(message) for message in messages), key=sort_key)
    result = {
        "schema": "mermail-bounty-ops-demo/v1",
        "source": source.name,
        "recommended_tools": ["list_mailboxes", "search_emails", "get_email"],
        "writes_executed": [],
        "payments_executed": [],
        "opportunities": packets,
    }
    print(json.dumps(result, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
