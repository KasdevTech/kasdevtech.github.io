---
title: AZ-104 — Managing Users, Groups & Guest Access
description: Users, groups, dynamic membership and B2B guest collaboration in Azure AD for AZ-104.
date: 2025-11-23
author: Kasi Suresh
tags: [Azure, AZ-104, Users, Groups, B2B]
type: "az-104"
---

# Managing Users, Groups & Guest Access

This post shows how to manage users, groups, bulk operations, dynamic groups and B2B guest access with CLI, PowerShell and portal steps.

## Users: creation and lifecycle
- Create users via Portal, Azure CLI, PowerShell, or Azure AD Connect for hybrid sync.
- Consider password policies, SSPR and onboarding automation.

### CLI examples
```bash
# Create a user
az ad user create --display-name "Jane Doe" --user-principal-name janedoe@kasdevtech.com --password "P@ssword123!" --force-change-password-next-sign-in true

# Get user details
az ad user show --id janedoe@kasdevtech.com
```

### PowerShell (AzureAD module)
```powershell
Connect-AzureAD
New-AzureADUser -DisplayName "Jane Doe" -UserPrincipalName "janedoe@kasdevtech.com" -AccountEnabled $true -PasswordProfile (New-Object -TypeName Microsoft.Open.AzureAD.Model.PasswordProfile -Property @{Password="P@ssword123!"; ForceChangePasswordNextLogin=$true})
```

### Bulk import (CSV) example (PowerShell)
```powershell
Import-Csv users.csv | ForEach-Object {
  $pwd = $_.Password
  New-AzureADUser -DisplayName $_.DisplayName -UserPrincipalName $_.UPN -AccountEnabled $true -PasswordProfile (New-Object -TypeName Microsoft.Open.AzureAD.Model.PasswordProfile -Property @{Password=$pwd; ForceChangePasswordNextLogin=$true})
}
```

## Groups: Security vs Microsoft 365
- **Security groups**: for access control (RBAC, app assignment).
- **Microsoft 365 groups**: for collaboration (Teams, SharePoint).

### Create group (CLI)
```bash
az ad group create --display-name "Dev Team" --mail-nickname "devteam"
```

### Dynamic membership
- Useful to auto-add users based on attributes (department, location).

PowerShell example:
```powershell
New-AzureADMSGroup -DisplayName "Sales" -MailEnabled $false -SecurityEnabled $true -MailNickName "sales" -GroupTypes "DynamicMembership" -MembershipRule "(user.department -eq 'Sales')" -MembershipRuleProcessingState "On"
```

### Guest users (B2B)
- Invite external collaborators as guests.
- Control guest scope: restrict to specific resources and use access reviews.

CLI invite:
```bash
az ad user invite --user-principal-name partner@example.com --display-name "Partner User" --send-invitation-message true
```

### Portal steps: add guest user
1. Azure AD → Users → New guest user → Invite user.
2. Configure group membership and roles.

## Real-world scenario
- Onboard 200 contractors: use CSV import, assign to dynamic group by department, apply Conditional Access policies to guest group.

## Exam Tips
- Know differences between group types and use-cases.
- Understand dynamic group rule syntax basics (equals, contains, -eq, -ne).
- Guests require explicit invitation; external users may appear with userType "Guest".

---

**– Kasi @ [KasdevTech](https://kasdevtech.com)** or [LinkedIn](https://www.linkedin.com/in/kasi-suresh-992675177/)
