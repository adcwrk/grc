---
artifact_id: SOW-test-client-1-0001
artifact_type: sow
client: "test-client-1"
status: draft
owner: TBD
sensitivity: CONFIDENTIAL
framework:
  - nist-csf-2.0
created: "2026-08-14"
updated: "2026-08-14"
tags:
  - sow
  - engagement
  - vciso
  - nist-csf-2.0
sources:
  - SRC-0001
  - SRC-0002
  - SRC-0003
---

# Statement Of Work — NIST CSF 2.0 vCISO Advisory Engagement

## Document Status

**Draft. Not reviewed. Not executed. Not client-ready.**

This draft is built entirely from synthetic intake material. All three cataloged sources
(`SRC-0001`, `SRC-0002`, `SRC-0003` in `clients/test-client-1/sources/catalog.jsonl`)
declare themselves AI-generated and state "Not evidence. Do not use for formal assessment
conclusions." Nothing in this SOW has been validated with a real client.

Commercial terms — fees, rates, hours, term length, calendar dates, staffing, and legal
provisions — are **absent from all sources and have not been invented**. They are recorded
in [Open Questions](#open-questions) and must be supplied by the consultant before this
draft can be issued.

## Parties

| Role | Party | Basis |
| --- | --- | --- |
| Client | Apex Precision Components, Inc. ("Apex Precision") | `SRC-0003` |
| Consultant | TBD | Not stated in any source; `consultant` is null in `engagement.yaml` |

Naming discrepancy: the workspace client of record is `test-client-1`
(`clients/test-client-1/client.yaml`), while the intake material describes
"Apex Precision Components, Inc." This SOW uses the intake name. See `ASM-0002`.

## Engagement Summary

Apex Precision is a medium-size discrete manufacturer operating four sites — headquarters
in Grand Rapids, Michigan; a main plant in Dayton, Ohio; a secondary plant in Fort Wayne,
Indiana; and a distribution and customer service office in Louisville, Kentucky — with
approximately 640 employees and approximately 520 active workforce identities (`SRC-0003`).

The Consultant will provide virtual CISO (vCISO) advisory services structured around
NIST CSF 2.0. The engagement establishes a governance rhythm, baselines the current state
of the corporate IT cybersecurity program, and produces a prioritized improvement roadmap
for executive decision-making (`SRC-0002`, `SRC-0003`).

This is an **advisory engagement**. It does not produce certification, attestation, or
regulatory audit conclusions (`SRC-0003`).

## Objectives

Derived from `SRC-0002` and `SRC-0003`:

1. Establish a practical cybersecurity governance rhythm appropriate to a medium-size
   manufacturing business, including risk register ownership and security roadmap cadence.
2. Baseline the current cybersecurity program against NIST CSF 2.0 for the corporate IT
   environment.
3. Validate current practices across identity, endpoint, backup, vulnerability management,
   incident response, and third-party risk.
4. Produce a prioritized security roadmap with owners, target dates, and budget ranges.
5. Improve executive reporting on cyber risk without creating unnecessary administrative
   burden.
6. Define a pragmatic improvement plan covering the next two quarters.

## Scope

### In Scope

Corporate IT environment only (`SRC-0002`, `SRC-0003`, `SRC-0001`):

- IT governance, policy structure, and security program management.
- Identity and access management for workforce users, including Microsoft Entra ID.
- Microsoft 365 tenant and IT-managed SaaS administration.
- Corporate endpoint fleet: laptops, office desktops, and shared workstations.
- Site LAN, WAN, wireless, firewalls, VPN, DNS, DHCP, and network monitoring across all
  four sites.
- On-premises server infrastructure at headquarters.
- Backup administration and restore testing.
- Vulnerability management for IT assets.
- Incident response planning and readiness.
- Third-party and vendor risk for critical IT and SaaS providers.
- Security awareness training program.
- IT asset management and the IT service desk, including joiner/mover/leaver process.
- Business applications used by finance, HR, sales, customer service, engineering office
  staff, and warehouse users.

### Out Of Scope

Explicitly excluded (`SRC-0002`, `SRC-0003`, `SRC-0001`):

- Operational technology, industrial control systems, PLCs, HMIs, SCADA, CNC controllers,
  and plant-floor automation networks.
- Safety systems, quality instrumentation networks, and machine telemetry platforms.
- Physical security systems, except where they depend on corporate identity or network
  services.
- Formal certification, attestation, compliance audit, or regulatory conclusions of any kind.
- Penetration testing, red teaming, and technical security testing (not requested in any
  source; excluded here to prevent scope ambiguity — confirm with client).
- Remediation implementation, engineering labor, and system configuration changes (advisory
  only unless separately agreed).

### Geographic Scope

Four corporate IT sites connected by a managed SD-WAN (`SRC-0002`, `SRC-0001`):

| Site | Location | Business role | Approx. headcount |
| --- | --- | --- | --- |
| Site 1 | Grand Rapids, Michigan | Headquarters, finance, HR, engineering leadership | 180 |
| Site 2 | Dayton, Ohio | Main manufacturing plant | 240 |
| Site 3 | Fort Wayne, Indiana | Secondary manufacturing plant | 150 |
| Site 4 | Louisville, Kentucky | Distribution and customer service | 70 |

## Applicable Framework

- NIST CSF 2.0 — sole organizing framework, reporting vocabulary, and program structure
  (`SRC-0002`; recorded as `DEC-0002` in `../context/decisions.md`).

No other framework is in scope. CMMC, NIST SP 800-171, and ISO 27001 were considered during
onboarding and not selected.

## Known Environment

Systems identified in intake (`SRC-0003`, `SRC-0001`). This list is a starting point for
discovery, not a validated asset inventory:

| Domain | Systems |
| --- | --- |
| Identity | Microsoft Entra ID (SSO and MFA) |
| Productivity / collaboration | Microsoft 365 |
| Endpoint management | Microsoft Intune |
| Endpoint detection and response | CrowdStrike Falcon |
| Network | Fortinet firewalls (all sites), Cisco switching and wireless (all sites), managed SD-WAN |
| Server infrastructure | VMware cluster at headquarters |
| Backup | Veeam, including cloud capacity tier |
| Business applications | NetSuite ERP, Salesforce CRM |
| ITSM | ServiceNow |
| Awareness training | KnowBe4 |
| Remote access | VPN terminating at the headquarters firewall |

## Approach

`SRC-0002` records a recommendation to run a discovery and baseline phase of approximately
four weeks before publishing roadmap commitments. That recommendation is reflected below as
phase sequencing. **No calendar dates, durations, or effort commitments are contracted here**
— see [Timeline](#timeline).

**Phase 1 — Kickoff and discovery.** Confirm scope boundaries, stakeholders, and reporting
expectations. Collect the information requested in [Client Responsibilities](#client-responsibilities).
Produce the kickoff summary and open question log.

**Phase 2 — Current-state baseline.** Assess the corporate IT environment against NIST CSF
2.0 Functions, Categories, and Subcategories through stakeholder interviews and documentation
review. Produce the current-state CSF profile.

**Phase 3 — Risk and roadmap.** Build the executive risk register, prioritize identified
gaps, and produce the roadmap with owners, target dates, and budget ranges.

**Phase 4 — Governance operationalization.** Stand up the governance calendar and recurring
vCISO agenda. Deliver the draft IT ransomware tabletop scenario.

## Deliverables

Deliverables are taken from the client's requested list in `SRC-0002`. **Acceptance criteria
were not stated in any source**; the criteria below are Consultant-proposed and require client
confirmation before this SOW is issued (see `OQ-06`).

| ID | Deliverable | Description | Proposed Acceptance Criteria |
| --- | --- | --- | --- |
| D-1 | Kickoff summary and open question log | Written record of confirmed scope, stakeholders, reporting expectations, and outstanding information requests. | Delivered in writing following kickoff; client confirms scope boundary and stakeholder list are accurately stated. |
| D-2 | Current-state NIST CSF 2.0 profile | Current-state profile for the corporate IT environment across CSF 2.0 Functions and Categories, with basis noted for each rating. | Covers all six CSF 2.0 Functions for in-scope IT; each rating traceable to an interview, document, or stated limitation; client review comments addressed in one revision cycle. |
| D-3 | Executive risk register | Prioritized register of identified cyber risks in business terms, with impact, likelihood, and owner fields. | Each entry has an identified risk, business impact statement, and proposed owner; reviewed with the executive sponsor. |
| D-4 | Prioritized security roadmap | Sequenced improvement plan covering the next two quarters, with owners, target dates, and budget ranges. | Every roadmap item maps to at least one D-2 gap or D-3 risk; each item carries an owner, target date, and budget range; approved by the roadmap approver identified under `OQ-01`. |
| D-5 | Security governance calendar and vCISO agenda | Recurring governance meeting cadence and standing agenda structure. | Cadence, participants, and standing agenda documented and accepted by the Director of IT and executive sponsor. |
| D-6 | IT ransomware tabletop scenario (draft) | Draft incident response tabletop scenario for an IT ransomware event. | Scenario covers detection, containment, recovery, and communication phases for the in-scope IT environment; delivered in draft form. Facilitation of the exercise is not included unless separately agreed. |

## Client Responsibilities

Apex Precision will:

- Identify the roadmap approver and the executive decision path (`OQ-01`).
- Make the stakeholders below available for interviews and working sessions.
- Provide the following information, requested in `SRC-0002`:
  - Current network diagrams and site inventory.
  - Identity provider configuration summary.
  - Endpoint management and EDR coverage reports.
  - Vulnerability scan summary for IT assets.
  - Backup job status and restore test history.
  - Security awareness training completion report.
  - Incident response plan and recent incident records, if any.
  - Third-party list for critical IT and SaaS vendors.
- Review deliverables and return consolidated comments within an agreed review window
  (`OQ-07`).
- Notify the Consultant if any in-scope IT system stores or processes regulated data, CUI,
  or PII, which would change data handling under `DEC-0001`.

### Identified Stakeholders

From `SRC-0003` and `SRC-0002`:

| Name | Role | Engagement interest |
| --- | --- | --- |
| Maria Chen | CFO, executive sponsor | Risk visibility, budget prioritization, board reporting |
| Evan Brooks | Director of IT | Roadmap, program structure, operational maturity |
| Priya Nair | Infrastructure Manager | Network, endpoint, backup, vulnerability management |
| Carlos Medina | Service Desk Lead | Ticket trends, onboarding/offboarding, endpoint support |
| Renee Walker | HR Director | Joiner/mover/leaver process, security awareness |

## Consultant Responsibilities

The Consultant will:

- Provide vCISO advisory services covering the objectives and deliverables above.
- Conduct stakeholder interviews and documentation review for the in-scope IT environment.
- Maintain the engagement record — decisions, assumptions, open questions, and source
  provenance — in the engagement repository under `clients/test-client-1/`.
- Distinguish facts, assumptions, recommendations, and unresolved questions in all
  deliverables.
- Escalate scope changes through the change control process below rather than absorbing them
  silently.

## Assumptions

| ID | Assumption | Basis | Validation Needed |
| --- | --- | --- | --- |
| A-1 | No regulated data or CUI is in scope. | `SRC-0002`; `DEC-0001` in `../context/decisions.md` | Confirm with client before evidence collection begins. |
| A-2 | IT and OT networks are separable for assessment purposes. | Scope boundary in `SRC-0001`, `SRC-0002` | `SRC-0002` raises this as an open question: whether any IT systems are shared with OT networks in ways requiring separate review. |
| A-3 | The engagement is advisory; the Consultant recommends and does not implement. | Engagement type `advisory` in `engagement.yaml`; `DEC-0002` | Confirm the client does not expect remediation labor. |
| A-4 | Guest wireless is internet-only and logically separated from corporate IT networks. | `SRC-0001` network notes | Verify during discovery; stated in a synthetic diagram, not observed. |
| A-5 | The four-site SD-WAN topology in `SRC-0001` reflects the production environment. | `SRC-0001` | `SRC-0001` states it is synthetic and not based on discovery evidence. Must be replaced by real diagrams. |

## Dependencies

- Timely client provision of the information requests listed above.
- Stakeholder availability for interviews across all four sites.
- Consultant of record named and assigned (`OQ-02`).
- Access to system consoles or exported reports sufficient to corroborate interview
  statements.

## Evidence Handling

Per `DEC-0001` in `../context/decisions.md`, the consultant approved committing client
source documents to this Git repository on the basis that engagement material is `INTERNAL`
— not CUI and not regulated. Source material is cataloged with a `source_id`, SHA-256 hash,
classification, source type, original path, and ingestion timestamp in
`../sources/catalog.jsonl`.

This SOW draft is classified `CONFIDENTIAL`.

`DEC-0001` does not extend to secrets, credentials, tokens, private keys, CUI, or PII. If
discovery surfaces regulated data in the IT environment, evidence handling must be revisited
before ingestion, and this section must be amended by change order.

## Timeline

**Not contracted.** No start date, end date, phase durations, milestone dates, or term length
appear in any source. `SRC-0002` records a recommendation of an approximately four-week
discovery and baseline phase before roadmap commitments are published; that is a
recommendation, not a commitment.

Phase sequencing is defined under [Approach](#approach). Dates must be supplied by the
consultant and agreed with the client — see `OQ-04`.

## Fees And Commercial Terms

**Not stated.** No rates, fees, retainer structure, hour estimates, expense terms, invoicing
schedule, or payment terms appear in any source, and none have been drafted. See `OQ-03`.

## Legal Terms

**Not stated.** Confidentiality, intellectual property, limitation of liability, insurance,
indemnification, termination, and governing law provisions are not addressed in this draft
and are not derivable from repository sources. See `OQ-08`. This draft is not a contract and
must be reviewed by qualified counsel before issuance.

## Change Control

Material changes to scope, deliverables, timeline, or fees require a written change order
recorded in `clients/test-client-1/sow/` and a corresponding decision entry in
`../context/decisions.md`. Adding OT/ICS environments, technical security testing, or
remediation implementation to scope constitutes a material change.

## Acceptance

**Not defined.** Signature authority, acceptance mechanism, and deliverable sign-off process
are not stated in any source. See `OQ-05`. This draft has not been reviewed, approved,
issued, or executed.

## Open Questions

These must be resolved before this draft can be issued to a client. They are unresolved
inputs, not oversights in drafting.

| ID | Question | Source |
| --- | --- | --- |
| OQ-01 | Who approves the final security roadmap? | `SRC-0002` |
| OQ-02 | Who is the consultant of record and vCISO lead? `SRC-0002` lists "Consultant TBD". | `SRC-0002`, `engagement.yaml` |
| OQ-03 | What are the fees, rate structure, retainer model, hour estimates, and payment terms? | Not in any source |
| OQ-04 | What are the engagement start date, phase dates, milestone dates, and term length? | Not in any source |
| OQ-05 | What is the acceptance and signature process, and who holds signature authority? | Not in any source |
| OQ-06 | Do the proposed acceptance criteria in the deliverables table match client expectations? | Not in any source |
| OQ-07 | What deliverable review window applies? | Not in any source |
| OQ-08 | What legal terms apply — confidentiality, IP, liability, insurance, termination, governing law? | Not in any source |
| OQ-09 | What budget cycle should roadmap recommendations align to? | `SRC-0002` |
| OQ-10 | Are cyber insurance requirements available for review, and do they impose control obligations? | `SRC-0002` |
| OQ-11 | Which SaaS applications are business critical beyond ERP, CRM, and Microsoft 365? | `SRC-0002` |
| OQ-12 | Are any IT systems shared with OT networks in ways that require separate review? | `SRC-0002` |
| OQ-13 | Does Apex Precision have contractual cybersecurity obligations from large customers that would impose scope beyond NIST CSF 2.0? | `SRC-0002` |
| OQ-14 | Is the client of record "Apex Precision Components, Inc." or `test-client-1`? Workspace metadata and intake material disagree. | `client.yaml` vs `SRC-0003` |
| OQ-15 | Is tabletop facilitation expected in addition to the D-6 draft scenario? | Not in any source |

## Source Provenance

| Source ID | Artifact | Type | Status |
| --- | --- | --- | --- |
| `SRC-0001` | `../intake/it-network-diagram-four-site-manufacturing.md` | diagram | Synthetic. Not evidence. |
| `SRC-0002` | `../intake/kickoff-notes-nist-csf-vciso.md` | meeting-notes | Synthetic. Not evidence. |
| `SRC-0003` | `../intake/synthetic-client-profile.md` | meeting-notes | Synthetic. Not evidence. |

Catalog: `../sources/catalog.jsonl`.
