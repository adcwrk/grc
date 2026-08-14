---
artifact_id: SRCNOTE-test-client-1-SYNTH-PROFILE
artifact_type: source-note
client: "test-client-1"
status: synthetic
sensitivity: INTERNAL
created: "2026-08-14"
updated: "2026-08-14"
tags:
  - intake
  - synthetic
  - client-profile
---

# Synthetic Client Profile

## Provenance

- Source type: AI-generated synthetic intake material.
- Purpose: Fake client context for testing a NIST CSF vCISO engagement workflow.
- Evidence status: Not evidence. Do not use for formal assessment conclusions.
- Sensitivity: INTERNAL.

## Organization

- Legal name: Apex Precision Components, Inc.
- Common name: Apex Precision.
- Industry: Discrete manufacturing.
- Company size: Medium business.
- Workforce: Approximately 640 employees.
- IT users: Approximately 520 active workforce identities.
- Operating model: Four-site manufacturing and distribution business.
- Engagement scope requested: IT environment only.

## Sites

| Site | Location | Business role | Approximate headcount | IT notes |
| --- | --- | --- | --- | --- |
| Site 1 | Grand Rapids, Michigan | Headquarters, finance, HR, engineering leadership | 180 | Primary data room, core WAN edge, Microsoft 365 administration |
| Site 2 | Dayton, Ohio | Main manufacturing plant | 240 | Local IDF closets, user VLANs, warehouse Wi-Fi, print services |
| Site 3 | Fort Wayne, Indiana | Secondary manufacturing plant | 150 | Local file cache, user VLANs, shared training room systems |
| Site 4 | Louisville, Kentucky | Distribution and customer service office | 70 | Shipping workstations, customer service users, guest Wi-Fi |

## Business Context

Apex Precision manufactures machined components for industrial equipment makers.
The company operates normal business IT services centrally while each site has
local network infrastructure for office, warehouse, and production-support users.

## IT Environment In Scope

- Identity and access management for workforce users.
- Microsoft 365 tenant and related SaaS administration.
- Corporate endpoint fleet, including laptops, office desktops, and shared workstations.
- Site LAN, WAN, wireless, firewalls, VPN, DNS, DHCP, and network monitoring.
- IT service desk, asset management, endpoint protection, vulnerability management, and backup administration.
- Business applications used by finance, HR, sales, customer service, engineering office staff, and warehouse users.

## Explicitly Out Of Scope

- Operational technology, industrial control systems, PLCs, HMIs, SCADA, CNC controllers, and plant-floor automation networks.
- Safety systems, quality instrumentation networks, and machine telemetry platforms.
- Physical security systems except where they depend on corporate identity or network services.
- Formal certification, attestation, or regulatory audit conclusions.

## Synthetic Key Contacts

| Name | Role | Engagement interest |
| --- | --- | --- |
| Maria Chen | CFO and executive sponsor | Risk visibility, budget prioritization, board reporting |
| Evan Brooks | Director of IT | Roadmap, security program structure, operational maturity |
| Priya Nair | Infrastructure Manager | Network, endpoint, backup, and vulnerability management |
| Carlos Medina | Service Desk Lead | Ticket trends, onboarding/offboarding, endpoint support |
| Renee Walker | HR Director | Joiner/mover/leaver process and security awareness |

## Known IT Systems

- Microsoft Entra ID for identity.
- Microsoft 365 for email, collaboration, and office productivity.
- Intune for endpoint management.
- CrowdStrike Falcon for endpoint detection and response.
- Fortinet firewalls at each site.
- Cisco switching and wireless at all sites.
- VMware cluster at headquarters for remaining on-premises business services.
- Veeam backup for on-premises workloads.
- NetSuite ERP.
- Salesforce CRM.
- ServiceNow ITSM.
- KnowBe4 security awareness training.

## Initial vCISO Focus Areas

- Establish governance cadence, risk register ownership, and security roadmap.
- Baseline current cybersecurity program against NIST CSF 2.0.
- Validate identity, endpoint, backup, vulnerability, incident response, and third-party risk practices.
- Define pragmatic improvement plan for the next two quarters.
