---
title: "Terraform Import in Azure — Fixing Out-of-Band Changes"
date: 2025-09-01
author: "Kasi Suresh"
tags: ["Terraform", "Azure", "State", "Troubleshooting"]
summary: "Sometimes resources created manually in the Azure Portal need to be managed by Terraform. Here's how I used `terraform import` to fix drift and sync state."
---

> ❌ Error:
>
> ```
> Error: A resource with the ID already exists - to be managed via Terraform this resource needs to be imported into the State
> ```

#### The Problem

Someone created a **Storage Account** manually in the Azure Portal.  
When I tried to deploy Terraform, it failed because the resource already existed.



#### Solution — Using `terraform import`

#### Step 1: Define the Resource in Code

```hcl
resource "azurerm_storage_account" "example" {
  name                     = "kasdevstorage01"
  resource_group_name      = azurerm_resource_group.rg.name
  location                 = azurerm_resource_group.rg.location
  account_tier             = "Standard"
  account_replication_type = "LRS"
}
```
#### Step 2: Import the Existing Resource

```
terraform import azurerm_storage_account.example \
  /subscriptions/<subId>/resourceGroups/<rgName>/providers/Microsoft.Storage/storageAccounts/kasdevstorage01
  ```

#### Step 3: Run Plan
```
terraform plan
Terraform now recognizes the resource as managed.
```
#### Notes:
- Always define the resource exactly as it exists in Azure.
- Use terraform state show <resource> after import to confirm values.
- Use imports to bring drifted or manually created resources back under Terraform.


**– Kasi @ [KasdevTech](https://kasdevtech.com)** or [LinkedIn](https://www.linkedin.com/in/kasi-suresh-992675177/)


