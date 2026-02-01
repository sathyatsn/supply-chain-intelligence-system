import pandas as pd
import boto3
import json
import io

# 1. Connect to our Warehouse (MinIO)
s3_client = boto3.client(
    's3',
    endpoint_url='http://localhost:9000',
    aws_access_key_id='admin',
    aws_secret_access_key='password123',
    region_name='us-east-1'
)

RAW_BUCKET = 'supply-chain-raw'
SILVER_BUCKET = 'supply-chain-silver'


def refine_data():
    all_events = []

    # 2. "Sweep" the Raw Bucket for files
    print("🧹 Cleaning up the Raw Data...")
    response = s3_client.list_objects_v2(Bucket=RAW_BUCKET)

    if 'Contents' not in response:
        print("📭 No files found to refine.")
        return

    for obj in response['Contents']:
        file_content = s3_client.get_object(Bucket=RAW_BUCKET, Key=obj['Key'])
        data = json.loads(file_content['Body'].read().decode('utf-8'))
        all_events.append(data)

    # 3. Create a Dataframe (The "Spreadsheet" view)
    df = pd.DataFrame(all_events)

    # 4. Apply Business Logic: Flag High Temperature Risks
    # (Imagine you are shipping sensitive medical parts or food!)
    df['temp_alert'] = df['temperature_c'] > 25.0

    print(f"✅ Refined {len(df)} records.")
    print(df.head())  # Preview the data

    # 5. Save the "Silver" Table back to MinIO
    csv_buffer = io.StringIO()
    df.to_csv(csv_buffer, index=False)

    s3_client.put_object(
        Bucket=SILVER_BUCKET,
        Key='shipment_analytics_base.csv',
        Body=csv_buffer.getvalue()
    )
    print(f"🚀 Silver Table uploaded to bucket: {SILVER_BUCKET}")


if __name__ == "__main__":
    refine_data()