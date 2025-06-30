---
title: "Azure Application Gateway 502 Error – Full Troubleshooting Guide for Beginners"
date: 2025-06-30
tags: ["Azure", "Application Gateway", "502 Error", "Troubleshooting", "Beginner"]
categories: ["Azure"]
description: "Step-by-step guide to troubleshoot and fix 502 errors on Azure Application Gateway. Easy enough for Beginners, clear enough for production."
type: "Azure"
---

If you’ve seen this before, don’t panic. This guide walks you through:

- What a 502 error means in Azure
- How to identify the root cause
- How to fix it with simple step-by-step actions

---

####  Step-by-Step Troubleshooting

####  Step 1: Reproduce the Problem

Go to the App Gateway public IP or custom domain (e.g., `https://myappexampleapp.com`)  
Check if the site is returning this:
502 - Web server received an invalid response while acting as a gateway or proxy server.
This means App Gateway couldn’t reach your backend **properly** — not that the app is down.

---

#### Step 2: Go to Azure Portal → Application Gateway

1. Open [portal.azure.com](https://portal.azure.com)
2. Search for your **Application Gateway** in the top bar.
3. Click on it to open the overview page.
---

#### Step 3: Check Backend Health

This is the most important step.
1. In the left menu, click on **“Backend health”**
2. You'll see your backend pool (App Service, VM, AKS, etc.)

Look for:

| Instance | Status     | Details                      |
|----------|------------|------------------------------|
| 0        |  Unhealthy | "Probe failed with 403"      |
| 1        |  Healthy   | "Received 200 from backend"  |

If you see  **Unhealthy** – note the reason (e.g., "Probe failed with status 403").


#### Step 4: Understand the Health Probe

 App Gateway uses a health probe(like a heartbeat check) to see if the backend is healthy.
 By default, the probe goes to `/` on your app — if that path returns 403 or 404, AppGW thinks it’s broken!


#### Step 5: Check Your App Service or Backend
1. Open your App Service or backend in Azure.
2. Under "App Service > Browse", visit the base URL.
3. Check if the root (`/`) is protected (e.g., needs login or redirects to Azure AD).
   - This causes AppGW to get blocked (403).
4. If yes, you need to **expose a simple health check endpoint**.
---

####  Step 6: Add a Custom Health Endpoint

In your backend app, create a new path like `/healthz`.

#### Example in Python Flask:

```python
@app.route("/healthz")
def health_check():
    return {"status": "ok"}, 200
Example in Node.js:

app.get("/healthz", (req, res) => {
  res.status(200).send({ status: "ok" });
});
This route should:
Be public (no auth)
Return status code 200
```
#### Step 7: Configure Custom Probe in App Gateway
Back to Application Gateway:
Go to “Health probes”
Click Add
Fill the form:
Name: custom-healthz
Protocol: HTTP or HTTPS (match backend)
Path: /healthz
Interval: 30 seconds
Timeout: 30 seconds
Unhealthy threshold: 3
Save the probe.

#### Step 8: Attach Probe to Backend Pool
Go to "HTTP Settings"
Click on the setting used by your listener
Under "Probe", select custom-healthz
Save

#### Step 9: Wait and Monitor
It takes a minute or two.
Then go back to Backend Health → You should now see:
Healthy ✔️
Now refresh your website. No more 502 errors 🙌
Extra Checks (if still not working)
- App is not listening on the expected port (use curl or SSH)
- SSL certificate issues (check if HTTPS probe is used)
- Backend DNS resolution issues inside AppGW subnet
- NSG/UDR blocking traffic between AppGW and backend
- App takes too long to respond (increase probe timeout)

#### Enable Diagnostics Logs (Optional but Recommended)
In Application Gateway → Diagnostics Settings
Enable:
Access logs
Performance logs
Firewall logs (if WAF enabled)
Send to Log Analytics / Storage for future review

#### Final Tips
Expose a lightweight /healthz endpoint — it's critical
Never protect health endpoints with auth
Add alerts for backend probe failures
Monitor backend response time via AppGW metrics

#### Useful Links
- https://learn.microsoft.com/en-us/azure/application-gateway/application-gateway-backend-health-troubleshooting
- https://learn.microsoft.com/en-us/azure/application-gateway/application-gateway-probe-overview

If this helped you or you’re building a production-grade Azure setup —
👋 Drop by kasdevtech.com for more real-time stories.


