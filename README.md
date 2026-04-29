---
# Supply Chain Intelligence System

> Real-time IoT fleet monitoring with AI-driven risk alerts — built on a Medallion Architecture using Kafka, MinIO, and Streamlit.

## What it solves
Global logistics teams drown in raw telemetry but lack actionable intelligence. This system converts high-frequency GPS and temperature data into proactive risk alerts — automatically flagging shipments in severe weather or exceeding thermal thresholds before damage occurs.

## What it does
- Ingests real-time IoT telemetry via Kafka into a Bronze data layer (MinIO/S3)
- Enriches raw coordinates with reverse geocoding + live weather API data in parallel (Silver layer)
- Surfaces a real-time Control Tower dashboard with fleet-wide risk alerts and shipment-level tracking (Gold layer)

## Architecture: Medallion Framework
| Layer | Role | Tech |
|-------|------|------|
| Bronze | Raw ingestion, immutable storage | Kafka, MinIO |
| Silver | Parallel enrichment (geocoding + weather) | ThreadPoolExecutor, Geopy, Weather API |
| Gold | Risk dashboard, precision tracking | Streamlit |

## Tech Stack
- **Languages:** Python 3.12 (Pandas, Requests, Geopy)
- **Infrastructure:** Kafka, MinIO, Docker Compose
- **Visualization:** Streamlit (real-time geospatial mapping)
- **Performance:** Multi-threaded parallel API enrichment via ThreadPoolExecutor

## Run it yourself
```bash
docker-compose up -d
python producer.py
python refine_with_weather.py
streamlit run app.py
```

## Engineering decisions
- **Parallel API calls:** ThreadPoolExecutor parallelizes geocoding and weather requests, preventing pipeline stalls during rate-limiting or timeouts.
- **Medallion separation:** Immutable Bronze layer ensures raw data is never overwritten, enabling full reprocessing if enrichment logic changes.
- **Containerised infra:** Docker Compose ensures single-command reproducibility across environments.
---
