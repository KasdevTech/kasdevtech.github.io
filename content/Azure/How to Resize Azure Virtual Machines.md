---
title: "How to Resize Azure Virtual Machines"
date: 2025-06-23
draft: false
tags: ["azure", "vm", "resize", "cloud", "beginner-guide"]
categories: ["azure", "cloud"]
---

Resizing an Azure Virtual Machine (VM) allows you to adjust the size (CPU, Memory, Disk) of the VM as your application needs change — for cost optimization, performance scaling, or seasonal traffic.

In this guide, we’ll walk through **how to resize an Azure VM in 2025** using both the Azure Portal and CLI.

---

## Why Resize VMs?

- **Scale Up:** Handle more traffic or workload
- **Scale Down:** Reduce costs for low-traffic periods
- **Change Type:** Move to different series (ex: from DSv2 to B series for dev/test)

---

## Pre-requisites

✅ Azure Subscription  
✅ Owner / Contributor permissions on the VM  
✅ VM must be in a **Stopped (Deallocated)** state to resize

---

## Resize via Azure Portal

1️⃣ Navigate to **Virtual Machines**  
2️⃣ Select your VM  
3️⃣ Click **Size** under the "Settings" section  
4️⃣ Select a new size (you will see estimated cost/month)  
5️⃣ Click **Resize**

> If the current hardware cluster doesn’t support the target size, you must stop (deallocate) the VM first.

---

## Resize via Azure CLI

```bash
# Stop and deallocate the VM
az vm deallocate --resource-group myResourceGroup --name myVM

# Resize the VM (example: Standard_DS3_v2)
az vm resize --resource-group myResourceGroup --name myVM --size Standard_DS3_v2

# Start the VM
az vm start --resource-group myResourceGroup --name myVM
