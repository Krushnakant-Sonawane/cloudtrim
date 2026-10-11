# CloudTrim

A read-only AWS cost-waste scanner, deployed through a production-style CI/CD pipeline.

CloudTrim finds wasted spend (unattached EBS volumes, unused Elastic IPs, old snapshots)
and estimates monthly savings. It never modifies or deletes anything.

## Run locally

```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt -r requirements-dev.txt
pytest -q
uvicorn app.main:app --reload
```

Open http://localhost:8000/health and http://localhost:8000/docs

`/findings` needs AWS credentials with read-only EC2 access (`ec2:Describe*`).

## Run with Docker

```bash
docker build -t cloudtrim .
docker run -p 8000:8000 cloudtrim
```

## Pipeline (current)

- Lint (ruff) and unit tests (pytest + moto, no real AWS needed)
- Docker build and Trivy vulnerability scan
- Dependabot for pip, Docker and GitHub Actions

## Roadmap

- [x] Phase 1: app, Docker, CI
- [ ] Phase 2: Terraform (remote state, VPC, ECR)
- [ ] Phase 3: ECS Fargate + ALB + least-privilege IAM
- [ ] Phase 4: GitHub OIDC + auto-deploy to staging
- [ ] Phase 5: production approval gate + auto-rollback
- [ ] Phase 6: monitoring, alarms, Terraform in CI
