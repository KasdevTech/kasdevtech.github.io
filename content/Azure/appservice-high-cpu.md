---
title: Fixing High CPU and Memory Usage in Azure App Service
description: A step-by-step guide to troubleshoot and resolve performance issues in Azure App Service caused by high CPU or memory usage.
date: 2025-08-16
author: Kasi Suresh
tags: [Azure, AppService, Troubleshooting, Performance, DevOps]
type: "Azure"
---

#### Fixing High CPU and Memory Usage in Azure App Service

Your app is running fine, and then suddenly… 🚨 users complain about **slowness** or the app even **crashes**.  
When you check the Azure Portal, you see CPU pegged at 90–100% or memory exhausted.  

This is a very **common real-world issue** in Azure App Service. Let’s walk step by step.



#### Step 1: Monitor Metrics

Go to:
**Azure Portal → App Service → Metrics → CPU Percentage / Memory Working Set**

Look for spikes during:
- High user traffic
- Background jobs
- Large API calls

You can also run via CLI:

```bash
az monitor metrics list \
  --resource /subscriptions/<subid>/resourceGroups/MyRG/providers/Microsoft.Web/sites/MyAppService \
  --metric "CpuPercentage" --interval PT1M

  ```
This gives you CPU usage minute by minute.

#### Step 2: Use App Service Diagnostics
In the App Service → Diagnose and Solve Problems:

Select Availability & Performance

Check High CPU Analysis or High Memory Analysis

This shows you:

Top requests consuming resources

Long-running threads

Memory leaks

#### Step 3: Profile the App
Enable Application Insights Profiler:

Portal → App Service → Application Insights → Turn On Profiler

Capture snapshots during high load

Review flame charts to see slow functions or memory leaks

#### Step 4: Scale Out or Scale Up
Sometimes, the fix is simple: add more resources.

Scale Up → Increase plan (B1 → S1 → P1v3)

Scale Out → Add more instances

```
az appservice plan update \
   --name MyAppPlan \
   --resource-group MyRG \
   --number-of-workers 3
   ```
This adds 3 worker instances to balance load.

#### Step 5: Optimize the App
High CPU isn’t always Azure’s fault. Check for:

Infinite loops in code

Heavy synchronous operations

Poor database queries

✅ Use async programming
✅ Cache results in Azure Cache for Redis
✅ Optimize database queries with indexes

#### Step 6: Use Autoscale
Enable Autoscale Rules to handle traffic spikes:

Portal → App Service Plan → Scale Out (App Service Plan)

Example:

Scale out if CPU > 75% for 10 minutes

Scale back in when CPU < 40%

#### Step 7: Restart and Recover
If your app gets stuck:
```
az webapp restart --name MyAppService --resource-group MyRG
```
Sometimes a simple restart clears memory leaks temporarily until you apply a permanent fix.

#### Common Causes of High CPU/Memory

Unoptimized Code → Loops, blocking threads, recursive calls

Leaky Dependencies → Not disposing connections properly

Bad DB Queries → Full table scans

Large Payloads → JSON/XML parsing at scale

Traffic Surge → Sudden load without autoscale

#### Best Practices
Always enable Application Insights for monitoring

Use Azure Front Door or Azure CDN to offload static content

Offload long jobs to Azure Functions or Azure WebJobs

Test performance with Azure Load Testing

#### Final Take
High CPU and memory issues in Azure App Service are often a mix of code inefficiency + resource limits.
With monitoring, scaling, and profiling tools, you can quickly identify whether the fix is your app or your plan.

Remember: Don’t guess → Measure → Fix → Scale.

**– Kasi @ [KasdevTech](https://kasdevtech.com)** or [LinkedIn](https://www.linkedin.com/in/kasi-suresh-992675177/)
