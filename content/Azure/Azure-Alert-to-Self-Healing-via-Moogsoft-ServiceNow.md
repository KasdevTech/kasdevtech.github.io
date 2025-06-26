---
title: "End-to-End Incident Automation: Azure Alert to Self-Healing via Moogsoft & ServiceNow"
date: 2025-06-25
author: "Kasi Suresh"
categories: [Azure, Automation, AIOps, DevOps]
tags: [Azure Monitor, Moogsoft, ServiceNow, Automation, Logic Apps, Runbook, Self-Healing]
description: "How I automated disk space alert remediation using Azure Alerts, Moogsoft, and ServiceNow — before it even reaches L1 support."
type: "Azure"
---
In one of my recent automation projects, I came across a real-time scenario:  
An Azure VM's **C:\ drive crosses 80% usage**, and boom — the alert triggers, gets routed to **Moogsoft**, and creates an incident in **ServiceNow**.  
But before it even hits the L1 queue, I wanted to give automation a shot.

Why assign disk cleanup to an engineer when a bot can do it better — and faster?
---
####  Real Scenario

Here’s what happens traditionally:

- Azure Monitor Alert: C:\ > 80%
- Moogsoft receives the alert
- Moogsoft creates an incident in ServiceNow
- L1 team gets it assigned (and starts with “clearing temp files”)

Let’s not wait till that point.

I wanted to **trigger an automated workflow** before the incident reaches L1. So we created an **Automation Assignment Group** in SNOW — all disk space alerts land here first.

---

####  What I Did – The Flow

```text
Azure Alert (C:\ > 80%) 
   ↓
Action Group → Logic App (or Webhook)
   ↓
Moogsoft receives and correlates
   ↓
Incident Created in ServiceNow → Assigned to "Automation-Bot" group
   ↓
Azure Automation Runbook kicks in
   ↓
1. Cleanup temp & log files
2. Recheck space
   ↓
→ If resolved: Close incident in SNOW
→ Else: Escalate to L1 with full logs & diagnostics
```
####  What the Runbook Does
Here’s the high-level logic in my Azure Automation Runbook (PowerShell-based):

```
$drive = Get-WmiObject Win32_LogicalDisk -Filter "DeviceID='C:'"
$percentFree = ($drive.FreeSpace / $drive.Size) * 100

if ($percentFree -lt 20) {
    Write-Output "Low space: $percentFree%. Starting cleanup..."
    
    # Clear temp files
    Remove-Item -Path "C:\Windows\Temp\*" -Recurse -Force -ErrorAction SilentlyContinue
    Remove-Item -Path "C:\Users\*\AppData\Local\Temp\*" -Recurse -Force -ErrorAction SilentlyContinue
    
    Start-Sleep -Seconds 30
    
    # Re-check
    $drive = Get-WmiObject Win32_LogicalDisk -Filter "DeviceID='C:'"
    $percentFree = ($drive.FreeSpace / $drive.Size) * 100
    
    if ($percentFree -gt 20) {
        Write-Output "Cleanup successful: $percentFree%. Closing incident."
        # Call SNOW API → Resolve incident
    } else {
        Write-Output "Still low space. Escalating to L1."
        # Call SNOW API → Update work notes and reassign
    }
} else {
    Write-Output "Disk space looks fine. No action taken."
}

```
####  Integration Points
Here’s where everything ties together:

- Component	         Role
- Azure Monitor	 Detect disk threshold breach
- Action Group	    Triggers Logic App or webhook
- Moogsoft	       Event correlation, dedupe
- ServiceNow	    Creates incident
- Azure Runbook	 Performs cleanup + resolution
- SNOW REST API	 Auto-close or reassign with logs

####  Optional Add-Ons (Next Steps)
- Runbook Scheduling: Run daily checks on all servers.
- AI Insights: Use historical patterns to decide cleanup thresholds.
- Self-Healing Summary Dashboard: How many incidents were fixed without L1?

#### Final Thoughts
- This is how I turned a simple disk space alert into a self-healing workflow.
- It saved our L1 team 15–20 incidents per week (no kidding), and gave me full control to inject intelligence and automation right at the start of the alert pipeline.
- Let me know if you’re building similar automation — I’d love to share ideas or show you how I did the SNOW integration in detail.

Until next time — keep automating 
– Kasi Suresh | @KasdevTech