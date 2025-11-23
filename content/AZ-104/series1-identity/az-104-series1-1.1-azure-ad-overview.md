
---
title: "AZ-104 — Azure AD Overview & Tenant Fundamentals"
description: "Foundations of Azure Active Directory: tenants, domains, directory roles and licensing."
date: 2025-11-23
author: "Kasi Suresh"
tags:
  - Azure
  - "AZ-104"
  - AzureAD
  - Identity
type: "Azure"
---



# Azure AD Overview & Tenant Fundamentals

This deep-dive covers the fundamentals of Azure Active Directory (Azure AD) — the identity backbone for Microsoft cloud services. It is written with AZ-104 objectives in mind and includes CLI, PowerShell, portal steps, real-world scenarios, and exam tips.

## What is Azure AD?
Azure AD is Microsoft’s cloud identity and access management service. It provides authentication, authorization, federation, and device identity for cloud and hybrid scenarios.

### Key capabilities
- Authentication (OAuth2, OpenID Connect, SAML)
- Authorization (tokens, RBAC integration)
- Single Sign-On (SSO) for SaaS apps
- Identity protection, Conditional Access
- Device management integration (Intune)

## Azure AD vs AD DS (short)
- Azure AD is flat (no OUs), designed for cloud apps; AD DS is hierarchical with GPOs for on-premises servers.
- Authentication protocols differ: Azure AD uses OAuth2/OpenID Connect/SAML; AD DS uses Kerberos/NTLM.

## Tenants and Directories
- **Tenant**: a dedicated instance of Azure AD (e.g., kasdevtech.onmicrosoft.com).
- **Directory**: logical container inside tenant holding users, groups, apps.
- **Subscription**: linked to a single tenant.

### CLI: view tenant and subscriptions
```bash
# Show signed-in account and tenant
az account show --query "{tenantId:tenantId, subscription: name}"

# List accessible tenants
az account tenant list -o table
```

### Portal steps
1. Sign in to Azure Portal.
2. Search "Azure Active Directory".
3. Overview shows Tenant ID, Primary domain, Licenses.

## Domains
- Default domain: <tenant>.onmicrosoft.com
- Add custom domain for UPNs and email addresses.

### CLI: add custom domain (preview)
```bash
az ad domain create --name "kasdevtech.com"
az ad domain list -o table
```

*Note: Domain verification requires adding a TXT record at your DNS provider.*

## Directory Roles and RBAC distinction
- Directory roles (Global Administrator, User Administrator, etc.) manage Azure AD objects.
- RBAC (Owner, Contributor, Reader) manages Azure resources (subscriptions, resource groups, resources).
> Exam tip: Directory roles and RBAC are separate — questions often test this distinction.

### List directory roles (CLI)
```bash
az ad sp list --query "[].{appId:appId, displayName:displayName}" -o table
```

## Licensing overview
- Free: basic user and group management.
- Premium P1: Conditional Access, SSPR, MFA integration.
- Premium P2: Identity Protection, Privileged Identity Management (PIM).

## Real-world tenant design
- Centralized tenant for corporate identity.
- Use Management Groups + Subscriptions for environment separation (Dev/Test/Prod).
- Use Azure AD Connect for hybrid identity sync.

## Exam Tips
- Know tenant vs subscription relationship.
- Be able to describe domain verification steps.
- Understand what features require P1 or P2.

---

**– Kasi @ [KasdevTech](https://kasdevtech.com)** or [LinkedIn](https://www.linkedin.com/in/kasi-suresh-992675177/)
