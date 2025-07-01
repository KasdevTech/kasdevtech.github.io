---
title: " Azure Virtual Network Basics – Public vs Private Networks"
date: 2025-07-01
tags: ["Azure", "Networking", "VNet", "Cloud Basics"]
categories: ["Azure Networking"]
description: "Understand the basics of Azure Virtual Networks, what public and private networks mean in the cloud, and how IPs work in Azure."
type: "Azure"
---

#### Azure Virtual Network Basics – Public vs Private
If you're getting started with Azure Networking, the first concept you must master is the **Virtual Network** (aka VNet). This is the **foundation** of all networking in Azure.

#### What is a VNet?
A **Virtual Network (VNet)** in Azure is like your private data center network in the cloud. It allows Azure resources (like VMs, App Services, etc.) to **communicate with each other securely**.
Think of it like a virtual version of a LAN (Local Area Network).


#### Public vs Private Networking

#### Private Network
- Resources inside a VNet **don’t have internet access by default**.
- Private IPs like `10.x.x.x`, `172.16.x.x`, or `192.168.x.x`
- Used for internal apps, databases, backend services

#### Public Network

- When you assign a **Public IP** to a VM or Load Balancer
- Accessible from the internet
- Needs **NSGs** and firewalls for protection

####  IP Addressing in Azure

When you create a VNet, you define an IP **address space** (CIDR block):

Example:
- VNet CIDR: `10.0.0.0/16` → gives you 65,536 IPs
- Subnet A: `10.0.1.0/24`
- Subnet B: `10.0.2.0/24`

Azure reserves **5 IPs per subnet** (first 4 + last 1) — plan your space accordingly.

#### Internet Access

- **Outbound**: By default, VMs **can access the internet** for updates, downloads.
- **Inbound**: You must assign a **Public IP** or use a **Load Balancer** for external access.



#### Tip

 Just because your VM has internet access, doesn’t mean it’s public. Internet **outbound** is default; **inbound** needs explicit public IP and NSG rule.


#### Learn More

- [Azure Virtual Network Overview](https://learn.microsoft.com/en-us/azure/virtual-network/virtual-networks-overview)

Next up: Hub-Spoke and VNet Peering!

**– Kasi @ [KasdevTech](https://kasdevtech.com)** or [LinkedIn](https://www.linkedin.com/in/kasi-suresh-992675177/)
