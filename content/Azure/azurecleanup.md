---
title: Automate Azure Cleanup — Before It Costs
description: Learn how to built a weekly automated Azure cleanup flow using PowerShell, Logic Apps, and Teams approvals to avoid surprise cloud bills.
date: 2025-07-28
author: Kasi Suresh
tags: [Azure, Automation, FinOps, PowerShell, LogicApps]
type: "Azure"
---

### Automate Azure Cleanup — Before It Costs Me

Most of us don’t realize how fast an Azure bill can grow — until we get that painful monthly invoice.

The surprise? It’s rarely because of production workloads.

It’s the small, forgotten things:
- Test VMs that should’ve been deleted  
- Staging App Services left running  
- Orphaned managed disks  
- Zombie NICs that no one even remembers creating  

These idle resources quietly drain money.

---

###  Solution: Weekly Automated Cleanup

Instead of manually checking everything, I built a simple system that does it all for me — safely and automatically.

Here’s what my setup includes:
- A **PowerShell script** that scans for unused resources
- An **Azure Logic App** that sends me an **approval request in Microsoft Teams**
- After approval, it deletes the resources
- Every action is logged to **Azure Storage** and **Log Analytics**



### Step-by-Step: How It Works

### Step 1: Detect Unused Resources with PowerShell

```powershell
# Find Unused Disks
$unusedDisks = Get-AzDisk | Where-Object { -not $_.ManagedBy }

# Find Zombie NICs
$zombieNICs = Get-AzNetworkInterface | Where-Object {
    -not $_.VirtualMachine -and $_.ProvisioningState -eq 'Succeeded'
}

# Save the list to JSON
$resources = [PSCustomObject]@{
    UnusedDisks = $unusedDisks.Id
    ZombieNICs  = $zombieNICs.Id
}
$resources | ConvertTo-Json -Depth 5 | Out-File "cleanupResources.json"
This script runs weekly on a schedule and saves the list of cleanup candidates.
``` 

### Step 2: Trigger a Logic App for Approval
I set up a Logic App that runs whenever the JSON file is uploaded to Blob Storage, or on a timer (e.g. every Sunday).

It reads the list and sends a message to Microsoft Teams using an Adaptive Card.

The card gives me the option to Approve or Reject the cleanup.

### Step 3: Delete Resources After Approval
If I approve the cleanup, the Logic App triggers an Azure Automation Runbook, which runs this PowerShell:

```

param (
    [string[]]$DiskIds,
    [string[]]$NICIds
)

foreach ($disk in $DiskIds) {
    Remove-AzDisk -ResourceId $disk -Force
    Write-Output "Deleted Disk: $disk"
}

foreach ($nic in $NICIds) {
    Remove-AzNetworkInterface -ResourceId $nic -Force
    Write-Output "Deleted NIC: $nic"
}
I’ve granted the automation account Managed Identity access so it can safely delete resources with the right permissions.
```
### Step 4: Log Everything
All deletion actions are logged to:

Azure Log Analytics Workspace for easy querying and alerts

Optionally to Azure Storage Table or a Blob for historical auditing

```
Write-Output "Deleted: $resourceId at $(Get-Date)"
```

Best Practice: Use Tags to Protect Critical Resources

- To avoid accidental deletes, I check for tags before including resources in the deletion list.

### Example:

- Only delete if AutoDelete = True
- Skip anything tagged with Environment = Production
- You can add this logic inside the detection PowerShell script.

### Why This Works
- This automation is simple but powerful.
- Avoid unexpected cost
- Keep my Azure environment clean
- Maintain an approval flow for transparency



### Final Take:
- Cleanup isn’t just a FinOps task — it’s hygiene.
- The longer you leave unused resources running, the more they cost you in silence.

So I automated it.
And I recommend you do the same.

Need help setting it up? Reach out to me — I’m happy to share the full setup.

**– Kasi @ [KasdevTech](https://kasdevtech.com)** or [LinkedIn](https://www.linkedin.com/in/kasi-suresh-992675177/)
