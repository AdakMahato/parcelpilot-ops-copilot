# Product Documentation: ParcelPilot Ops Copilot

## 1. Primary User
The primary user is an authorized ParcelPilot support agent or operations team member. They spend their day investigating discrepancies in shipments, resolving bulk upload errors, navigating complex service credit SLAs, and determining when to escalate tickets.

## 2. Problem Being Solved
Customer support agents constantly switch contexts between CRMs, billing systems, carrier tracking, and a static knowledge base of PDF agreements. This fragmentation creates severe delays, leads to incorrect SLA application (like ignoring custom enterprise terms), and causes operational fatigue.

## 3. Why Internal Support/Operations?
Internal operations are high-stakes but have high tolerance for steep technical tooling if it improves efficiency. Unlike consumer-facing AI (where hallucinations destroy trust), an internal copilot acts as a research assistant where the agent remains in the loop to verify evidence and confirm state-changing actions.

## 4. Issue Intelligence and Proactive Detection
The "Issue Intelligence" dashboard shifts the team from reactive ticket-answering to proactive management. The backend dynamically groups incoming tickets by subject string (e.g., "Bulk upload") and calculates real-time SLA metrics against the static dataset snapshot, allowing operators to spot platform-level degradations before the engineering team does.

## 5. Trust/Reliability Approach
The copilot cites its sources explicitly inside the UI. We force the LLM to provide its deterministic reasoning chain and rank customer-specific agreements over general SOPs. Users aren't just given a "Yes/No" – they are given the "Yes/No, because... [Source Link]".

## 6. What I Would Build Next
- **Webhook Integration**: Direct hooks into Shopify/Magento integrations to verify order states instantly.
- **Bi-Directional Actioning**: Expanding the `/api/action/confirm` to actually mutate the `sqlite` database (e.g., generating service credits directly on the account ledger).

## 7. What Was Intentionally Left Out
- We omitted raw text generation templates for email responses. Support agents can write emails themselves; they need help with the *investigation*, not the *prose*.
- No generic AI avatars or conversational chitchat.

## 8. Primary Product Metric
"Percentage of support investigations resolved without human escalation, while maintaining an audited accuracy target."
