---
title: "Sample Azure DevOps Pipeline for .NET App"
date: 2025-06-23T11:20:00+05:30
draft: false
tags: [azure, devops, pipeline, ci-cd, cloud]
---

Here is a simple YAML pipeline for building a .NET Core app:

```yaml
trigger:
- main

pool:
  vmImage: 'ubuntu-latest'

steps:
- task: UseDotNet@2
  inputs:
    packageType: 'sdk'
    version: '8.0.x'

- script: |
    dotnet build
    dotnet test
  displayName: 'Build and Test'

- task: PublishBuildArtifacts@1
  inputs:
    PathtoPublish: '$(Build.ArtifactStagingDirectory)'
    ArtifactName: 'drop'
