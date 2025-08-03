---
title: "🛠️ Azure VM Boot Issue – VM stuck in 'Starting' or 'Failed'? Here’s how to fix it"
date: 2025-08-03
tags: ["Azure VM", "Troubleshooting", "Boot diagnostics", "Serial Console", "NSG", "Repair"]
categories: ["Azure Compute", "Azure Virtual Machines"]
description: "Your Azure VM stuck on 'Starting' or 'Failed'? Learn how to troubleshoot using Boot Diagnostics, Serial Console, and recovery tools."
---

#### Azure VM Boot Issue – VM stuck in 'Starting' or 'Failed'? Here’s how to fix it

You hit Start on your Azure VM… and it gets stuck in:

>  "Starting..."  
>  "Provisioning failed"  
>  "Failed to start VM"

You're not alone — this is a common issue. In this blog, I’ll show you how to troubleshoot and fix it using **step-by-step, beginner-friendly methods.**



#### Common Causes

| Problem                            | Example |
|------------------------------------|---------|
| Corrupt OS disk                    | Kernel panic / bluescreen |
| VM extension failed                | "Failed to install extension" |
| NSG or route blocking Boot agent   | No serial output |
| DNS or DHCP misconfigured          | Stuck boot or network unreachable |
| OS-level login or update hang      | Incomplete patch |



#### Step-by-step Fix Guide



#### Step 1: Open Boot Diagnostics

Go to your VM → **Boot diagnostics**

- Check **Screenshot** tab
  - Windows: Blue screen? Login screen?
  - Linux: Kernel panic? Black screen?
- Check **Serial log**
  - Look for errors: `Failed to mount`, `No bootable disk`, etc.

>  This is your first clue into what went wrong.



#### Step 2: Try Serial Console (If OS boots partially)

VM → **Serial Console**

- Windows:
  - Login with credentials
  - Check `sconfig` or Event logs
- Linux:
  - Use root shell
  - Check `/var/log/syslog` or `dmesg`

```bash
journalctl -xe
systemctl status
```
You can fix fstab, services, or disable broken extensions directly.

#### Step 3: Run “Redeploy VM”
Go to VM → Support + Troubleshooting → Redeploy
This:
Moves your VM to another host
Retains public/private IP and disk
Fixes hypervisor-side issues
Works well for random "Failed to start" errors.

#### Step 4: Reset SSH or RDP Access (if login fails)
VM → Reset password → Choose OS → Reset login

VM → Run Command → Reset SSH config (Linux)

```
az vm user update --name vm1 --resource-group myRG \
  --username azureuser --password 'StrongP@ssword123!'

```  
#### Step 5: Disk Repair (Advanced)
Stop VM
Detach OS disk
Attach to a healthy rescue VM
Mount and inspect disk:
```
sudo fdisk -l
sudo mount /dev/sdc1 /mnt
Fix /etc/fstab, remove bad init files, update kernel
```
Reattach disk to original VM and boot

#### Step 6: Check NSG or Route Table
Ensure outbound access to:
Azure platform IPs (168.63.129.16)
DNS (8.8.8.8 or 168.63.129.16)
If UDRs block outbound or Boot diagnostics, VM won't load properly

#### Summary Fix Table
Fix	Use When
Boot diagnostics screenshot	See if OS booted
Serial Console	Fix login or boot issues
Redeploy VM	Platform/infrastructure issues
Reset SSH/RDP	Login or key problems
Disk Repair via Rescue VM	Corrupt boot or config file
NSG/UDR fix	Connectivity / agent failures

#### Pro Tips
Always enable Boot Diagnostics for all VMs
Take snapshot before running updates
Use custom script extension to auto repair
Use Availability Set or Zone to avoid platform issues

#### Resources
Azure VM Serial Console
Redeploy VM guide
Run command from portal
Facing the boot error right now?

Message me on LinkedIn for a walkthrough.

– Kasi @ KasdevTech