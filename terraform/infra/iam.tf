data "aws_iam_policy_document" "ecs_assume" {
  statement {
    actions = ["sts:AssumeRole"]
    principals {
      type        = "Service"
      identifiers = ["ecs-tasks.amazonaws.com"]
    }
  }
}

# Execution role: lets ECS pull the image and write logs (used by ECS, not by your code)
resource "aws_iam_role" "execution" {
  name               = "${var.project}-execution-role"
  assume_role_policy = data.aws_iam_policy_document.ecs_assume.json
}

resource "aws_iam_role_policy_attachment" "execution" {
  role       = aws_iam_role.execution.name
  policy_arn = "arn:aws:iam::aws:policy/service-role/AmazonECSTaskExecutionRolePolicy"
}

# Task role: what the running app is allowed to do. Least privilege, read-only.
resource "aws_iam_role" "task" {
  name               = "${var.project}-task-role"
  assume_role_policy = data.aws_iam_policy_document.ecs_assume.json
}

data "aws_iam_policy_document" "task_readonly" {
  statement {
    sid = "ReadOnlyScan"
    actions = [
      "ec2:DescribeVolumes",
      "ec2:DescribeAddresses",
      "ec2:DescribeSnapshots",
    ]
    resources = ["*"] # Describe* calls do not support resource-level permissions
  }
}

resource "aws_iam_role_policy" "task_readonly" {
  name   = "${var.project}-readonly-scan"
  role   = aws_iam_role.task.id
  policy = data.aws_iam_policy_document.task_readonly.json
}
