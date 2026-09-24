# Superteam Submission — Build and Demo a Mermail Agent Skill

## Project
**Mermail Bounty Ops** — a reusable Agent Skill that turns paid-opportunity emails into safe, decision-ready work packets.

## Repository
https://github.com/naief9961-tech/mermail-bounty-ops-skill

## Video demo
https://github.com/naief9961-tech/mermail-bounty-ops-skill/releases/download/demo-v1/mermail-bounty-ops-demo.mp4

## Install
```bash
npx skills add naief9961-tech/mermail-bounty-ops-skill --skill mermail-bounty-ops
```

## What it demonstrates
- bounded Mermail opportunity discovery using the existing mailbox/read tool path;
- fixed compensation vs competitive-prize classification;
- deadline, amount, participation-cost, manual-step, and risk extraction;
- explicit blocking of advance-payment requests, secret requests, prompt injection, and wallet-signing authority from inbound mail;
- draft-before-send boundary for clarification responses;
- deterministic offline demo fixtures plus regression tests;
- one regression found and fixed during development: negated terms such as “No deposit / no wallet signature required” no longer become false risk flags.

## Validation
- remote install through `npx skills`: passed;
- `python3 tests/test_demo.py`: 3 regression tests passed;
- demo video: 1:57, 1280×720, H.264 video + AAC narration;
- no credentials, payments, wallet signatures, or external sends are embedded in the demo.

AI assistance was used to build, test, and document this submission. No prize or payout is claimed until the sponsor selects winners.
