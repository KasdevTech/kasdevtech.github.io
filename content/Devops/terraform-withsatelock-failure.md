---
title: "Terraform Fails with State Lock Error in Azure DevOps Pipeline"
date: 2025-07-07
categories: [Azure DevOps, Terraform, IaC]
tags: [Terraform, State Lock, CI/CD, Azure Storage]
type: "DevOps"
---

If you're running Terraform in Azure DevOps and see this:

Error: Error acquiring the state lock: state blob is already locked

You're facing a **Terraform state lock** issue — and it can block your pipeline!

#### What Causes It?

- A previous run crashed or was canceled
- Two pipelines tried to modify state simultaneously
- State is locked but not released due to network timeout

#### Step-by-Step Fix

####  Manually Unlock State

Use this command from your local machine (or DevOps pipeline):

```bash
terraform force-unlock <LOCK_ID>

To get the lock ID, run:
terraform show -no-color
```

####  Use lock and retry Settings
Set retry logic in your pipeline:
- script: terraform init -backend-config="..." -lock=true -lock-timeout=120s
####  Serial Execution
Avoid running two pipelines on the same state file by adding a check-in-progress step or resource lock mechanism using environment gates or manual approvals.

####  Conclusion
State lock errors are common, but avoidable. Use serial workflows and unlock cautiously to prevent state corruption.

