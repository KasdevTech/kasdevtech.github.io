---
title: " Azure NSG vs ASG – Network Security for VNets "
date: 2025-07-03
tags: ["Azure", "Networking", "NSG", "ASG", "Security"]
categories: ["Azure Networking"]
description: "Understand Network Security Groups (NSG) and Application Security Groups (ASG) in Azure. Learn how they protect your VNets and workloads."
type: "Azure"
---

#### Azure NSG vs ASG

In cloud networking, **firewalls and access control** are your first line of defense.  
In Azure, the two main tools for this are:

-  **Network Security Group (NSG)**
-  **Application Security Group (ASG)**

Let’s explore what they are, how they work, and how to use them together.


#### What is a Network Security Group (NSG)?

An **NSG** acts like a virtual firewall. You can apply it to:

- Subnets  
- Network interfaces (NICs)

#### NSG Rules look like:

| Priority | Direction | Source | Destination | Port | Action |
|----------|-----------|--------|-------------|------|--------|
| 100      | Inbound   | Any    | 10.0.1.4     | 80   | Allow  |
| 200      | Inbound   | Any    | Any         | *    | Deny   |

Azure processes rules **top-down**, based on **priority** (lower = higher priority).


#### How NSGs Work

- You can associate an NSG to:
  - A **subnet** → all resources in that subnet
  - A **NIC** → specific VM or resource
- Rules are **stateful** — response traffic is allowed automatically.

#### What is an Application Security Group (ASG)?

**ASGs** are **labels** or **tags** that group VMs logically. Think of them like virtual "security groups" for workloads.

You use ASGs **inside NSG rules** to simplify targeting.

#### Example:

| Rule | Source ASG | Destination ASG | Port | Action |
|------|------------|------------------|------|--------|
| 100  | `web-servers` | `db-servers`   | 1433 | Allow  |

ASG lets you manage security at **scale** without tracking IPs.


#### NSG vs ASG: What's the Difference?

| Feature              | NSG                              | ASG                                 |
|----------------------|----------------------------------|-------------------------------------|
| Type                 | Firewall                         | Logical group/tag                   |
| Applies to           | Subnets, NICs                    | Only used **inside NSG rules**      |
| Manages              | Access rules                     | Targets inside NSG rules            |
| Example              | Allow port 80 to 10.0.1.4        | Allow traffic to `web-servers` ASG  |



#### Best Practices

- Use NSGs for all subnets — even private ones
- Use ASGs to group workloads (e.g., web-tier, db-tier)
- Don’t use public IPs in rules — use ASGs or service tags
- Always **deny all** at end unless explicitly required



#### Learn More

- [Network Security Groups Overview](https://learn.microsoft.com/en-us/azure/virtual-network/network-security-groups-overview)
- [Application Security Groups](https://learn.microsoft.com/en-us/azure/virtual-network/application-security-groups)

Next: Azure Firewall, DDoS Protection, and network security design patterns 

**– Kasi @ [KasdevTech](https://kasdevtech.com)** or [LinkedIn](https://www.linkedin.com/in/kasi-suresh-992675177/)
