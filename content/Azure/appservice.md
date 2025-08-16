---
title: Troubleshooting Azure App Service Startup Failures
description: Step-by-step guide to diagnose and fix Azure App Service startup failures, including logs, Kudu console, and common misconfigurations.
date: 2025-08-16
author: Kasi Suresh
tags: [Azure, AppService, Troubleshooting, DevOps]
type: "Azure"
---

#### Troubleshooting Azure App Service Startup Failures

One of the most common issues with **Azure App Service** is when your web app refuses to start after deployment.  

The symptoms usually look like this:
- The app returns **HTTP 500 – Internal Server Error**  
- You see **Service Unavailable (503)**  
- The container or code doesn’t start properly  

This is a **real-world headache** because you deploy with confidence, but the app never comes up.



#### Step 1: Check App Service Logs

Enable **Application Logging** and **Web Server Logging**.

**Azure Portal → App Service → Monitoring → App Service logs**  

Or use Azure CLI:

```bash
az webapp log config \
   --name MyAppService \
   --resource-group MyRG \
   --application-logging filesystem \
   --web-server-logging filesystem

   ```
Check the LogFiles directory in Kudu Console (https://<appname>.scm.azurewebsites.net/DebugConsole).

#### Step 2: Use Kudu Console to Debug
The Kudu Console is your best friend.

Navigate to: https://<appname>.scm.azurewebsites.net

Go to Debug Console → CMD

Run commands like:

dir site\wwwroot
Check if your files are deployed correctly. Missing web.config or package.json often causes startup failures.

#### Step 3: Validate Application Settings
Misconfigured settings = silent failure.

In Azure Portal → App Service → Configuration → Application Settings

Verify connection strings (DB, Storage, APIs)

Ensure ASPNETCORE_ENVIRONMENT or WEBSITE_NODE_DEFAULT_VERSION is set correctly

#### Step 4: Check Deployment Logs
If you’re deploying with CI/CD (Azure DevOps, GitHub Actions), open the Deployment Center logs.

```
az webapp deployment list-publishing-profiles \
   --name MyAppService \
   --resource-group MyRG
   ```
This will show if your build failed before reaching App Service.

#### Step 5: Scale & Restart
Sometimes, it’s just about resources.

Restart the App Service from Portal or CLI:

```
az webapp restart --name MyAppService --resource-group MyRG
```
If your app needs more memory, move from B1 (Basic) → S1 (Standard) or higher.

Common Causes of Startup Failures
Missing Dependencies → Node.js, Python, or .NET versions mismatched

Wrong Startup Command → Custom container apps fail if startup.txt or CMD isn’t configured

Port Issues → Containers must listen on PORT=80

Database Connectivity → App boots, but crashes due to DB connection timeout

#### Best Practices
Always use App Service Diagnostics → (Portal → App Service → Diagnose and Solve Problems)

Enable Health Check under App Service → Monitoring

Use Deployment Slots (Staging → Production) to avoid downtime

#### Final Take
Startup issues in Azure App Service are painful but preventable.
With logs, Kudu console, and configuration checks, you can usually fix them within minutes.

Think of this as a standard L1/L2 troubleshooting checklist before escalating further.

**– Kasi @ [KasdevTech](https://kasdevtech.com)** or [LinkedIn](https://www.linkedin.com/in/kasi-suresh-992675177/)
