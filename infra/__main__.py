import pulumi
import pulumi_aws as aws
import json

# ========================================
# Configuration
# ========================================
stack = pulumi.get_stack()
project = pulumi.get_project()

def name(resource: str) -> str:
    """Generate resource name: project-resource-stack"""
    return f"{project}-{resource}-{stack}"

tags = {
    "Project": project,
    "Environment": stack,
}

# ========================================
# S3 Buckets
# ========================================

# Images bucket
  # Images bucket - allow public read access
images_bucket = aws.s3.Bucket(
      name("images"),
      bucket=name("images"),
      cors_rules=[
          aws.s3.BucketCorsRuleArgs(
              allowed_headers=["*"],
              allowed_methods=["GET", "HEAD"],
              allowed_origins=[
                  "http://localhost:3000",
                  "https://*",
              ],
              max_age_seconds=3000,
          )
      ],
      tags=tags,
  )

  # Make images bucket publicly readable
images_bucket_public_access_block = aws.s3.BucketPublicAccessBlock(
      name("images-public-access"),
      bucket=images_bucket.id,
      block_public_acls=False,
      block_public_policy=False,
      ignore_public_acls=False,
      restrict_public_buckets=False,
  )

images_bucket_ownership_controls = aws.s3.BucketOwnershipControls(
      name("images-ownership"),
      bucket=images_bucket.id,
      rule=aws.s3.BucketOwnershipControlsRuleArgs(
          object_ownership="BucketOwnerPreferred",
      ),
  )

images_bucket_policy = aws.s3.BucketPolicy(
      name("images-policy"),
      bucket=images_bucket.id,
      policy=images_bucket.arn.apply(lambda arn: {
          "Version": "2012-10-17",
          "Statement": [{
              "Sid": "PublicReadGetObject",
              "Effect": "Allow",
              "Principal": "*",
              "Action": ["s3:GetObject"],
              "Resource": [f"{arn}/*"]
          }]
      }),
      opts=pulumi.ResourceOptions(depends_on=[images_bucket_public_access_block]),
  )

  # Audio bucket - allow public read access
audio_bucket = aws.s3.Bucket(
      name("audio"),
      bucket=name("audio"),
      cors_rules=[
          aws.s3.BucketCorsRuleArgs(
              allowed_headers=["*"],
              allowed_methods=["GET", "HEAD"],
              allowed_origins=[
                  "http://localhost:3000",
                  "https://*",
              ],
              max_age_seconds=3000,
          )
      ],
      tags=tags,
  )

audio_bucket_public_access_block = aws.s3.BucketPublicAccessBlock(
      name("audio-public-access"),
      bucket=audio_bucket.id,
      block_public_acls=False,
      block_public_policy=False,
      ignore_public_acls=False,
      restrict_public_buckets=False,
  )

audio_bucket_ownership_controls = aws.s3.BucketOwnershipControls(
      name("audio-ownership"),
      bucket=audio_bucket.id,
      rule=aws.s3.BucketOwnershipControlsRuleArgs(
          object_ownership="BucketOwnerPreferred",
      ),
  )

audio_bucket_policy = aws.s3.BucketPolicy(
      name("audio-policy"),
      bucket=audio_bucket.id,
      policy=audio_bucket.arn.apply(lambda arn: {
          "Version": "2012-10-17",
          "Statement": [{
              "Sid": "PublicReadGetObject",
              "Effect": "Allow",
              "Principal": "*",
              "Action": ["s3:GetObject"],
              "Resource": [f"{arn}/*"]
          }]
      }),
      opts=pulumi.ResourceOptions(depends_on=[audio_bucket_public_access_block]),
  )

# ========================================
# IAM Role for Lambda
# ========================================

lambda_role = aws.iam.Role(
    name("lambda-role"),
    assume_role_policy=json.dumps({
        "Version": "2012-10-17",
        "Statement": [{
            "Action": "sts:AssumeRole",
            "Effect": "Allow",
            "Principal": {"Service": "lambda.amazonaws.com"}
        }]
    }),
    tags=tags,
)

# Attach CloudWatch Logs policy
aws.iam.RolePolicyAttachment(
    name("lambda-logs-policy"),
    role=lambda_role.name,
    policy_arn="arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole"
)

# Custom policy for S3 and Polly
aws.iam.RolePolicy(
    name("lambda-s3-polly-policy"),
    role=lambda_role.id,
    policy=pulumi.Output.all(images_bucket.arn, audio_bucket.arn).apply(
        lambda arns: json.dumps({
            "Version": "2012-10-17",
            "Statement": [
                {
                    "Effect": "Allow",
                    "Action": ["s3:PutObject", "s3:GetObject"],
                    "Resource": [f"{arns[0]}/*", f"{arns[1]}/*"]
                },
                {
                    "Effect": "Allow",
                    "Action": "polly:SynthesizeSpeech",
                    "Resource": "*"
                }
            ]
        })
    )
)

# ========================================
# Lambda Functions
# ========================================

image_upload_lambda = aws.lambda_.Function(
    name("image-upload"),
    runtime="python3.11",
    role=lambda_role.arn,
    handler="index.handler",
    timeout=30,
    memory_size=256,
    environment={
        "variables": {
            "BUCKET_NAME": images_bucket.id,
        }
    },
    code=pulumi.AssetArchive({
        ".": pulumi.FileArchive("./lambda_functions/image_upload")
    }),
    tags=tags,
)

tts_lambda = aws.lambda_.Function(
    name("tts"),
    runtime="python3.11",
    role=lambda_role.arn,
    handler="index.handler",
    timeout=60,
    memory_size=512,
    environment={
        "variables": {
            "BUCKET_NAME": audio_bucket.id,
        }
    },
    code=pulumi.AssetArchive({
        ".": pulumi.FileArchive("./lambda_functions/text_to_speech")
    }),
    tags=tags,
)

# ========================================
# Lambda Function URLs (Instead of API Gateway!)
# ========================================

image_upload_url = aws.lambda_.FunctionUrl(
    name("image-upload-url"),
    function_name=image_upload_lambda.name,
    authorization_type="NONE",
    cors={
        "allow_origins": ["*"],
        "allow_methods": ["POST"],
        "allow_headers": ["content-type"],
        "max_age": 86400,
    }
)

tts_url = aws.lambda_.FunctionUrl(
    name("tts-url"),
    function_name=tts_lambda.name,
    authorization_type="NONE",
    cors={
        "allow_origins": ["*"],
        "allow_methods": ["POST"],
        "allow_headers": ["content-type"],
        "max_age": 86400,
    }
)

# ========================================
# Outputs
# ========================================

pulumi.export("images_bucket", images_bucket.id)
pulumi.export("audio_bucket", audio_bucket.id)
pulumi.export("image_upload_url", image_upload_url.function_url)
pulumi.export("tts_url", tts_url.function_url)