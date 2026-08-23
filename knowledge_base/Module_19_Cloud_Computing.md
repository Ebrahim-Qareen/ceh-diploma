---
source: web research (official CEH v13 syllabus) + Module 9 miscellaneous topics.pdf (instructor deck, partial)
session: 10
gap_topic: true (instructor deck covers basics only — this file supplements with full CEH scope)
---

# Module 19 — Cloud Computing

> The instructor deck (Module 9) covers cloud deployment/service models
> only. This file supplements with full CEH Ch.19 security content from
> official syllabus topics and web sources.

## Official learning objectives (CEH Ch.19)

1. Explain Cloud Computing Concepts
2. Explain Container Technology and Serverless Computing
3. Explain Cloud Computing Threats and Attacks
4. Explain Cloud Security Techniques, Tools, and Best Practices

## 1. Cloud Computing Concepts (from instructor deck)

On-demand computer services delivered over the internet.

### Deployment Models

| Model | Access | Example |
|---|---|---|
| Public | Open to all | AWS, Azure, GCP |
| Private | Restricted to one organization | On-prem OpenStack, VMware vSphere |
| Hybrid | Mix of public and private | Azure Arc, AWS Outposts |
| Community | Shared among specific organizations | Government clouds, healthcare consortiums |

### Service Models

| Model | You manage | Provider manages | Examples |
|---|---|---|---|
| IaaS | OS, apps, data | Hardware, networking, virtualization | AWS EC2, Azure VMs, GCP Compute |
| PaaS | Apps, data | OS, runtime, middleware, hardware | Heroku, Google App Engine, Azure App Service |
| SaaS | Data (configuration only) | Everything else | Gmail, Office 365, Salesforce |

## 2. Shared Responsibility Model

| Layer | IaaS | PaaS | SaaS |
|---|---|---|---|
| Data | Customer | Customer | Customer |
| Applications | Customer | Customer | Provider |
| OS | Customer | Provider | Provider |
| Network controls | Shared | Provider | Provider |
| Physical infrastructure | Provider | Provider | Provider |

**Key concept:** "security OF the cloud" (provider's job) vs "security IN
the cloud" (customer's job).

## 3. Container Technology

**Containers** = lightweight, isolated application environments sharing the
host OS kernel. Faster startup and less overhead than VMs.

| Concept | Description |
|---|---|
| Docker | Container runtime — build, ship, run containers |
| Kubernetes (K8s) | Container orchestration — deploy, scale, manage containers |
| Container image | Immutable template for creating containers |
| Container registry | Repository for container images (Docker Hub, ECR, ACR) |

### Container Security Risks

- Vulnerable base images (outdated, unpatched)
- Misconfigured containers (running as root, exposed ports)
- Container escape (break out of container to host OS)
- Insecure container registries (unauthenticated access)
- Secrets in images (hardcoded credentials, API keys)
- Supply chain attacks (compromised images in public registries)

## 4. Serverless Computing

Code runs in provider-managed ephemeral containers. Developer writes
functions, provider handles everything else.

**Examples:** AWS Lambda, Azure Functions, Google Cloud Functions.

**Security risks:** function event injection, insecure function permissions,
inadequate monitoring (short-lived execution), third-party dependency
vulnerabilities.

## 5. Cloud Threats and Attacks

| Threat/Attack | Description |
|---|---|
| Data breach | Unauthorized access to cloud-stored data |
| Data loss | Accidental deletion, provider failure, ransomware |
| Account/service hijacking | Stolen credentials → full cloud account control |
| Insecure APIs | Unauthenticated or weakly authenticated cloud APIs |
| Misconfigured storage | Public S3 buckets, open Azure Blob Storage |
| Insufficient IAM | Over-permissive roles, no MFA, shared credentials |
| Insider threats | Malicious or negligent cloud admins |
| DoS/DDoS | Overwhelm cloud services (cost amplification attack) |
| Side-channel attacks | Co-tenant attacks in shared infrastructure |
| Cryptojacking | Unauthorized cryptocurrency mining on cloud resources |
| Wrapping attacks | Manipulate SOAP messages in cloud web services |
| Man-in-the-Cloud | Steal cloud sync tokens to access cloud storage |

### S3 Bucket Misconfiguration (common exam topic)

Publicly accessible S3 buckets exposing sensitive data. Tools to find:
`aws s3 ls s3://bucket-name`, Bucket Finder, GrayhatWarfare, Shodan.

## 6. Cloud Security Best Practices

- Implement least-privilege IAM policies
- Enable MFA for all cloud accounts (especially root/admin)
- Encrypt data at rest and in transit
- Regular audit of cloud configurations (AWS Config, Azure Policy, GCP Security Command Center)
- Use cloud-native security tools (GuardDuty, Security Hub, Defender for Cloud)
- Monitor and log all API calls (CloudTrail, Azure Monitor, GCP Audit Logs)
- Implement network segmentation (VPCs, security groups, NACLs)
- Regular vulnerability scanning of cloud resources
- Secure container images (scan with Trivy, Snyk, Clair)
- Implement CIS Benchmarks for cloud configuration
- Use Cloud Access Security Broker (CASB) for visibility
- Regular backup and disaster recovery testing
- Penetration testing (within provider's acceptable use policy)

## 7. Cloud Security Tools

| Tool | Purpose |
|---|---|
| ScoutSuite | Multi-cloud security auditing |
| Prowler | AWS security best practices assessment |
| CloudSploit | Cloud misconfiguration detection |
| Pacu | AWS exploitation framework |
| Trivy | Container image vulnerability scanner |
| CASB solutions | Cloud access visibility and control (Netskope, McAfee MVISION) |
