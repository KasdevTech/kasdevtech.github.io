---
title: AZ-104 Deep Dive — Role Assignments & Automation
description: Creating, assigning, removing, auditing and automating RBAC with CLI, PowerShell, ARM, Bicep and real-world enterprise workflows.
author: Kasi Suresh
tags: [Azure, AZ-104, RBAC, Automation]
type: "az-104"
---

# RBAC Deep Dive — Role Assignments & Automation

This post provides **step‑by‑step RBAC assignment automation** for CLI, PowerShell, ARM, Bicep and Terraform.  
Includes enterprise workflows used in real-large scale organizations.

---

# 1. Role Assignment Concepts

A role assignment binds:

```
Principal → Role → Scope
```

Examples:
- Assign VM Contributor to DevOps group at RG scope
- Assign Key Vault Secrets Officer to AppService MSI at resource scope

---

# 2. Create Role Assignments (CLI)

### Assign Owner at Subscription

```bash
az role assignment create   --assignee <userObjectId>   --role Owner   --scope /subscriptions/<subscriptionId>
```

### Assign VM Contributor at RG

```bash
az role assignment create   --assignee <groupObjectId>   --role "Virtual Machine Contributor"   --resource-group demo-rg
```

### Assign role to Managed Identity

```bash
az role assignment create   --assignee-object-id <miObjectId>   --role "Storage Blob Data Contributor"   --scope /subscriptions/<subId>/resourceGroups/demo-rg/providers/Microsoft.Storage/storageAccounts/kasdevsa
```

---

# 3. PowerShell RBAC

```powershell
Connect-AzAccount

# Assign Reader
New-AzRoleAssignment -ObjectId <objectid> -RoleDefinitionName Reader -Scope "/subscriptions/<sub>"
```

### Remove assignment

```powershell
Remove-AzRoleAssignment -ObjectId <objectid> -RoleDefinitionName Reader
```

---

# 4. Bicep RBAC Automation

```bicep
param principalId string

resource role 'Microsoft.Authorization/roleAssignments@2022-04-01' = {
  name: guid(principalId, 'Reader')
  scope: subscription()
  properties: {
    roleDefinitionId: subscriptionResourceId('Microsoft.Authorization/roleDefinitions', 'acdd72a7-3385-48ef-bd42-f606fba81ae7') // Reader
    principalId: principalId
  }
}
```

---

# 5. Terraform RBAC

```hcl
resource "azurerm_role_assignment" "vm_admin" {
  scope              = azurerm_resource_group.demo.id
  role_definition_name = "Virtual Machine Contributor"
  principal_id       = var.group_object_id
}
```

---

# 6. RBAC Audit & Troubleshooting

### View role assignments for a resource

```bash
az role assignment list --scope <scope> -o table
```

### Check why access is denied

```bash
az role assignment list --assignee <user> -o table
```

### Portal Tools
Azure Portal → Resource → Access Control → Check Access

---

# 7. Real‑World Patterns

### Pattern: Multi‑Layer RBAC
- Subscription: Reader for auditors
- RG: Contributor for DevOps
- Resource: Data roles (Storage Blob Data Reader)

### Pattern: Assign RBAC via CI/CD
Use Bicep/Terraform pipelines to standardize RBAC per environment.

---

# 8. Exam Tips

✔ Know how to assign roles via CLI and PowerShell  
✔ Understand scope differences  
✔ Expect questions on Managed Identity role assignments  
✔ Must know Reader vs Owner vs Contributor boundaries  

---

**– Kasi @ KasdevTech**
