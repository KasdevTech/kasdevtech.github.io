---
title: AZ-104 — RBAC Overview & Role Fundamentals
description: Complete breakdown of Azure Role-Based Access Control (RBAC), role types, scopes, inheritance, evaluation logic, and real-world design patterns.
author: Kasi Suresh
tags: [Azure, AZ-104, RBAC, IAM]
type: "az-104"
---

# RBAC Deep Dive — Overview & Role Fundamentals

Azure Role-Based Access Control (RBAC) allows fine‑grained access management for Azure resources.  
In AZ‑104, RBAC is one of the most heavily tested areas.

This post provides highly detailed, exam‑level and real‑world knowledge.

---

# 1. RBAC Architecture

RBAC uses **role assignments** to control who can access what resource.

A role assignment = **Principal + Role + Scope**

Where:

| Component | Meaning |
|----------|---------|
| **Principal** | User, Group, Service Principal, Managed Identity |
| **Role** | Set of permissions (JSON definition) |
| **Scope** | Management Group → Subscription → Resource Group → Resource |

### Scope Hierarchy (Very Important for Exam)

```
Management Group
   └── Subscription
         └── Resource Group
               └── Resource
```

> **Permissions inherit downward**, never upward.

Example:  
Assigning **Reader** at Subscription gives read access to all RGs and resources under it.

---

# 2. Built‑in Role Types

Azure includes over 120 built‑in roles.

### Common Admin Roles

| Role | Capabilities |
|------|--------------|
| **Owner** | Full access + can assign roles |
| **Contributor** | Full access except RBAC |
| **Reader** | Read‑only |
| **User Access Administrator** | Can assign roles but cannot manage resources |

### Service‑Specific Roles

Examples:
- Virtual Machine Contributor
- Storage Blob Data Reader
- Key Vault Secrets Officer
- Network Contributor

These give least‑privilege and modular security.

---

# 3. Role Evaluation Logic (Important!)

RBAC uses **additive permissions**.

If a user is assigned two roles:
- Storage Reader
- Storage Contributor

User gets the **sum** of both permissions.

RBAC **does not support deny** except via Azure Blueprints or Azure AD Conditional Access (not RBAC).

---

# 4. CLI & PowerShell Examples

### List available roles

```bash
az role definition list -o table
```

### Show full JSON role definition

```bash
az role definition list --name "Contributor" -o json
```

### Portal Path
Azure Portal → Subscriptions → select subscription → Access Control (IAM)

---

# 5. Real‑World RBAC Design Patterns

### Pattern 1 — Least Privilege
Use granular roles:
- VM team → Virtual Machine Contributor
- Network team → Network Contributor
- Backup admin → Backup Operator

### Pattern 2 — Use Groups, not individuals
Assign RBAC at group level:
- Easier audits
- No “access creep”

### Pattern 3 — Identity Separation
Avoid assigning **Owner** to:
- Developers
- Interns
- App Services

Use managed identities instead.

---

# 6. Exam Tips

✔ Owner is the only role that can assign roles (besides UAA).  
✔ RBAC inheritance always flows downward.  
✔ Use Azure AD groups for assignment, not direct to users.  
✔ Know difference between **Directory Roles** vs **RBAC Roles**.  
✔ Be able to read role JSON structure.

---

**– Kasi @ KasdevTech**  
