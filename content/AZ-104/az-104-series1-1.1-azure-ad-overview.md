---
title: AZ-104 — Azure AD Overview & Tenant Fundamentals
description: Explore Azure Active Directory, tenants, domains, directory structures, and licensing. Understand how Azure AD forms the backbone of identity and access management in Microsoft Azure.
date: 2025-10-08
author: Kasi Suresh
tags: [Azure, AZ-104, AzureAD, Identity, Tenant, Governance]
type: "az-104"
---

# AZ-104 — Azure AD Overview & Tenant Fundamentals

Welcome to the **KasdevTech AZ-104 **, where we explore each exam skill in depth with real-world context.  
This post — **Series 1, Part 1.1** — covers the **foundations of Azure Active Directory (Azure AD)** and the **tenant model**, which is crucial for every Azure Administrator.

---

## What is Azure Active Directory?

**Azure Active Directory (Azure AD)** is Microsoft’s cloud-based identity and access management service.  
It allows organizations to manage users, groups, and access to resources both on-premises and in the cloud.

### Key Capabilities
- Authentication (Sign-in & MFA)
- Authorization (RBAC, access tokens)
- Device and app identity
- SSO (Single Sign-On) for SaaS apps
- Integration with Microsoft 365, Intune, etc.

Azure AD is different from the traditional **Active Directory Domain Services (AD DS)** — it’s built for the cloud.

| Feature | Azure AD | Active Directory DS |
|----------|-----------|---------------------|
| Authentication | OAuth 2.0, SAML, OpenID | Kerberos, NTLM |
| Structure | Flat (no OUs or GPOs) | Hierarchical |
| Management | Azure Portal, CLI, Graph API | ADUC, GPO Console |
| Best For | Cloud and hybrid apps | On-prem servers |

---

## Understanding Tenants and Directories

An **Azure AD Tenant** is a dedicated, trusted instance of Azure AD that your organization receives when it signs up for any Microsoft cloud service (like Azure or Microsoft 365).

### Tenant Example
If your company signs up with **kasdevtech.com**, a tenant is automatically created:  
`kasdevtech.onmicrosoft.com`

You can add your custom domain (`kasdevtech.com`) and verify ownership.

### Tenant Hierarchy
- **Tenant** → Root container for identity management.
- **Directory** → Logical structure under the tenant, contains users, groups, and apps.
- **Subscription** → Linked to one tenant; can’t span multiple tenants.

```bash
# View current signed-in tenant
az account show --query tenantId

# List all tenants accessible
az account tenant list --output table
```

### Real-World Example
A multinational company like *Contoso* might have multiple Azure subscriptions (for Dev, Test, and Prod), all linked to a single tenant for centralized identity management.

---

## Domains in Azure AD

Each tenant has a default domain (e.g., kasdevtech.onmicrosoft.com), but you can add custom verified domains.

```bash
# Add a custom domain
az ad domain create --name "kasdevtech.com"

# List domains
az ad domain list --output table
```

### Domain Verification
To verify a domain, Azure AD provides a TXT record that must be added to your DNS registrar.

Once verified, you can use that domain for UPNs (User Principal Names), email addresses, and login identities.

---

## Directory Roles and Licensing

Azure AD includes built-in **directory roles** that control administrative access.

| Role | Description |
|------|--------------|
| Global Administrator | Full control over all Azure AD resources |
| User Administrator | Manage users, groups, and password resets |
| Application Administrator | Manage app registrations and permissions |
| Security Administrator | Manage security policies and MFA settings |

### Licensing Models
- **Azure AD Free** – Basic user and group management  
- **Premium P1** – Conditional Access, MFA, self-service password reset  
- **Premium P2** – Identity Protection, Privileged Identity Management (PIM)  

```bash
# View current directory roles
az ad role list --output table
```

---

## Portal Walkthrough

**Azure Portal → Azure Active Directory → Overview**  
Here you can view:
- Tenant ID and primary domain
- Licensing information
- Branding and customization
- User & group overview

**Azure Portal → Azure Active Directory → Custom domain names**  
- Add and verify custom domains  
- Configure primary domain

**Azure Portal → Azure Active Directory → Roles and administrators**  
- Assign or review role access for users and groups

---

## Real-World Scenario

**Scenario:**  
KasdevTech is migrating from on-prem Active Directory to Azure AD for cloud workloads.

**Solution Approach:**
1. Create and verify custom domain `kasdevtech.com`
2. Sync users using **Azure AD Connect** (for hybrid setups)
3. Assign roles (e.g., Global Admin, Security Admin)
4. Enable **MFA** and Conditional Access
5. Use **Enterprise Applications** for SSO integration

```powershell
# PowerShell example to view tenant details
Connect-AzureAD
Get-AzureADTenantDetail
```

---

## Common Exam Tips

 **Remember:** A single user can belong to multiple directories, but can only sign in to one at a time.  
Custom domains require **TXT record verification** before use.  
Azure AD roles are independent of Azure Resource Manager (RBAC) roles — exam questions often mix these up.  
Azure AD Free tier does *not* include Conditional Access or PIM.  
Every subscription trusts only one Azure AD tenant.

---

## Summary

| Concept | Key Point |
|----------|------------|
| Azure AD | Cloud-based identity and access management |
| Tenant | Dedicated instance of Azure AD for an organization |
| Domain | Used for user authentication (custom or default) |
| Roles | Define admin access levels |
| Licensing | Determines available identity features |

---

### Coming Next
**Post 1.2 – Managing Users, Groups & Guest Access**  
We’ll explore bulk user management, B2B collaboration, and dynamic groups in depth.

---

**– Kasi @ [KasdevTech](https://kasdevtech.com)** or [LinkedIn](https://www.linkedin.com/in/kasi-suresh-992675177/)
