---
title: AZ-104 — Manage Azure Storage and Compute Resources
description: Learn how to manage Azure Storage Accounts, Virtual Machines, and related compute resources in the AZ-104 Administrator certification path.
date: 2025-10-08
author: Kasi Suresh
tags: [Azure, AZ-104, Storage, Compute, VirtualMachines]
type: "Azure"
---

# AZ-104  — Manage Azure Storage and Compute Resources

Welcome to  of the AZ-104 series. In this blog, we’ll explore managing **Azure Storage Accounts** and **Compute Resources** including Virtual Machines (VMs). These are key skills tested in the certification exam.

---

## Part 1: Manage Azure Storage

Azure Storage provides scalable, secure, and durable storage for your data. The main types are Blob, File, Queue, and Table storage.

### 1. Create a Storage Account

```bash
az storage account create   --name kasdevstorage01   --resource-group demo-rg   --location eastus   --sku Standard_LRS
```

### 2. Configure Access Tiers

Access tiers help optimize costs based on data usage:
- Hot: Frequently accessed data
- Cool: Infrequently accessed data
- Archive: Rarely accessed data

```bash
az storage blob service-properties update   --account-name kasdevstorage01   --enable-change-feed true
```

### 3. Secure Storage with Shared Access Signature (SAS)

```bash
az storage account generate-sas   --account-name kasdevstorage01   --permissions rwdlac   --expiry 2025-12-31T23:59:00Z   --services b   --resource-types sco
```

### 4. Configure Azure Files with Identity-based Access

Enable Azure Files and authenticate using Azure AD.

```bash
az storage account update   --name kasdevstorage01   --enable-files-aadkerb true
```

---

## Part 2: Manage Azure Compute Resources

Azure compute provides on-demand scalable computing power through Virtual Machines (VMs) and related services.

### 1. Create a Virtual Machine

```bash
az vm create   --resource-group demo-rg   --name kasvm01   --image Ubuntu2204   --admin-username azureuser   --generate-ssh-keys
```

### 2. Manage VM Power States

```bash
# Start VM
az vm start --name kasvm01 --resource-group demo-rg

# Stop VM
az vm stop --name kasvm01 --resource-group demo-rg

# Deallocate VM
az vm deallocate --name kasvm01 --resource-group demo-rg
```

### 3. Attach and Manage Data Disks

```bash
az vm disk attach   --resource-group demo-rg   --vm-name kasvm01   --name kasdisk01   --new   --size-gb 50
```

### 4. Configure Availability Sets and Zones

- **Availability Sets**: Protect against hardware failures within a datacenter.
- **Availability Zones**: Protect against datacenter-level failures.

```bash
az vm availability-set create   --resource-group demo-rg   --name kas-avset   --platform-fault-domain-count 2   --platform-update-domain-count 2
```

---

## Part 3: Automation and Best Practices

### Automate with VM Extensions

```bash
az vm extension set   --publisher Microsoft.Azure.Extensions   --name CustomScript   --vm-name kasvm01   --resource-group demo-rg   --settings '{"fileUris": ["https://example.com/setup.sh"], "commandToExecute": "./setup.sh"}'
```

### Best Practices
- Use Managed Identities for secure access to resources
- Apply Tags for cost tracking and governance
- Regularly take Snapshots or use Azure Backup for recovery
- Use Availability Zones for production workloads

---

## Summary

| Component | Key Tasks |
|------------|------------|
| Storage | Create, secure, and configure tiers |
| Compute | Create, manage, and automate VMs |
| Governance | Apply tags, policies, and backups |

---

### Coming Next
Day 3 — Manage Azure Networking

We’ll cover:
- Virtual Networks and Subnets
- Network Security Groups
- Load Balancers and Application Gateways

---

**– Kasi @ [KasdevTech](https://kasdevtech.com)** or [LinkedIn](https://www.linkedin.com/in/kasi-suresh-992675177/)
