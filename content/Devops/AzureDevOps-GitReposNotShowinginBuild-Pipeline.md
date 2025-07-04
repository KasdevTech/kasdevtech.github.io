
---
title: "Azure DevOps Git Repos Not Showing in Build Pipeline: Fixing Broken Repo Connections"
date: 2025-07-04
categories: [Azure DevOps, Git, CI/CD]
tags: [Pipelines, GitHub, Azure Repos, Service Connection]
type: "DevOps"
---


Seeing this error when trying to trigger a pipeline from your Azure DevOps repo?

Error: The repository ‘<repo-name>’ could not be found or no longer exists.

#### Common Causes

- Repository renamed or deleted
- Permissions changed in the project
- PAT token expired (for GitHub or external repos)

#### Fixing the Issue

#### Azure Repos Git

- Navigate to `Repos` in your project
- Check if the repo still exists and hasn’t been renamed
- Confirm the branch in your trigger matches the YAML

```yaml
trigger:
  branches:
    include:
      - main
```   
#### GitHub Repositories
Go to Project Settings → Service Connections
Open your GitHub connection
Re-authenticate or update the PAT/token
Ensure scopes: repo, workflow, admin:repo_hook

#### Validate Pipeline YAML
```  
pool:
  vmImage: ubuntu-latest

steps:
  - checkout: self
  - script: echo "Building app..."

If using multiple repos:

resources:
  repositories:
    - repository: templates
      type: git
      name: DevOps/templates
```  
#### Permissions for Pipeline Identity
Project Settings → Repositories → Permissions
Ensure Project Collection Build Service has at least Read access

If the pipeline fails after switching branches or renaming repos, update the trigger and checkout steps immediately to reflect the changes.

#### Conclusion
Broken repo connections are a common issue, but easily resolved with a few checks. Keep your PATs and permissions up-to-date, and your builds will keep flowing.

