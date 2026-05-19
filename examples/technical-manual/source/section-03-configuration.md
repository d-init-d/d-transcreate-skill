# Section 3: Configuration

## The ForgeFile

Every StreamForge pipeline is defined by a **ForgeFile** — a YAML document that declares stages, connectors, transformations, and operational policies. ForgeFiles follow a strict schema validated by `sfctl` before deployment.

A minimal ForgeFile looks like this:

```yaml
apiVersion: streamforge.dev/v1
kind: Pipeline
metadata:
  name: user-events-to-warehouse
  namespace: analytics
spec:
  schedule: "*/15 * * * *"
  stages:
    - name: extract-events
      connector: kafka-source
      config:
        brokers: ["kafka-01:9092", "kafka-02:9092"]
        topic: user.events
        group: sf-analytics
    - name: transform
      processor: sql
      config:
        query: |
          SELECT user_id, event_type, timestamp,
                 JSON_EXTRACT(payload, '$.page') AS page
          FROM input
          WHERE event_type IN ('page_view', 'click')
    - name: load-warehouse
      connector: bigquery-sink
      config:
        project: acme-data
        dataset: analytics
        table: user_events_processed
        write_mode: append
```

## Configuration Parameters

### Global Settings

Global settings are defined in the platform configuration file (`streamforge.yaml`) and apply to all pipelines unless overridden:

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `worker.concurrency` | integer | 4 | Maximum number of stages executed in parallel per worker node. |
| `worker.memory_limit` | string | `"2Gi"` | Memory limit for each worker process. Uses Kubernetes resource notation. |
| `scheduler.retry_policy.max_attempts` | integer | 3 | Maximum retry attempts for a failed stage before marking the pipeline as failed. |
| `scheduler.retry_policy.backoff_base` | duration | `"30s"` | Base duration for exponential backoff between retries. |
| `registry.schema_validation` | boolean | true | Whether to enforce schema validation on connector inputs and outputs. |
| `observability.trace_sampling_rate` | float | 0.1 | Fraction of executions sampled for distributed tracing (0.0 to 1.0). |

### Pipeline-Level Overrides

Any global setting can be overridden at the pipeline level by adding an `overrides` block to the ForgeFile:

```yaml
spec:
  overrides:
    worker.concurrency: 8
    scheduler.retry_policy.max_attempts: 5
```

### Environment Variables

StreamForge reads the following environment variables at startup:

| Variable | Required | Description |
|----------|----------|-------------|
| `SF_CLUSTER_ID` | Yes | Unique identifier for this StreamForge cluster. |
| `SF_REGISTRY_URL` | Yes | URL of the Registry Service endpoint. |
| `SF_LOG_LEVEL` | No | Logging verbosity: `debug`, `info`, `warn`, `error`. Defaults to `info`. |
| `SF_METRICS_PORT` | No | Port for the Prometheus metrics endpoint. Defaults to `9090`. |
| `SF_ENCRYPTION_KEY` | Yes (prod) | Base64-encoded 256-bit AES key for encrypting sensitive connector credentials at rest. |

### Connector Configuration

Each connector has its own configuration schema documented in the Connector Registry. Use `sfctl connector describe <name>` to view the schema for a specific connector. Common patterns include authentication credentials (passed via Kubernetes secrets), connection pooling parameters, and batch size tuning.
