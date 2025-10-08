---
title: AZ-104 — Introduction and Manage Azure Identities & Governance
description: Begin your AZ-104 journey. Learn the exam structure, skills measured, and dive into Azure Active Directory, RBAC, and governance fundamentals.
date: 2025-10-08
author: Kasi Suresh
tags: [Azure, AZ-104, Certification, RBAC, Governance]
type: "Azure"
---

# AZ-104 — Introduction and Manage Azure Identities & Governance

Welcome to the AZ-104 Exam Series**!  
In this post, we’ll first introduce the **Microsoft Azure Administrator (AZ-104)** certification — what it is, who it’s for, and how to prepare — followed by an in-depth look at **Azure Identity and Governance** management.

---

##  Part 1: Introduction to AZ-104

###  What is the AZ-104 Exam?

The **AZ-104** exam tests your ability to manage core Azure services like compute, networking, and storage.  
It’s ideal for professionals managing day-to-day Azure operations.

###  Who Should Take It

- IT Admins managing on-prem or hybrid systems  
- Cloud/DevOps Engineers maintaining infrastructure  
- Students pursuing Microsoft certifications  

###  Skills Measured

| Domain | Weight |
|--------|--------|
| Manage identities & governance | 15–20% |
| Manage storage | 10–15% |
| Manage compute resources | 25–30% |
| Manage networking | 30–35% |
| Monitor & backup | 10–15% |

###  Tools Required
- Azure Portal  
- Azure CLI  
- Azure PowerShell  
- VS Code with Azure extensions  

### Study Strategy
1. Learn theory from Microsoft Learn  
2. Practice on a real Azure subscription  
3. Automate with CLI & PowerShell  
4. Take mock tests  

---

##  Part 2: Manage Azure Identities and Governance

### 1. Azure Active Directory (Azure AD)

Azure AD handles authentication, user management, and app access in the cloud.

#### Common Tasks:
```bash
# List users
az ad user list --output table

# Create new user
az ad user create --display-name "Kas Dev"   --user-principal-name kasdev@kasdevtech.onmicrosoft.com   --password "P@ssword123!"
```

---

### 2. Role-Based Access Control (RBAC)

RBAC controls **who can do what** in Azure.

| Role | Access Level |
|------|---------------|
| Owner | Full control |
| Contributor | Manage resources |
| Reader | View only |

```bash
# Assign Reader role to a user
az role assignment create   --assignee johndoe@kasdevtech.onmicrosoft.com   --role "Reader"   --resource-group demo-rg
```

---

### 3. Governance Tools

####  Management Groups
Organize subscriptions under logical hierarchies.

```bash
az account management-group create --name "Production"
```

####  Azure Policy
Apply compliance and configuration rules.

```bash
az policy assignment create   --name "EnforceTags"   --scope "/subscriptions/<id>/resourceGroups/demo-rg"   --policy "/providers/Microsoft.Authorization/policyDefinitions/<policyId>"
```

---

###  Best Practices
- Enforce **MFA** for all users  
- Apply **least privilege** roles  
- Use **Management Groups** for multi-subscription setups  
- Regularly **audit RBAC assignments**  

---

###  Real-World Scenario

| Environment | Role | Access |
|--------------|------|--------|
| Dev | Contributor | Full |
| Test | Contributor | Partial |
| Prod | Reader | View only |

Policies ensure cost efficiency and security compliance across all environments.

---

##  Summary

| Section | Focus |
|----------|--------|
| Azure AD | User/Group management |
| RBAC | Role assignments |
| Policy | Compliance enforcement |

---

###  Coming Next
** — Azure Storage and Compute Management**

We’ll explore:
- Creating and securing Azure Storage Accounts  
- Deploying and managing Virtual Machines  

---

**– Kasi @ [KasdevTech](https://kasdevtech.com)** or [LinkedIn](https://www.linkedin.com/in/kasi-suresh-992675177/)
