---
title: "Azure Pipeline Not Triggering Automatically on Push – YAML Trigger Issues"
date: 2025-07-05
categories: [Azure DevOps, Pipelines]
tags: [CI/CD, YAML, Triggers, Debugging]
type: "DevOps"
---

Ever pushed code and expected the pipeline to run… but nothing happens?
This is one of the most common issues teams face after setting up YAML-based Azure Pipelines.

####  Symptoms

- No pipeline run triggered after pushing code
- Manual runs work fine
- Pipeline shows: `No CI trigger found for this repo`

#### Common Causes

1. **Missing `trigger` block in YAML**  
2. Wrong branch name under `trigger`  
3. YAML file is in a non-default location or branch  
4. Triggers disabled in pipeline UI  
5. Repo is disconnected or has permission issues

####  Define the Trigger Block Properly

```yaml
trigger:
  branches:
    include:
      - main

If you're using develop, adjust accordingly.
```

#### Check Pipeline Settings in Azure DevOps
Go to Pipelines → Click your pipeline → Edit
Click the 3 dots → Triggers
Ensure CI Trigger is enabled

#### YAML File Location Matters
If your YAML file is not in the root folder, define the path in pipeline config:
Go to Pipeline → Edit
Set path correctly: .azure-pipelines/pipeline.yml

#### Repository Permissions
Make sure the Build Service has at least Read access to the repo

#### Conclusion:
Triggers not working is mostly a YAML or permission issue. Always define trigger branches explicitly and keep your repo permissions tight but correct.

