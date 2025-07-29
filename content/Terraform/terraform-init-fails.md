
---
title: "Terraform Init Fails in CI/CD — Fixed Remote Backend & Auth Issues"
date: 2025-07-29
author: "Kasi Suresh"
tags: ["Terraform", "Azure", "CI/CD", "Remote Backend", "Troubleshooting"]
summary: "Terraform init sometimes fails in CI/CD pipelines when authenticating to remote backend. Here's how I fixed it using service principal and storage configuration updates."
---

> Error:
>
> ```
> Error loading state: Error retrieving keys from storage account
> ```

---
#### The Problem

In a GitHub Actions pipeline, `terraform init` failed when trying to initialize the remote backend pointing to an Azure Storage Account.



#### Root Causes

- Missing or incorrect authentication to Azure
- Backend block has invalid `resource_group_name`, `container_name`, or `storage_account_name`
- Identity used by pipeline doesn’t have **Storage Blob Data Contributor**



#### Step-by-Step Fix

####  Step 1: Validate `backend` Configuration

```hcl
terraform {
  backend "azurerm" {
    resource_group_name  = "tf-rg"
    storage_account_name = "kasdevtfstate"
    container_name       = "tfstate"
    key                  = "prod.terraform.tfstate"
  }
}
```
Make sure all values are correct and exist in Azure.

#### Step 2: Check the Identity Used in CI/CD
If using GitHub Actions with OIDC:
Check the federated credential mapping in Azure AD
Ensure client_id, tenant_id, and subscription_id are correctly exported

#### Step 3: Assign Storage Role
Use this command to allow Terraform to read/write state:

```
az role assignment create \
  --assignee <client_id> \
  --role "Storage Blob Data Contributor" \
  --scope "/subscriptions/<subId>/resourceGroups/tf-rg/providers/Microsoft.Storage/storageAccounts/kasdevtfstate"

  ```
#### Step 4: Re-run terraform init
In GitHub Actions:

```
- name: Terraform Init
  run: terraform init
  env:
    ARM_CLIENT_ID: ${{ secrets.AZURE_CLIENT_ID }}
    ARM_SUBSCRIPTION_ID: ${{ secrets.AZURE_SUBSCRIPTION_ID }}
    ARM_TENANT_ID: ${{ secrets.AZURE_TENANT_ID }}

```    
#### Tips to be consider
Ensure container_name exists before init
Avoid manual storage account creation—automate it using CLI or Terraform
Use -reconfigure in terraform init if backend config changes

#### Conclusion
Terraform init failures in CI/CD are usually tied to remote backend or identity misconfigurations. Validating backend values and assigning correct RBAC permissions solves 95% of the cases.

**– Kasi @ [KasdevTech](https://kasdevtech.com)** or [LinkedIn](https://www.linkedin.com/in/kasi-suresh-992675177/)


