"""CloudTrim scanner: read-only checks for wasted AWS spend.

Every price below is a rough us-east-1 estimate used only to rank findings.
The scanner never modifies or deletes anything.
"""
from datetime import UTC, datetime, timedelta

import boto3

EBS_GB_MONTH = 0.08        # gp3, per GB-month
SNAPSHOT_GB_MONTH = 0.05   # per GB-month
EIP_MONTH = 3.65           # $0.005/hr


def find_unattached_volumes(ec2):
    findings = []
    paginator = ec2.get_paginator("describe_volumes")
    for page in paginator.paginate(Filters=[{"Name": "status", "Values": ["available"]}]):
        for v in page["Volumes"]:
            findings.append({
                "type": "unattached_ebs_volume",
                "resource_id": v["VolumeId"],
                "detail": f"{v['Size']} GB volume not attached to any instance",
                "est_monthly_savings": round(v["Size"] * EBS_GB_MONTH, 2),
            })
    return findings


def find_unused_eips(ec2):
    findings = []
    for a in ec2.describe_addresses()["Addresses"]:
        if "AssociationId" not in a:
            findings.append({
                "type": "unused_elastic_ip",
                "resource_id": a.get("AllocationId", a.get("PublicIp")),
                "detail": "Elastic IP not associated with any resource",
                "est_monthly_savings": EIP_MONTH,
            })
    return findings


def find_old_snapshots(ec2, days=90):
    findings = []
    cutoff = datetime.now(UTC) - timedelta(days=days)
    paginator = ec2.get_paginator("describe_snapshots")
    for page in paginator.paginate(OwnerIds=["self"]):
        for s in page["Snapshots"]:
            if s["StartTime"] < cutoff:
                findings.append({
                    "type": "old_snapshot",
                    "resource_id": s["SnapshotId"],
                    "detail": f"{s['VolumeSize']} GB snapshot older than {days} days",
                    "est_monthly_savings": round(s["VolumeSize"] * SNAPSHOT_GB_MONTH, 2),
                })
    return findings


def run_scan(region="us-east-1", session=None):
    session = session or boto3.Session()
    ec2 = session.client("ec2", region_name=region)
    findings = (
        find_unattached_volumes(ec2)
        + find_unused_eips(ec2)
        + find_old_snapshots(ec2)
    )
    total = round(sum(f["est_monthly_savings"] for f in findings), 2)
    return {
        "region": region,
        "count": len(findings),
        "est_total_monthly_savings": total,
        "findings": findings,
    }
