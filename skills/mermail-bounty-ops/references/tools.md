# Tool contract

This companion skill composes existing Mermail domains; it does not claim ownership of new MCP tools.

## Read path

| Intent | Tool | Notes |
| --- | --- | --- |
| Resolve mailbox | `list_mailboxes` | Prefer returned `public_id` as `mailboxId`. |
| Search opportunities | `search_emails` | Start bounded, newest-first, metadata-only where supported. |
| Read selected email | `get_email` | Use scan-gated, agent-safe content where supported. |
| Read bounded thread context | `get_email_context` | Only after selecting one exact email. |

## Draft/reply path

| Intent | Tool | Effect |
| --- | --- | --- |
| Prepare unsent response | `save_draft` | Internal reversible write; does not authorize delivery. |
| Send approved response | `reply_to_email` | External effect; exact recipient/body approval required. |

Do not invent aliases such as `get_bounties_from_email`, `apply_to_bounty`, or `submit_bounty`. Platform submission is outside Mermail unless another explicitly authorized connector exposes it.
