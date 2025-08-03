
---
title: "🚧 Azure Application Gateway – Backend Health Unknown? Fix Step-by-Step"
date: 2025-08-03
tags: ["Azure Application Gateway", "Troubleshooting", "Probes", "NSG", "Load Balancer"]
categories: ["Azure Networking", "Application Gateway"]
description: "App Gateway backend shows 'Unknown' or 'Unhealthy'? Follow this detailed troubleshooting guide to fix it."
type: "Azure"
---

### Azure Application Gateway – Backend Health Unknown? Fix Step-by-Step

If you’re using Azure Application Gateway and you see:

>  **Backend health: UNKNOWN**  
>  **Backend health: UNHEALTHY**

Don’t panic. This is a common issue — and we’ll walk through how to fix it **end-to-end**, even if you’re new to Azure.



####  What Does “Unknown” or “Unhealthy” Mean?

- **Unknown** = App Gateway **can’t reach** the backend (network issue)
- **Unhealthy** = App Gateway **can reach** the backend, but **probe failed** (wrong path, port, etc.)



#### Step-by-Step Troubleshooting



#### Step 1: Check Backend Pool IP/VM

Go to:
App Gateway → **Backend pools**
Confirm:

- Correct **IP or FQDN**
- The backend (VM, App, etc.) is **running**
- If using **FQDN**, DNS must be resolvable



#### Step 2: Validate Probes

App Gateway → **Health Probes**

- Confirm the **path** exists — e.g., `/health`, `/status`, etc.
- Check **protocol** (HTTP or HTTPS)
- Ensure **custom host name** (if used) matches backend cert (for HTTPS)

Avoid using `/` as probe path for apps that require login or redirect.



#### Step 3: Review Listener + HTTP Settings

App Gateway → **HTTP Settings**

- Backend port = matches backend (usually 80 or 443)
- Use correct **protocol**
- If HTTPS: Set **pick host name from backend**, or set manually
- Associate with correct **probe**



#### Step 4: Backend NSG and Routes

Check **backend subnet’s NSG**:

Allow:
- Inbound from App Gateway subnet on **port 80/443**
- Outbound to App Gateway if response is needed

Check **UDR** (User Defined Routes):

Avoid sending App Gateway traffic to NVA/firewall unless configured properly.



#### Step 5: Diagnose from App Gateway

Go to:

App Gateway → **Backend health**

Here you’ll see:

| Backend | Status   | Code | Description        |
|---------|----------|------|--------------------|
| 10.0.1.4 | Unknown | 0    | No response        |
| 10.0.1.5 | Unhealthy | 403 | Probe failed auth |

> Click each backend to view probe logs and exact error



#### Step 6: Use Network Watcher

Enable **Connection Troubleshoot** from:

Network Watcher → **Connection troubleshoot**

- Test from App Gateway subnet → Backend IP:Port
- Verify reachability and response time


#### Fix Summary

| Issue                             | Fix                                      |
|----------------------------------|-------------------------------------------|
| Backend health Unknown           | NSG/UDR block, wrong IP, DNS issue        |
| Backend health Unhealthy         | Wrong probe path, wrong port/cert         |
| HTTPS failing probe              | Hostname mismatch or cert issue           |
| DNS FQDN backend unreachable     | Private DNS or no resolution              |
| VMs in stopped state             | Start them or replace in backend pool     |

---

#### Quick Fix – Sample NSG Rule

```bash
az network nsg rule create \
  --resource-group myRG \
  --nsg-name backend-nsg \
  --name AllowAppGw \
  --priority 100 \
  --direction Inbound \
  --access Allow \
  --protocol Tcp \
  --source-address-prefixes <AppGwSubnetPrefix> \
  --destination-port-ranges 80 443

```

Final Tips:
Use custom probes over default probes
Always test probe path manually in browser or Postman
For HTTPS, check backend certs and hostname validation
Use FQDN only if DNS is guaranteed to resolve

References:
Troubleshoot App Gateway backend health
Custom probes

Need help debugging your Gateway?
Drop a comment or reach out on LinkedIn!

– Kasi @ KasdevTech 🚀