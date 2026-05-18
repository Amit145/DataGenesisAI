# Insurance Claims Domain Knowledge

Insurance synthetic data should represent an enterprise lifecycle, not isolated random rows.

Typical lifecycle:

1. A customer is created.
2. A policy is issued to the customer.
3. A claim is submitted against an active or recently active policy.
4. The claim receives a claim type, amount, status, and fraud score.
5. A payment may be issued after the claim date.

Important realism expectations:

- Policy, claim, and payment dates must follow a valid temporal order.
- Customer, policy, claim, and payment identifiers should be stable and reproducible.
- Fraud flags should be derived from fraud score instead of random independent assignment.
- Claim amounts and payment amounts should be plausible but synthetic.
- The generated dataset should be reproducible from a contract and seed.
