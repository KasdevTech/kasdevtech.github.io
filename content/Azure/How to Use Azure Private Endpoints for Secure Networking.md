---
title: "How to Use Azure Private Endpoints for Secure Networking"
date: 2025-06-23
author: "Kasi Suresh"
categories: [Azure, Networking, Security]
tags: [Azure Private Endpoint, Networking, Security, Azure Storage, DevSecOps]
description: "Learn how to use Azure Private Endpoints to securely access services like Azure Storage without exposing them to the public internet."
---

# 🔐 How to Use Azure Private Endpoints for Secure Networking

## 1️⃣ What is a Private Endpoint?

A **Private Endpoint** in Azure allows you to connect to Azure services (like Storage, SQL, CosmosDB, etc.) over a private IP inside your Azure Virtual Network (VNet), instead of using the public internet.

Think of it as a private IP address for an Azure service. This ensures:
✅ No traffic goes over the internet  
✅ Improved security (zero public exposure)  
✅ You can apply **NSG**, **firewall**, and **custom routing**  

---

## 2️⃣ When to Use Private Endpoints?

| Scenario                                    | Private Endpoint Recommended? |
|---------------------------------------------|-------------------------------|
| Critical data (PII, financial, healthcare)   | ✅ Yes                        |
| Internal line-of-business apps              | ✅ Yes                        |
| Public APIs serving global customers        | ❌ No — consider public endpoint |
| Hybrid network (on-premises + Azure)        | ✅ Yes                        |
| Regulatory/compliance (GDPR, HIPAA, PCI)    | ✅ Yes                        |

**Common Use Cases:**
- Azure Storage Account  
- Azure SQL Database  
- Azure Cosmos DB  
- Azure App Services (via Private Link)  
- Azure Key Vault  

---

## 3️⃣ Step-by-Step Example: Secure a Storage Account with Private Endpoint

### a) Prerequisites
- Azure Subscription  
- Existing Virtual Network (VNet)  
- Existing Storage Account  

---

### b) Architecture Diagram

+---------------------------+
| Azure VNet |
| +---------------------+ |
| | Subnet (10.0.1.0/24) | --> Private IP (e.g. 10.0.1.5) for Storage
| +---------------------+ |
+---------------------------+

Storage Account --[Private Endpoint]-- VNet
---

### c) Step 1: Create a Private Endpoint

#### CLI Example:

```bash
# Variables
RG_NAME="demo-rg"
VNET_NAME="demo-vnet"
SUBNET_NAME="demo-subnet"
STORAGE_NAME="mystorageaccountxyz"

# Create Private Endpoint
az network private-endpoint create \
  --resource-group $RG_NAME \
  --name pe-storage \
  --vnet-name $VNET_NAME \
  --subnet $SUBNET_NAME \
  --private-connection-resource-id $(az storage account show --name $STORAGE_NAME --query id -o tsv) \
  --group-id blob \
  --connection-name pe-conn-storage

d) Step 2: Create Private DNS Zone

az network private-dns zone create \
  --resource-group $RG_NAME \
  --name "privatelink.blob.core.windows.net"

# Link the DNS zone with your VNet
az network private-dns link vnet create \
  --resource-group $RG_NAME \
  --zone-name "privatelink.blob.core.windows.net" \
  --name "dns-link-storage" \
  --virtual-network $VNET_NAME \
  --registration-enabled false

# Add A record for Storage Account
az network private-dns record-set a create \
  --name $STORAGE_NAME \
  --zone-name "privatelink.blob.core.windows.net" \
  --resource-group $RG_NAME
Tip: Auto-managed if you use Azure Portal Private Link center.

e) Step 3: Restrict Public Network Access

az storage account update \
  --name $STORAGE_NAME \
  --resource-group $RG_NAME \
  --default-action Deny
Now, only traffic from the private endpoint in VNet is allowed! 🚀

4️⃣ Testing with Private IP Only
a) From VM inside VNet

# nslookup should resolve to private IP
nslookup mystorageaccountxyz.blob.core.windows.net

# Test connectivity
curl https://mystorageaccountxyz.blob.core.windows.net
b) From outside VNet (should fail)

# From your laptop or public IP
curl https://mystorageaccountxyz.blob.core.windows.net
# Expected: Access denied or timeout
5️⃣ Summary
✅ Private Endpoints help you securely access Azure services inside your VNet
✅ No public IP needed
✅ Great for internal, sensitive, or regulated workloads
✅ Works across Azure Storage, SQL, CosmosDB, Key Vault, App Services, and more