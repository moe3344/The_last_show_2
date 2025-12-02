import json
import boto3
import uuid
import os

polly = boto3.client('polly')
s3 = boto3.client('s3')
BUCKET = os.environ['BUCKET_NAME']

def handler(event, context):
    try:
        body = json.loads(event['body'])
        text = body['text']
        obituary_id = body.get('obituary_id', str(uuid.uuid4()))

        # Generate speech
        response = polly.synthesize_speech(
            Text=text,
            OutputFormat='mp3',
            VoiceId='Joanna',
            Engine='standard'
        )

        audio_data = response['AudioStream'].read()
        key = f"audio/{obituary_id}.mp3"

        # Upload to S3
        s3.put_object(
            Bucket=BUCKET,
            Key=key,
            Body=audio_data,
            ContentType='audio/mpeg',
 
        )

        url = f"https://{BUCKET}.s3.amazonaws.com/{key}"

        return {
            'statusCode': 200,
            'headers': {'Access-Control-Allow-Origin': '*'},
            'body': json.dumps({'audio_url': url})
        }
    except Exception as e:
          return {
              'statusCode': 500,
              'headers': {'Access-Control-Allow-Origin': '*'},
              'body': json.dumps({'error': str(e)})
          }
