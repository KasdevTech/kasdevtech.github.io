---
title: "Fixing 'az login' Authentication Failures in IaC Pipelines"
date: 2025-07-07
categories: [Azure DevOps, IaC, Bicep, Terraform]
tags: [Azure CLI, az login, Service Connection, DevOps Pipeline]
type: "DevOps"
---

You added an `az login` command to your pipeline… and now the pipeline fails?

ERROR: Please run 'az login' to setup account

#### Root Cause

The Azure CLI needs credentials to authenticate. When run in a pipeline, `az login` needs to be done **non-interactively** using a **service principal**.

#### Solution: Use Service Principal with Secrets

Add a login step like this in your YAML:

```yaml
- script: |
    az login --service-principal \
             --username $appId \
             --password $clientSecret \
             --tenant $tenantId
  env:
    appId: $(azureAppId)
    clientSecret: $(azureClientSecret)
    tenantId: $(azureTenantId)
Then store these as secrets in Pipeline → Library → Secure files or variable groups.
```

#### Use AzureCLI@2 Task Instead
```
- task: AzureCLI@2
  inputs:
    azureSubscription: 'MyServiceConnection'
    scriptType: bash
    scriptLocation: inlineScript
    inlineScript: |
      az account show
This auto-authenticates using the linked service connection.
```
#### Conclusion
Use the right login method for your IaC tools. For Terraform or Bicep, the AzureCLI@2 task is the safest, most DevOps-friendly approach.