---
title: "Azure Routing Simplified – UDR, Route Tables & BGP"
date: 2025-07-02
tags: ["Azure", "Networking", "Route Table", "BGP", "UDR", "Routing"]
categories: ["Azure Networking"]
description: "Learn how Azure routes traffic inside virtual networks. Understand UDRs (User Defined Routes), System Routes, and BGP basics."
type: "Azure"
---

#### Azure Routing  – UDR, Route Tables, and BGP

Ever wonder how traffic knows where to go inside your VNet?
That magic is thanks to **Routing** – and in Azure, it’s handled by:

- System Routes
- User Defined Routes (UDR)
- Border Gateway Protocol (BGP)

#### System Routes (Default)
Azure **automatically adds system routes** to all subnets.

Examples:

| Destination       | Next Hop         |
|-------------------|------------------|
| 0.0.0.0/0         | Internet          |
| <VNet CIDR>       | Virtual Network   |
| 168.63.129.16     | Virtual Network   |

These work fine in most cases — **until you need customization**.



#### User Defined Routes (UDR)

UDRs are custom routes **you create** and assign to subnets via **Route Tables**.

#### Use Cases:
- Force traffic through a **firewall**
- Send all outbound traffic to a **NAT gateway**
- Isolate traffic between subnets

#### Example:

| Destination CIDR | Next Hop Type     | Next Hop IP    |
|------------------|-------------------|----------------|
| 0.0.0.0/0        | Virtual Appliance | 10.0.1.4       |
| 10.1.0.0/16      | Virtual Network   | —              |

>  “Virtual Appliance” = firewall, NVA, etc.

####  Route Table Basics

- You can create a **Route Table** in Azure
- Add **UDRs** (custom rules)
- Associate the table with **one or more subnets**

> Changes apply **immediately** once associated.


#### What is BGP?

BGP = Border Gateway Protocol

Used mostly with **ExpressRoute and VPN Gateway** to dynamically share routes between:

- On-premises
- Azure
- Peer networks

#### Benefits:
- Avoids manual route entries
- Learns new prefixes automatically
- Supports active-active gateways

> For most standard Azure VNets, **BGP is optional** — used in hybrid/enterprise setups.

#### Use `Effective Routes`

Want to see what routes apply to a VM?

1. Go to **VM > Networking > NIC > Effective Routes**
2. Azure shows a full list of all inherited + UDRs



#### Summary

| Route Type    | Use For                             |
|---------------|--------------------------------------|
| System Routes | Default routing in VNet              |
| UDR           | Custom control (firewalls, NAT, etc) |
| BGP           | Hybrid/ExpressRoute dynamic routing  |

---

#### Learn More

- [Overview of Routing](https://learn.microsoft.com/en-us/azure/virtual-network/virtual-networks-udr-overview)
- [BGP with ExpressRoute](https://learn.microsoft.com/en-us/azure/expressroute/expressroute-routing)

Next: NSG, ASG, and network security in Azure 

**– Kasi @ [KasdevTech](https://kasdevtech.com)** or [LinkedIn](https://www.linkedin.com/in/kasi-suresh-992675177/)
