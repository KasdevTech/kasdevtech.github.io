---
title: "Terraform Destroy Fails in Azure Due to Resource Dependencies — Here's the Fix"
date: 2025-07-16
author: "Kasi Suresh"
tags: ["Terraform", "Azure", "Destroy", "Troubleshooting"]
summary: "Running `terraform destroy` in Azure sometimes fails due to implicit resource dependencies. Here's how I resolved a common NSG and subnet dependency issue and ensured clean teardown."
type: "Terraform"
---

> Error:
>
> ```
> Error: deleting Network Interface: cannot delete because of resource being in use
> ```

---

#### The Problem

While cleaning up a non-prod environment using:

```bash
terraform destroy
Terraform failed to delete certain resources (like Network Interfaces, NSGs, or Public IPs) due to implicit dependencies.
```
#### Common Cases in Azure
- NSG attached to a subnet
- Subnet attached to a NIC
- Public IP still in use by Load Balancer
- Role Assignments not deleting properly due to RBAC propagation delays

#### Step-by-Step Fix
#### Step 1: Identify the Failing Resources
Terraform typically logs the resource it failed to delete. If unclear, use:

- terraform state list
- or directly inspect the Azure Portal to trace dependencies.

#### Step 2: Use terraform taint or terraform state rm
You can either taint the resource to recreate it later or remove it manually from state:
```
terraform taint azurerm_network_interface.nic1

OR

terraform state rm azurerm_network_interface.nic1
```
 Use state rm with caution — it removes tracking but does NOT delete the resource!

####  Step 3: Destroy in Stages (Use Targeting)
Destroy resources in a specific order:

```
terraform destroy -target=azurerm_network_interface.nic1
terraform destroy -target=azurerm_subnet.subnet1
terraform destroy
```
This forces Terraform to destroy dependencies manually in sequence.

#### Step 4: Final Clean-Up
After partial destroy, run:

```
terraform destroy
```
again to remove remaining infra.
If required, delete leftover resources in Azure Portal.


- Avoid using implicit dependencies; declare them using depends_on if order matters.
- Split NSGs, subnets, and NICs into separate modules for better control.
- Tag resources clearly with environment, owner, etc., to identify leftovers.



#### Conclusion
Terraform destroy is powerful — but you must manage Azure dependencies explicitly for smooth clean-up. Manual ordering and dependency awareness are key!

