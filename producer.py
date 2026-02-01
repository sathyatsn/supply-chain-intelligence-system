import json
import time
import random
from faker import Faker
from confluent_kafka import Producer

# 1. Initialize Faker for generating realistic data
fake = Faker()

# 2. Configure the Kafka Producer
# 'localhost:9092' is where your Docker Kafka container is listening
conf = {'bootstrap.servers': 'localhost:9092'}
producer = Producer(conf)


def delivery_report(err, msg):
    """ Called once for each message produced to indicate delivery result. """
    if err is not None:
        print(f"❌ Message delivery failed: {err}")
    else:
        print(f"✅ Message delivered to {msg.topic()} [{msg.partition()}]")


def generate_shipment_event():
    """ Creates a fake shipment 'ping' event """
    # List of common supply chain statuses
    statuses = ['In Transit', 'Delayed', 'At Warehouse', 'Out for Delivery']

    event = {
        "shipment_id": f"TRK-{random.randint(1000, 9999)}",
        "timestamp": time.strftime('%Y-%m-%dT%H:%M:%S'),
        "origin_city": fake.city(),
        "destination_city": "Farmington Hills",  # Focus on your Michigan location!
        "latitude": float(fake.latitude()),
        "longitude": float(fake.longitude()),
        "status": random.choices(statuses, weights=[0.7, 0.1, 0.1, 0.1])[0],
        "temperature_c": round(random.uniform(-5.0, 30.0), 1)  # IoT sensor data
    }
    return event


# 3. The Main Loop: Send data every 2 seconds
print("🚀 Starting Supply Chain Stream... Press Ctrl+C to stop.")
try:
    while True:
        shipment_data = generate_shipment_event()

        # Send data to a topic named 'raw_shipments'
        producer.produce(
            'raw_shipments',
            key=shipment_data['shipment_id'],
            value=json.dumps(shipment_data),
            callback=delivery_report
        )

        # 'Poll' handles the delivery report callbacks
        producer.poll(0)
        time.sleep(2)

except KeyboardInterrupt:
    print("\n🛑 Stopping the stream.")
finally:
    producer.flush()  # Ensure all messages are sent before exiting