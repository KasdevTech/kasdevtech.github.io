---
title: AZ-104 Deep Dive — Authentication, MFA & Conditional Access
description: Implementing authentication methods, MFA, Conditional Access and Identity Protection for AZ-104.
date: 2025-11-23
author: Kasi Suresh
tags: [Azure, AZ-104, MFA, ConditionalAccess]
type: "Azure"
---

# Authentication, MFA & Conditional Access

This post covers authentication protocols, password protection, MFA implementation, Conditional Access policies, Identity Protection and exam-ready examples.

## Authentication protocols
- **OAuth 2.0**: authorization framework for token issuance.
- **OpenID Connect**: identity layer on top of OAuth2 for SSO.
- **SAML 2.0**: legacy enterprise SSO.
- **Kerberos/NTLM**: on-prem AD DS scenarios.

## Password policies & SSPR
- Enable Self-Service Password Reset (SSPR) to reduce helpdesk load.
- Combine with MFA for secure recovery.

PowerShell (MSOnline / AzureAD):
```powershell
# Example: enable SSPR settings (via Graph / portal is common)
# Use portal: Azure AD -> Password reset -> Properties -> Selected/All users
```

## Multi-Factor Authentication (MFA)
- Enforce MFA for high-privilege users (admins).
- Use Conditional Access to apply MFA only when needed (less friction).

CLI: enable per-user MFA (example)
```powershell
# Per-user MFA is being deprecated in favor of Conditional Access policies.
# Use Conditional Access policies (P1+) for production.
```

## Conditional Access (CA)
CA evaluates conditions (user, device, location, risk) and enforces controls (MFA, block, require compliant device).

Portal: Azure AD -> Security -> Conditional Access -> New policy
Example policy: Require MFA for all admins
- Assign: Users and groups -> Directory role -> Global administrator
- Cloud apps: All cloud apps
- Conditions: Sign-in risk / locations as needed
- Grant: Require multi-factor authentication

PowerShell: CA policies are typically managed via MS Graph APIs; examples require Graph cmdlets.

## Identity Protection
- Detect risky sign-ins and risky users.
- Automate remediation (require password reset, block access).

Example use-case:
- Detect high-risk sign-in -> require password reset -> block until remediation.

## Exam Tips
- Understand P1 vs P2 features: Conditional Access requires P1; Identity Protection requires P2.
- Know typical CA policy scopes and What If tool for testing.
- Legacy authentication should be blocked where possible.

---

**– Kasi @ [KasdevTech](https://kasdevtech.com)** or [LinkedIn](https://www.linkedin.com/in/kasi-suresh-992675177/)
