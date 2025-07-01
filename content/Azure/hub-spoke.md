---
title: "Azure Hub-Spoke Architecture & VNet Peering"
date: 2025-07-01
tags: ["Azure", "Networking", "Hub-Spoke", "VNet Peering"]
categories: ["Azure Networking"]
description: "Understand Hub-Spoke network architecture in Azure, how VNet peering works, and why it matters for enterprise design."
type: "Azure"
---

#### Azure Hub-Spoke Architecture

Once you understand VNets and Subnets, the next step is designing how they connect. One of the most **popular architectures** in Azure is called the **Hub-Spoke Model**.

#### What is the Hub-Spoke Model?

Think of the **Hub** as the central point where all shared services live — like a corporate office.

Each **Spoke** is a separate environment — like dev, test, or app workloads.


         +-----------------------+
         |      Hub VNet         |
         |  (Firewall, VPN, etc) |
         +-----------------------+
             /     |     \
            /      |      \
     +--------+ +--------+ +--------+
     | Spoke1 | | Spoke2 | | Spoke3 |
     +--------+ +--------+ +--------+



####  What is VNet Peering?

**VNet Peering** allows two VNets to communicate **privately** using Azure backbone (no internet).

#### Types of Peering:

- **Intra-region**: Same Azure region (fastest, lowest latency)
- **Global Peering**: Different regions (e.g., East US ↔ West Europe)

#### Key Facts:

- Fast (Azure backbone)
- Low-latency
- No public IPs required
- No extra hops — direct connection
- Resources can talk using **private IPs**

#### Peering Gotchas

- Peering is **not transitive**
  - If A ↔ B and B ↔ C, **A cannot talk to C**
- Need to **enable traffic flow** in both directions (if required)
- Watch out for overlapping IP address spaces — peering won't work

---

#### Why Use Hub-Spoke?

-  Centralized security (firewalls in hub)
-  Single VPN/ExpressRoute connection shared with all spokes
-  Simpler management of shared services like DNS, Bastion, etc.
-  Cost-effective: Share expensive appliances like firewalls across environments


#### Learn More

- [VNet Peering Overview](https://learn.microsoft.com/en-us/azure/virtual-network/virtual-network-peering-overview)
- [Hub-Spoke Reference Architecture](https://learn.microsoft.com/en-us/azure/architecture/reference-architectures/hybrid-networking/hub-spoke)

Next up: VPN Gateway vs ExpressRoute and when to use S2S or P2S connections!

**– Kasi @ [KasdevTech](https://kasdevtech.com)** or [LinkedIn](https://www.linkedin.com/in/kasi-suresh-992675177/)

- What’s Next?
Tomorrow's post can cover:
VPN Gateway vs ExpressRoute – S2S vs P2S
Routing in Azure – Route tables, UDR, BGP
