---
title: AZ-104 Deep Dive — Managed Identities for Azure Resources
description: Use system-assigned and user-assigned managed identities to secure resource access without credentials.
date: 2025-11-23
author: Kasi Suresh
tags: [Azure, AZ-104, ManagedIdentity, KeyVault]
type: "az-104"
---

# Managed Identities for Azure Resources

This post describes managed identities (system-assigned and user-assigned), how to create them, use them with Key Vault, and best practices.

## Types of managed identities
- **System-assigned**: lifecycle tied to the resource (deleted with resource).
- **User-assigned**: independent resource; can be attached to multiple resources.

## Create & assign identities (CLI)
```bash
# Create user-assigned identity
az identity create --name kasdev-identity --resource-group demo-rg --location eastus

# Assign system-assigned identity to a VM
az vm identity assign --resource-group demo-rg --name kasvm01

# Assign user-assigned identity to VM
az vm identity assign --resource-group demo-rg --name kasvm01 --identities /subscriptions/<sub>/resourceGroups/demo-rg/providers/Microsoft.ManagedIdentity/userAssignedIdentities/kasdev-identity
```

## Use case: Key Vault access
1. Create Key Vault or use existing.
2. Grant the managed identity `get` and `list` permissions on secrets.
3. From the resource, request token from IMDS and use to call Key Vault.

CLI: grant access
```bash
az keyvault set-policy --name kasdev-kv --object-id <identity-object-id> --secret-permissions get list
```

## Example: Access secret from VM (Linux)
- Use the Azure SDK or REST call to IMDS endpoint to obtain token, then call Key Vault.

## Best practices
- Use user-assigned identities for shared services to avoid recreation overhead.
- Limit Key Vault permissions following least privilege.
- Use RBAC-based access for Key Vault (when possible) instead of vault access policies.

## Exam Tips
- Know differences and lifecycle implications.
- Understand how to attach, detach, and assign roles to identities.

---

**– Kasi @ [KasdevTech](https://kasdevtech.com)** or [LinkedIn](https://www.linkedin.com/in/kasi-suresh-992675177/)
