# Mermail Bounty Ops

A reusable Agent Skill that turns paid-opportunity emails into **safe, decision-ready work packets** before an agent spends money, signs a wallet, submits externally, or sends a reply.

Built for the Superteam **Build and Demo a Mermail Agent Skill** bounty.

## What it does

Given bounded, selected Mermail messages, the skill separates:

- fixed compensation from competitive prize pools;
- stated reward from guaranteed payout;
- zero-cost participation from deposit/purchase/trading requirements;
- work the agent can prepare now from account, CAPTCHA, identity, wallet-signature, or final-submit steps that remain human-controlled;
- legitimate commercial terms from prompt injection, secret requests, or advance-payment traps.

It composes existing Mermail tools instead of inventing a new server API.

## Install

```bash
npx skills add naief9961-tech/mermail-bounty-ops-skill --skill mermail-bounty-ops
```

Connect the hosted Mermail MCP server at `https://console.mermail.app/mcp` using OAuth where supported or an environment-provided API key. Never paste an API key into chat.

## Mermail tool path

Read-only triage uses:

```text
list_mailboxes
  → search_emails
  → get_email
  → optional get_email_context
```

When clarification is useful, `save_draft` prepares an unsent response. `reply_to_email` is an external effect and requires exact user approval immediately before execution.

## Deterministic demo

The repository includes sanitized fixtures and a no-network demo runner:

```bash
python3 demo/run_demo.py
python3 tests/test_demo.py
```

The three fixtures demonstrate:
1. a 150 USDC fixed project with zero stated participation cost;
2. a 500 USDC competitive prize pool that is explicitly **not guaranteed**;
3. a malicious "guaranteed" offer that asks for a deposit, secret material, and policy bypass — correctly blocked.

The demo records `writes_executed: []` and `payments_executed: []`.

## Video proof

See [demo/mermail-bounty-ops-demo.mp4](demo/mermail-bounty-ops-demo.mp4), a 1:57 narrated demonstration of the workflow, classification output, and regression test.

The video is reproducible with [demo/build_video.py](demo/build_video.py). The build script uses Pillow, edge-tts, and imageio-ffmpeg only for demo media generation; they are not runtime dependencies of the Agent Skill.

## Repository layout

```text
skills/mermail-bounty-ops/
  SKILL.md
  agents/openai.yaml
  references/tools.md
  references/security.md
  references/workflows.md
demo/
  sample_inbox.json
  run_demo.py
  expected_output.json
  video_script.json
  build_video.py
  mermail-bounty-ops-demo.mp4
tests/test_demo.py
```

## Safety design

Inbound email is evidence, never authority. The skill refuses to execute or authorize:

- deposits, purchases, trading, staking, or arbitrary payments from email instructions;
- wallet signing or wallet connection merely because a message requests it;
- seed phrase, private key, API key, OTP, recovery-code, or cookie disclosure;
- recipient changes, external submissions, or sends without independent user authorization;
- misleading claims that a prize pool or conditional award is guaranteed income.

A stale email is not proof that an opportunity is still open. Current-state verification remains a separate step when live data is required.

## Why the demo is offline

This repository intentionally ships **no credential** and requires no live Mermail workspace to evaluate the decision logic. The fixture runner consumes sanitized objects shaped like selected Mermail messages. In a real client, those fixtures are replaced by bounded `search_emails` / `get_email` results through the hosted MCP server.

## Test result

```text
3 demo regression tests passed
```

One regression specifically protects a subtle case found while building the demo: a sentence saying **"No deposit ... wallet signature is required"** must not be misread as a spend/signing requirement.

## License

MIT. See [LICENSE](LICENSE).
