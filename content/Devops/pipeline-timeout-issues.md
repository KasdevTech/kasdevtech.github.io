
---
title: "Azure DevOps Pipeline Timeout – Fixing Long-Running Build Failures"
date: 2025-07-05
categories: [Azure DevOps, Pipelines]
tags: [Build Timeout, CI/CD, Troubleshooting, Hosted Agent]
type: "DevOps"
---

Does your build or deployment fail after 60 minutes? You might be hitting a **default timeout** on Azure Pipelines.

#### Error Message
[error]The job was canceled after reaching the timeout limit of 60 minutes.

#### Default Limits

- **Microsoft-hosted agents**: 60 minutes per job (can be increased)
- **Self-hosted agents**: You control the timeout

#### Increase Timeout in YAML

Add the `timeoutInMinutes` setting to your job:

```yaml
jobs:
- job: Build
  timeoutInMinutes: 120
  pool:
    vmImage: 'ubuntu-latest'
  steps:
    - script: echo "Building..."
```

#### Optimize the Build
- Avoid long dependency installations (e.g., move to cache or Docker layer)
- Parallelize jobs using strategy and matrix
- Use restoreCache and saveCache for npm, pip, Maven, etc.

#### Use Self-Hosted Agent (No Hard Timeout)
Set up a self-hosted agent in Azure VM or AKS to avoid limits altogether.

#### Monitor:
To monitor how long each task takes, turn on detailed logs in Pipeline settings → Diagnostics → Enable system diagnostics.

#### Conclusion
Timeouts are easy to miss until they break your CI/CD. Either extend timeouts or move to optimized or self-hosted agents.