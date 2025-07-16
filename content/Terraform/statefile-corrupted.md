---
title: "Terraform State Corruption in Azure — Recovered"
date: 2025-07-16
author: "Kasi Suresh"
tags: ["Terraform", "Azure", "Troubleshooting"]
summary: "Faced a corrupted Terraform state file in Azure Blob Storage? Here's a real-world recovery guide to restore infrastructure state safely in 4 simple steps."
type: "Terraform"
---

#### Encountered this error?

```
Error: state snapshot was corrupt
```

#### The Problem

During a large-scale Azure deployment using remote state in Azure Blob Storage, a `terraform apply` was interrupted. The result: a corrupted `terraform.tfstate`.



#### Symptoms

- `terraform plan` or `terraform apply` fails immediately.
- `terraform state pull` shows unreadable or broken JSON.
- Azure CLI blob shows latest version is malformed.


#### Fix — Step-by-Step

#### Backup the Current (Corrupted) State

```bash
az storage blob download \
  --container-name tfstate \
  --name terraform.tfstate \
  --file backup-corrupt.tfstate \
  --account-name <storage_account>

 ```

#### List Older Versions (Versioning Must Be Enabled)
```
az storage blob list-versions \
  --container-name tfstate \
  --name terraform.tfstate

```  
#### Download a Working Version
```
az storage blob download \
  --container-name tfstate \
  --name terraform.tfstate \
  --version-id <valid_version_id> \
  --file terraform.tfstate

  ```
#### Restore the Good State
```
az storage blob upload \
  --container-name tfstate \
  --name terraform.tfstate \
  --file terraform.tfstate \
  --account-name <storage_account> \
  --overwrite

  ```
#### Verification
```
terraform init
terraform plan
```

- Always enable blob versioning in your backend container.
- Use terraform state pull > backup.json as a safety net in CI/CD.
- Consider switching to state locking with azurerm backend or use tools like Terragrunt.


