
import json
import base64
import boto3
import uuid
import os

s3 = boto3.client('s3')
BUCKET = os.environ['BUCKET_NAME']

def handler(event, context):
      try:
          body = json.loads(event['body'])
          image_data = base64.b64decode(body['image'])
          filename = body.get('filename', 'image.jpg')

          # Generate unique name
          ext = filename.split('.')[-1]
          key = f"images/{uuid.uuid4()}.{ext}"

          # Upload to S3
          s3.put_object(
              Bucket=BUCKET,
              Key=key,
              Body=image_data,
              ContentType=f'image/{ext}',
          
          )

          url = f"https://{BUCKET}.s3.amazonaws.com/{key}"

          return {
              'statusCode': 200,
              'headers': {'Access-Control-Allow-Origin': '*'},
              'body': json.dumps({'image_url': url})
          }
      except Exception as e:
          return {
              'statusCode': 500,
              'headers': {'Access-Control-Allow-Origin': '*'},
              'body': json.dumps({'error': str(e)})
          }