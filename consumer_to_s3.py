import json
import boto3
from confluent_kafka import Consumer, KafkaError
from datetime import datetime

# 1. Configure the S3 (MinIO) Client
s3_client = boto3.client(
    's3',
    endpoint_url='http://localhost:9000',  # Your MinIO address
    aws_access_key_id='admin',
    aws_secret_access_key='password123',
    region_name='us-east-1'
)

# 2. Configure the Kafka Consumer
kafka_conf = {
    'bootstrap.servers': 'localhost:9092',
    'group.id': 's3-writer-group',
    'auto.offset.reset': 'earliest'
}
consumer = Consumer(kafka_conf)
consumer.subscribe(['raw_shipments'])

BUCKET_NAME = 'supply-chain-raw'


def upload_to_minio(data, filename):
    """Saves the shipment JSON to your local S3 bucket"""
    try:
        s3_client.put_object(
            Bucket=BUCKET_NAME,
            Key=filename,
            Body=json.dumps(data)
        )
        print(f"📁 Saved to S3: {filename}")
    except Exception as e:
        print(f"❌ S3 Upload Failed: {e}")


# 3. The Main Loop
print("📥 Consumer started. Listening for shipments...")
try:
    while True:
        msg = consumer.poll(1.0)
        if msg is None: continue
        if msg.error():
            print(f"Consumer error: {msg.error()}")
            continue

        # Parse the message
        shipment_data = json.loads(msg.value().decode('utf-8'))

        # Create a unique filename based on ID and Timestamp
        filename = f"shipment_{shipment_data['shipment_id']}_{datetime.now().strftime('%H%M%S')}.json"

        # Save to S3
        upload_to_minio(shipment_data, filename)

except KeyboardInterrupt:
    print("🛑 Consumer stopped.")
finally:
    consumer.close()