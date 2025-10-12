---
title: AZ-104 — Managing Users, Groups & Guest Access
description: Learn how to efficiently manage users, groups, and guest access in Azure AD. Covers bulk import, B2B collaboration, dynamic groups, and real-world management scenarios.
date: 2025-10-08
author: Kasi Suresh
tags: [Azure, AZ-104, AzureAD, Users, Groups, B2B]
type: "az-104"
---

# AZ-104 Deep Dive — Managing Users, Groups & Guest Access

This is **Series 1, Part 1.2** of the KasdevTech AZ-104 .  
We focus on **user and group management**, including guest access and advanced scenarios for enterprise deployments.

---

## Managing Users in Azure AD

### Creating Users

Azure AD supports creating users individually or in bulk. Use the **Azure Portal**, **CLI**, or **PowerShell**.

```bash
# Create a single user
az ad user create --display-name "Jane Doe" --user-principal-name janedoe@kasdevtech.com --password "P@ssword123!"

# List all users
az ad user list --output table
```

### Bulk User Import

For large organizations, CSV import is supported via PowerShell.

```powershell
# Import users from CSV
Import-Csv "users.csv" | ForEach-Object {
    New-AzureADUser -DisplayName $_.DisplayName -UserPrincipalName $_.UPN -PasswordProfile (New-Object -TypeName Microsoft.Open.AzureAD.Model.PasswordProfile -Property @{Password = $_.Password; ForceChangePasswordNextLogin=$true}) -AccountEnabled $true
}
```

### Real-World Example

- A company onboarding 100 new hires at once can automate user creation via CSV import and assign them to default groups and roles automatically.

---

## Managing Groups in Azure AD

Groups simplify permission management by assigning access to multiple users simultaneously.

### Types of Groups

| Type | Description |
|------|-------------|
| Security | Used for access control to resources |
| Microsoft 365 | Used for collaboration (Teams, SharePoint) |

### Dynamic Groups

- Membership can be automatic based on rules (e.g., department, location)

```powershell
# Create a dynamic group for all users in 'Sales' department
New-AzureADMSGroup -DisplayName "Sales Team" -MailEnabled $false -SecurityEnabled $true -MailNickName "Sales" -GroupTypes "DynamicMembership" -MembershipRule "(user.department -eq 'Sales')" -MembershipRuleProcessingState "On"
```

### Real-World Example

- Automatically add new employees to relevant security groups based on their department to streamline access management and reduce admin overhead.

---

## Guest Access and B2B Collaboration

Azure AD allows **external users** to collaborate securely via B2B (Business-to-Business) collaboration.

### Inviting Guest Users

```bash
# Invite guest user
az ad user invite --user-principal-name partner@external.com --display-name "Partner User" --send-invitation-message true
```

### Guest Access Best Practices

- Limit guest permissions to only required resources  
- Assign guests to specific groups for RBAC  
- Monitor guest activity regularly for security compliance  

### Real-World Scenario

- A partner company needs temporary access to a SharePoint site.  
- Invite them as a guest user and assign them to a group with restricted permissions.  
- Remove or disable the account after the project ends.

---

## CLI & PowerShell Tips

- Use `az ad user list --filter "userPrincipalName eq 'john@kasdevtech.com'"` for targeted queries  
- Use `Get-AzureADUser` in PowerShell to fetch specific attributes and assign roles dynamically  
- Combine dynamic groups with automation scripts for enterprise-scale user management

---

## Common Exam Tips

Bulk operations are preferred in real-world enterprise scenarios  
Dynamic groups simplify ongoing management and reduce errors  
B2B guest accounts require explicit invitation and can be monitored for security  
Always assign users to roles and groups following least privilege principles  

---

## Summary

| Concept | Key Takeaway |
|---------|--------------|
| Users | Create individually or in bulk; manage via CLI/PowerShell/Portal |
| Groups | Security and Microsoft 365; dynamic membership recommended |
| Guests | B2B collaboration with restricted access and monitoring |

---

### Coming Next
**Post 1.3 – Authentication, MFA & Conditional Access**  
We’ll dive into securing Azure AD with multi-factor authentication, conditional access policies, and identity protection.

---

**– Kasi @ [KasdevTech](https://kasdevtech.com)** or [LinkedIn](https://www.linkedin.com/in/kasi-suresh-992675177/)
