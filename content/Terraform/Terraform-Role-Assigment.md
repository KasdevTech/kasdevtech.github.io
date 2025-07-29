---
title: "Terraform Role Assignment Fails on Azure — Fixed with Correct RBAC & Automation"
date: 2025-07-29
author: "Kasi Suresh"
tags: ["Terraform", "Azure", "RBAC", "Permissions", "Troubleshooting"]
summary: "Terraform often fails when assigning roles in Azure due to RBAC permission issues. Here's how I fixed this in a CI/CD pipeline using the right roles and automation."
type: "Terraform"
---

>  Error:
>
> ```
> Error: creating Role Assignment: authorization.RoleAssignmentsClient#Create: Failure sending request
> ```



#### The Problem

During `terraform apply`, the deployment failed when trying to create a `azurerm_role_assignment` resource.

The error indicated **insufficient permissions**, even though the identity had Contributor access.



#### Why It Happens

In Azure, `Contributor` role **cannot assign roles**.

You need **Microsoft.Authorization/roleAssignments/write** permission, which is only available in roles like:

- **User Access Administrator**
- **Owner**
- **Custom Role** with that permission



#### Step-by-Step Fix

#### Step 1: Identify the Identity Terraform Uses

If using a pipeline, it's usually:

- A **Managed Identity**
- A **Federated Identity** (OIDC/GitHub Actions)

Make sure this identity has **User Access Administrator** or custom role that includes:

```json
"Microsoft.Authorization/roleAssignments/write"
```
#### Step 2: Grant the Required Role at Scope
Use Azure CLI:

```
az role assignment create \
  --assignee <objectId> \
  --role "User Access Administrator" \
  --scope "/subscriptions/<subId>/resourceGroups/<rgName>"

  ```
#### Step 3: Wait for Propagation
RBAC assignments may take up to 5 minutes to propagate. You can script a wait/retry block if using automation.

#### Step 4: Retry terraform apply

If identity is correctly scoped, it will succeed in assigning roles like:

```
resource "azurerm_role_assignment" "example" {
  scope              = azurerm_resource_group.example.id
  role_definition_name = "Reader"
  principal_id       = azurerm_user_assigned_identity.example.principal_id
}

```
#### Tips to be consider:

- Always assign minimal custom role scopes for automation.
- Use az role definition list to verify permissions.
- In CI/CD, test with a dev environment before production runs.

#### Conclusion
Terraform won’t assign roles unless your identity has the right RBAC permissions. Always pre-check scope, role, and objectId to avoid mid-pipeline failures.


**– Kasi @ [KasdevTech](https://kasdevtech.com)** or [LinkedIn](https://www.linkedin.com/in/kasi-suresh-992675177/)
