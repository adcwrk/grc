---
artifact_id: DIAG-test-client-1-IT-NETWORK-4SITE
artifact_type: diagram
client: "test-client-1"
status: synthetic
sensitivity: INTERNAL
created: "2026-08-14"
updated: "2026-08-14"
tags:
  - intake
  - synthetic
  - network-diagram
  - it-environment
---

# Synthetic IT Network Diagram: Four-Site Manufacturing Business

## Provenance

- Source type: AI-generated synthetic network diagram.
- Purpose: Fake intake diagram for an IT-only NIST CSF vCISO engagement.
- Evidence status: Not evidence. Do not use for formal assessment conclusions.
- Sensitivity: INTERNAL.

## Scope Boundary

This diagram represents the corporate IT environment only. OT/ICS, PLCs, HMIs,
SCADA, CNC controllers, plant-floor controls, and machine networks are explicitly
out of scope and are not represented as assessed assets.

```mermaid
flowchart TB
    Internet((Internet))
    SaaS[Cloud SaaS<br/>Microsoft 365<br/>NetSuite ERP<br/>Salesforce CRM<br/>ServiceNow ITSM]
    IdP[Microsoft Entra ID<br/>SSO and MFA]
    EDR[EDR Console<br/>CrowdStrike Falcon]
    Backup[Cloud Backup Repository<br/>Veeam Capacity Tier]

    Internet --- SDWAN[Managed SD-WAN Provider]
    Internet --- SaaS
    SaaS --- IdP
    EDR --- Internet
    Backup --- Internet

    subgraph HQ["Site 1 - Headquarters / Grand Rapids"]
        HQFW[Fortinet Firewall HA Pair]
        HQCore[Cisco Core Switch Stack]
        HQServers[VMware Cluster<br/>File, print, monitoring, backup server]
        HQUsers[Corporate Users VLAN]
        HQWiFi[Corporate Wi-Fi]
        HQGuest[Guest Wi-Fi]
        HQVPN[Remote Access VPN]

        HQFW --- HQCore
        HQCore --- HQServers
        HQCore --- HQUsers
        HQCore --- HQWiFi
        HQFW --- HQGuest
        HQFW --- HQVPN
    end

    subgraph PlantA["Site 2 - Main Plant / Dayton"]
        PAFW[Fortinet Firewall]
        PASwitch[Cisco Access Switches]
        PAUsers[Office and Warehouse Users VLAN]
        PAWiFi[Corporate Wi-Fi]
        PAGuest[Guest Wi-Fi]
        PAPrint[Print and Label Services]

        PAFW --- PASwitch
        PASwitch --- PAUsers
        PASwitch --- PAWiFi
        PAFW --- PAGuest
        PASwitch --- PAPrint
    end

    subgraph PlantB["Site 3 - Secondary Plant / Fort Wayne"]
        PBFW[Fortinet Firewall]
        PBSwitch[Cisco Access Switches]
        PBUsers[Office and Training Users VLAN]
        PBWiFi[Corporate Wi-Fi]
        PBGuest[Guest Wi-Fi]
        PBCache[Local File Cache]

        PBFW --- PBSwitch
        PBSwitch --- PBUsers
        PBSwitch --- PBWiFi
        PBFW --- PBGuest
        PBSwitch --- PBCache
    end

    subgraph DC["Site 4 - Distribution / Louisville"]
        DCFW[Fortinet Firewall]
        DCSwitch[Cisco Access Switches]
        DCUsers[Customer Service Users VLAN]
        DCShip[Shipping Workstations VLAN]
        DCWiFi[Corporate Wi-Fi]
        DCGuest[Guest Wi-Fi]

        DCFW --- DCSwitch
        DCSwitch --- DCUsers
        DCSwitch --- DCShip
        DCSwitch --- DCWiFi
        DCFW --- DCGuest
    end

    SDWAN --- HQFW
    SDWAN --- PAFW
    SDWAN --- PBFW
    SDWAN --- DCFW

    HQServers --- Backup
    HQUsers --- SaaS
    PAUsers --- SaaS
    PBUsers --- SaaS
    DCUsers --- SaaS
```

## Network Notes

- Each site has a Fortinet firewall and Cisco switching.
- Headquarters hosts remaining on-premises IT workloads.
- Remote access terminates at the headquarters firewall.
- Guest wireless is internet-only and logically separated from corporate IT networks.
- The managed SD-WAN connects the four corporate IT sites.
- SaaS applications are accessed over the internet and federated to Microsoft Entra ID.
- Endpoint security telemetry is managed through a cloud EDR console.

## Segments Shown

| Segment | Purpose | Sites |
| --- | --- | --- |
| Corporate users | Standard office and knowledge-worker endpoints | All sites |
| Warehouse and shipping users | IT-managed workstations for logistics workflows | Site 2, Site 4 |
| Corporate Wi-Fi | Managed wireless for company devices | All sites |
| Guest Wi-Fi | Internet-only visitor access | All sites |
| Server VLAN | On-premises IT workloads | Site 1 |
| Remote access VPN | IT-managed remote workforce access | Site 1 |

## Diagram Limitations

- This diagram is synthetic and not based on discovery evidence.
- IP addressing, firewall rules, routing details, and VLAN IDs are intentionally omitted.
- OT/ICS connectivity is not modeled and should not be inferred from this diagram.
