# Section 2: Installation

## Prerequisites

Before installing StreamForge, ensure your environment meets the following requirements:

- **Operating system:** Linux (Ubuntu 20.04+, Debian 11+, or RHEL 8+), macOS 12+, or Windows 10+ with WSL2.
- **Container runtime:** Docker 24.0 or later, or Podman 4.0 or later.
- **Kubernetes cluster:** Version 1.27 or later (required for production deployments; optional for local development).
- **CLI tools:** `kubectl` (matching your cluster version), `helm` 3.12+, and `curl`.
- **Hardware:** Minimum 4 CPU cores, 8 GB RAM, and 20 GB free disk space for a single-node development setup.

## Installing the StreamForge CLI

The StreamForge CLI (`sfctl`) is the primary interface for managing pipelines, connectors, and cluster operations. Install it using the platform package manager:

```bash
# macOS (Homebrew)
brew install streamforge/tap/sfctl

# Linux (APT)
curl -fsSL https://packages.streamforge.dev/gpg.key | sudo gpg --dearmor -o /usr/share/keyrings/streamforge.gpg
echo "deb [signed-by=/usr/share/keyrings/streamforge.gpg] https://packages.streamforge.dev/apt stable main" | sudo tee /etc/apt/sources.list.d/streamforge.list
sudo apt update && sudo apt install sfctl

# Windows (WSL2)
curl -fsSL https://install.streamforge.dev | bash
```

After installation, verify the CLI is working:

```bash
sfctl version
# Expected output: sfctl v2.4.1 (build 20240315)
```

## Deploying the Platform

For local development, StreamForge provides a single-command setup that launches all services in Docker containers:

```bash
sfctl platform init --mode local
sfctl platform start
```

This creates a local Kubernetes cluster using kind, deploys the Scheduler Service, Worker Pool, and Registry Service, and exposes the monitoring dashboard at `http://localhost:9400`.

For production deployments, use the Helm chart:

```bash
helm repo add streamforge https://charts.streamforge.dev
helm install streamforge streamforge/platform \
  --namespace streamforge \
  --create-namespace \
  --values production-values.yaml
```

Refer to Section 3 for configuration options available in `production-values.yaml`.
