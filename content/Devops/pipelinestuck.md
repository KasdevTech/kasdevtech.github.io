---
title: "Azure DevOps pipeline stuck on 'Initialize job' Step-by-step fix"
date: 2025-07-09
tags: ["Azure DevOps", "Pipelines", "Troubleshooting", "CI/CD", "Self-hosted agent"]
categories: ["Azure DevOps"]
description: "Fix Azure DevOps pipeline hangs at 'Initialize job' phase. Complete checklist with real root causes and fixes from production."
type: "DevOps"
---

#### Azure DevOps pipeline stuck on 'Initialize job'? Step-by-step fix

Ever had your Azure DevOps pipeline **hang at the very first step** – _Initialize job_ – and not move forward?

 This issue is frustrating and common — especially with **self-hosted agents**, permissions misconfiguration, or pipeline resource locks.

Let’s break down exactly how to troubleshoot and fix this problem step-by-step.



#### What does 'Initialize job' actually mean?

It’s the **very first phase** in a pipeline run:

- Validates the pipeline YAML
- Prepares agent + tools
- Downloads secure files/secrets
- Authenticates resources

If it hangs here — it means the pipeline **can’t reserve the agent or access required resources**.


#### Step-by-step Troubleshooting

#### Step 1: Check Agent Pool Status

- Go to `Project Settings` → `Agent Pools`
- Check if the **correct pool is selected**
- Ensure at least one **agent is online and idle**

If using **self-hosted agent**, ensure the agent service is running.

```bash
sudo systemctl status vsts.agent.[org].[agent-name].service
```

#### Step 2: Verify Agent Capabilities Match Job Demands
In the agent pool → Click on agent → Check Capabilities
Ensure it has required:
OS
dotnet/node versions
PowerShell/bash
If pipeline uses demands, ensure they’re met

#### Step 3: Check Organization + Project Access
Make sure the agent has access to the organization/project where the pipeline is running

For Microsoft-hosted agents, confirm your organization is not blocked or limited

#### Step 4: Check Job Authorization Scope
Go to Project Settings > Pipelines > Settings
Enable:
Limit job authorization scope to current project
This solves scope mismatch in many enterprise setups.

#### Step 5: Restart Agent / Remove Locks
Sometimes agents go stale or locked.
```
./svc.sh stop
./svc.sh uninstall
./config.sh remove
# Then reconfigure and start again
Or simply restart the VM/agent.
```
#### Step 6: Check YAML for Timeout or Infinite Loops
Make sure your pipeline YAML doesn't have:

```
jobs:
  - job: build
    timeoutInMinutes: 0 # ❌ will hang indefinitely

```
####  Step 7: Review Pipeline Permissions
Service connection permissions (Key Vault, Azure RM) may block pipeline setup
Check if the agent identity (e.g., Azure DevOps Service Principal) has access to:
Key Vault
Artifact feeds
Repos

