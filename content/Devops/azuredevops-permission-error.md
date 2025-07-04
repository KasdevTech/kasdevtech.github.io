---
title: "Fixing 'Permission Denied' Errors While Deploying from Azure Pipelines to Azure Resources"
date: 2025-07-04
categories: [Azure DevOps, CI/CD]
tags: [RBAC, Service Principal, Azure Pipelines, ARM Permissions]
type: "DevOps"
---

Deploying resources from Azure Pipelines and running into the dreaded `AuthorizationFailed` error? You’re not alone!

Error: AuthorizationFailed: The client does not have authorization to perform action 'Microsoft.Web/sites/write'...

####  Root Cause

This error usually occurs because the **service principal** used in your Azure DevOps **service connection** does not have the required **role-based access control (RBAC)** permissions on the target resource group or subscription.

#### Step-by-Step Fix

####  Verify the Service Connection Identity

- Go to `Project Settings` → `Service Connections`
- Click on your Azure Resource Manager connection
- Note the **Object ID** of the service principal

#### Assign the Correct Role in Azure Portal

- Navigate to your **Resource Group** (or Subscription)
- Go to `Access Control (IAM)` → `Add Role Assignment`
- Select the role (e.g., `Contributor` or `Web App Contributor`)
- Assign it to the **service principal**

#### Review Pipeline YAML

Make sure you're referencing the correct service connection:

```yaml
- task: AzureWebApp@1
  inputs:
    azureSubscription: 'MyServiceConnection'
    appName: 'mywebapp'
    package: '$(System.DefaultWorkingDirectory)/drop.zip'
``` 
#### Least Privilege Principle
Avoid assigning Owner or broad Contributor roles at subscription level—use custom roles or resource-level assignments for better governance.

#### Conclusion
With proper RBAC and service connection scope, your pipeline will deploy seamlessly without permission errors.

