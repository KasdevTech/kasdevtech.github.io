---
title: "How to Create a Self-Hosted Azure DevOps Agent using Azure Virtual Machine Scale Sets"
date: 2025-06-25
author: "Kasi Suresh"
categories: [Azure DevOps, CI/CD, Infrastructure]
tags: [Azure DevOps, VMSS, Self-Hosted Agent, Scale Set, Pipeline]
description: "Step-by-step guide to setting up a self-hosted Azure DevOps agent pool using Azure Virtual Machine Scale Sets (VMSS) with scaling, screenshots, and security best practices."
type: "DevOps"
---
Setting up self-hosted agents using **Azure Virtual Machine Scale Sets (VMSS)** gives you more **control, performance, and scalability** compared to Microsoft-hosted agents.

>  This guide includes detailed setup steps, CLI commands, and screenshots from the Azure Portal.

---
###  Use Cases for Self-Hosted Agents
- Large builds requiring more compute
- Custom toolchains (e.g., Docker, Terraform, Node.js)
- Controlled access with internal networking
- Reducing build time and cost
---

###  Prerequisites
- Azure DevOps Organization + Project
- Azure Subscription
- Contributor or Owner role on Azure
- VMSS Contributor role for DevOps managed identity

---

####  Step 1: Create a Virtual Machine Scale Set (VMSS)

You can create this via **Azure CLI** or **Portal**. Below are the CLI steps:

```bash
###  Create Resource Group
az group create --name devops-agents-rg --location eastus

 Create VM Scale Set
---------------------
az vmss create \
  --resource-group devops-agents-rg \
  --name devops-vmss \
  --image UbuntuLTS \
  --upgrade-policy-mode automatic \
  --admin-username azureuser \
  --generate-ssh-keys \
  --instance-count 1
```
#### Step 2: Create a Managed Identity for Azure DevOps
```
This identity allows Azure DevOps to access and manage the VMSS.
az identity create --name devops-agent-identity --resource-group devops-agents-rg

Get the clientId:
az identity show --name devops-agent-identity --resource-group devops-agents-rg --query clientId
```
####  Step 3: Assign Roles to the Managed Identity
```
Assign the Virtual Machine Contributor role to this identity on the VMSS:
az role assignment create \
  --assignee <CLIENT_ID> \
  --role "Virtual Machine Contributor" \
  --scope /subscriptions/<SUBSCRIPTION_ID>/resourceGroups/devops-agents-rg/providers/Microsoft.Compute/virtualMachineScaleSets/devops-vmss
```
####  Step 4: Register VMSS with Azure DevOps as Agent Pool
```
In Azure DevOps:
Go to Project Settings > Agent Pools
Click Add pool > Azure Virtual Machine Scale Set
Provide:
Name: vmss-agent-pool
Subscription
Resource Group: devops-agents-rg
VMSS Name: devops-vmss
Managed Identity
```

#### Step 5: Use the Agent Pool in Your Pipeline
```
pool:
  name: 'vmss-agent-pool'

steps:
- script: echo "Running build on VMSS agent"
```

####  Step 6: Optional - Enable Auto-Scaling Rules
```
You can configure auto-scaling on the VMSS via:
az monitor autoscale create \
  --resource-group devops-agents-rg \
  --resource devops-vmss \
  --resource-type Microsoft.Compute/virtualMachineScaleSets \
  --name vmss-autoscale \
  --min-count 1 --max-count 5 --count 1
```
####  Security Best Practices
- Use private networking (e.g., VNet + NSG)
- Harden VM image (disable password login, use private artifacts)
- Monitor agent health with Azure Monitor
- Periodically update VM images (golden images or packer)

###  Conclusion
Azure VMSS-backed DevOps agents give you flexibility, security, and scale. With VMSS integration, you no longer need to manually install or configure agents on VMs — Azure DevOps handles it!

