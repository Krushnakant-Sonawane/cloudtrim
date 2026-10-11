import boto3
from moto import mock_aws

from app.scanner import run_scan


@mock_aws
def test_finds_unattached_volume_and_unused_eip():
    ec2 = boto3.client("ec2", region_name="us-east-1")
    ec2.create_volume(Size=100, AvailabilityZone="us-east-1a")
    ec2.allocate_address(Domain="vpc")

    result = run_scan("us-east-1")

    types = {f["type"] for f in result["findings"]}
    assert "unattached_ebs_volume" in types
    assert "unused_elastic_ip" in types
    assert result["est_total_monthly_savings"] > 0


@mock_aws
def test_clean_account_has_no_findings():
    result = run_scan("us-east-1")
    assert result["count"] == 0
