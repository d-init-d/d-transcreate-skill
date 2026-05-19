# Section 1: StreamForge Overview

## What Is StreamForge?

StreamForge is a data pipeline orchestration platform designed for teams that need to move, transform, and deliver data across distributed systems. It provides a declarative configuration language for defining pipelines, a scheduler for managing execution order, and a monitoring dashboard for observing pipeline health in real time.

Unlike traditional ETL tools that require manual coding for each integration, StreamForge uses a connector-based architecture. Each connector encapsulates the logic for reading from or writing to a specific data system — whether that is a relational database, a message queue, an object store, or a third-party API. Connectors are versioned independently and can be updated without redeploying the entire platform.

## Core Concepts

A **pipeline** in StreamForge consists of one or more **stages**. Each stage performs a single operation: extract data from a source, apply a transformation, or load data into a destination. Stages are connected by **channels**, which are typed, buffered message paths that handle backpressure automatically.

The **ForgeFile** is the primary configuration artifact. Written in YAML, a ForgeFile declares the pipeline's stages, their connectors, transformation logic, retry policies, and output routing. ForgeFiles are stored in version control alongside application code, enabling teams to review pipeline changes through standard pull-request workflows.

## Architecture

StreamForge runs as a set of microservices deployed on Kubernetes. The **Scheduler Service** manages pipeline execution timing and dependency resolution. The **Worker Pool** executes individual stages, scaling horizontally based on queue depth. The **Registry Service** stores connector metadata, schema definitions, and pipeline versions. All inter-service communication uses gRPC with Protocol Buffers for type safety and performance.

Observability is built in. Every stage execution emits structured logs, metrics, and distributed traces. The monitoring dashboard aggregates these signals and provides alerting rules that teams can configure per pipeline.
