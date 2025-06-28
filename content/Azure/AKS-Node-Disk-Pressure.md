---
title: " AKS Node Disk Pressure "
date: 2025-06-28
tags: ["Azure", "AKS", "Troubleshooting", "Kubernetes"]
categories: ["Azure"]
description: "A production issue in Azure AKS where nodes ran into DiskPressure. Here's how we investigated, fixed, and prevented it in the future."
type: "Azure"
---

####  What Happened?

Hey folks,  
Let me share a real incident we faced in production on **Azure Kubernetes Service (AKS)**. Our workloads were behaving oddly — pods getting evicted, app downtime alerts, and our monitoring tools screaming `DiskPressure` on some nodes.

We didn’t make any infra changes recently, so the obvious question was:  
**What’s going on inside the AKS nodes?**

####  Root Cause Analysis
We dug into the node metrics using **Azure Monitor** and `kubectl describe node`. Here’s what we found:
```
- **DiskPressure Condition = True**
- Evicted pods had logs like:
The node was low on resource: ephemeral-storage.
Turns out, ephemeral storage on the nodes was filling up rapidly — mostly from:
Container logs
Image cache
Tmp files inside /var/lib/docker
```
Solution Applied
Here’s how we fixed it step-by-step:
```
1. Enabled Log Rotation
We added a custom containerd config to enable log rotation on our AKS nodes.

# /etc/containerd/config.toml

[plugins."io.containerd.grpc.v1.cri".containerd]
  max_log_size = "10MiB"
  max_log_files = 3
Then restarted containerd:

sudo systemctl restart containerd

2. Cleaned Up Unused Docker Resources (Manual Step)
On affected nodes:


docker system prune -a
If you're using containerd, use crictl or ctr instead of Docker.

 3. Implemented Auto Cleanup CronJob
We created a daemonset that periodically cleans up unused logs and image layers, to avoid manual interventions.
```

#### Long-Term Fix:
- We updated our AKS node pool disk size from 100Gi → 200Gi and set up proper alerts:
- Azure Monitor Alert on node disk usage > 70%
- Action Group integration to alert via Teams/Email

#### Final Thoughts:
- Logs are silent killers.
- Monitoring node storage is non-negotiable.
- Don’t rely on default log settings — customize them!

If you're running AKS in production, please double-check your disk usage, retention, and alerting setup.