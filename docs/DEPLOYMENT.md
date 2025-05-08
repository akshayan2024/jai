# JAI API Deployment Pipeline

This document outlines the deployment process for the JAI API, including environment setup, testing, and production deployment.

## Environments

The JAI API deployment pipeline consists of the following environments:

1. **Development**: Local environment for developers
2. **Testing**: Automated testing environment
3. **Staging**: Pre-production environment
4. **Production**: Live production environment

## Deployment Pipeline Overview

The deployment pipeline follows these stages:

```
Code Change → Automated Tests → Build → Stage Deployment → Production Deployment
```

## Development Environment

### Local Setup

1. Clone the repository
   ```bash
   git clone https://github.com/your-org/jai-api.git
   cd jai-api
   ```

2. Create a virtual environment
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install development dependencies
   ```bash
   pip install -r requirements/dev.txt
   ```

4. Run the API in development mode
   ```bash
   uvicorn jai_api.main:app --reload
   ```

### Docker Development Environment

Alternatively, use Docker for development:

```bash
docker-compose -f docker/docker-compose.dev.yml up
```

## Continuous Integration

### Pre-commit Hooks

The repository uses pre-commit hooks for code quality:

```bash
pre-commit install
```

### Automated Testing

Tests run automatically on pull requests:

1. Static code analysis (flake8, mypy)
2. Unit tests (pytest)
3. Integration tests
4. Coverage reporting

## Build Process

### Docker Image

The API is packaged as a Docker image:

```bash
docker build -t jai-api:latest -f docker/Dockerfile .
```

### Image Tagging

Images are tagged with:
- Semantic version (from git tags)
- Commit SHA
- Environment (dev/staging/prod)

## Staging Deployment

### Infrastructure

The staging environment mirrors production but with reduced resources:

- Kubernetes cluster with 2 pod replicas
- PostgreSQL database (if needed)
- Redis cache (if needed)
- API Gateway

### Deployment Process

1. Deploy to staging from CI/CD pipeline:
   ```bash
   kubectl apply -f k8s/staging/
   ```

2. Run smoke tests to verify basic functionality
3. Run performance tests to ensure acceptable response times

## Production Deployment

### Infrastructure

Production runs on:

- Kubernetes cluster with auto-scaling (3-10 pods)
- Managed database service with replication
- Redis cache cluster for performance
- CDN for static assets (if any)
- API Gateway with rate limiting

### Deployment Strategy

The production deployment uses a rolling update strategy:

1. Deploy new version to a subset of pods
2. Monitor health and performance
3. Gradually roll out to all pods
4. Roll back automatically if health checks fail

### Deployment Command

```bash
kubectl apply -f k8s/production/
```

## Monitoring and Observability

The deployed API is monitored using:

1. **Health Checks**: Regular probes to /health endpoint
2. **Metrics**: Prometheus metrics for system and business KPIs
3. **Logging**: Structured logs sent to centralized logging system
4. **Tracing**: Distributed tracing for request flows
5. **Alerts**: Configured for critical service degradation

## Backup and Disaster Recovery

1. Database backups run daily
2. Point-in-time recovery capability
3. Multi-region failover option for high availability
4. Regular disaster recovery drills

## Security Considerations

1. Secrets management through environment variables or secret stores
2. Regular security scans of container images
3. Network policies to restrict pod-to-pod communication
4. API authentication and authorization

## Rollback Procedure

In case of deployment issues:

1. Identify the problem through monitoring
2. Roll back to previous version:
   ```bash
   kubectl rollout undo deployment/jai-api
   ```
3. Investigate root cause
4. Fix issues in development and follow the deployment process again 