---
title: "Kubernetes v1.37: KubeletInUserNamespace (aka Rootless mode) Graduates to Beta"
date: 2026-09-05T16:14:58.674993+00:00
lastmod: 2026-09-05T16:14:58.674993+00:00
draft: false
slug: "kubernetes-v1-37-rootless-mode-beta"
url: "/devops/kubernetes-v1-37-rootless-mode-beta/"
categories: [devops, cloud]
summary: "Kubernetes v1.37 promotes the KubeletInUserNamespace feature gate to beta. This feature, known as rootless mode, allows all node components to run as a non-root user on the host, using a Linux user namespace. The work started as an experiment in 2018 and was merged into Kubernetes v1.22 in 2021 as an alpha feature."
excerpt: "Kubernetes v1.37 promotes the KubeletInUserNamespace feature gate to beta. This feature, known as rootless mode, allows all node components to run as a non-root user on the host, using a Linux user namespace. The work started as an experiment in 2018 and was merged into Kubernetes v1.22 in 2021 as an alpha feature."
canonical_url: ""
---

This article was auto-published by AI Blog Generation Agent.

Canonical WordPress URL: 

<h1>Kubernetes v1.37: KubeletInUserNamespace (aka Rootless mode) Graduates to Beta</h1>

<p>Kubernetes v1.37 promotes the <code>KubeletInUserNamespace</code> feature gate to beta. With this feature enabled, all of the node components (kubelet, CRI and OCI runtimes, CNI plugins, and kube-proxy) can run as a non-root user on the host, using a <a href="https://man7.org/linux/man-pages/man7/user_namespaces.7.html">Linux user namespace</a>. This technique is also known as <em>rootless mode</em>. The work started as an experiment in 2018 and was merged into Kubernetes v1.22 in 2021 as an alpha feature (Kubernetes Enhancement Proposal <a href="https://www.kubernetes.dev/resources/keps/2033/">KEP-2033</a>).</p>

<p>This feature should not be confused with <a href="https://kubernetes.io/docs/concepts/workloads/pods/user-namespaces/">user namespaces for pods</a> (<code>hostUsers: false</code>).</p>

<h2>Enterprise Impact</h2>

<p>As of 2026-09-05, Kubernetes v1.37 introduces the <code>KubeletInUserNamespace</code> feature, enabling non-root user execution across node components. This change is particularly beneficial for enterprises that require enhanced security and compliance measures. By allowing non-root user execution, organizations can mitigate risks associated with root-level access and improve overall security posture. This feature also simplifies the management of non-root users, reducing the need for additional security measures and improving operational efficiency.</p>

<h2>Sources</h2>

<ul>
  <li><a href="https://kubernetes.io/blog/2026/09/04/kubernetes-v1-37-rootless-beta/">Kubernetes Blog</a></li>
  <li><a href="https://news.google.com/rss/articles/CBMiXkFVX3lxTE1temFOYmpTeU9vekltdERRcDhQVEZqeHpqaEF5aEh1OXNtNVpBbjVBaG9MNjJXWFpTU3hHTkJrSm1nbExoTi1oeEpzTXZ3Vm5sU29RQ1FsV210dnhYRGc?oc=5">Blume: Zero-Config Docs Framework That Turns a Markdown Folder into an AI-Ready Website</a></li>
  <li><a href="https://github.blog/changelog/2026-09-04-gpt-6-astra-is-generally-available-in-github-copilot">GPT-6 Astra is generally available in GitHub Copilot</a></li>
  <li><a href="https://aws.amazon.com/blogs/devops/investigate-dms-migration-issues-with-aws-devops-agent/">Investigate DMS migration issues with AWS DevOps Agent</a></li>
</ul>
