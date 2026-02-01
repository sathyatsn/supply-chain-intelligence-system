# Supply Chain Intelligence System: A Medallion Architecture Implementation

### Business Problem and Project Necessity
Global logistics operations frequently face a visibility gap where raw data is abundant but actionable intelligence is scarce. High-frequency IoT telemetry—such as GPS coordinates and temperature readings—provides a pulse on a fleet but lacks the environmental context necessary for proactive risk management.

This system was engineered to address three specific operational challenges:
* **Contextual Blindness**: Converting abstract latitude and longitude into human-readable locations to identify regional accountability.
* **Environmental Risk Mitigation**: Automatically cross-referencing fleet positions with real-time weather and thermal data to identify shipments at risk of damage or spoilage.
* **Processing Throughput**: Implementing high-performance engineering to ensure a global fleet can be audited in minutes rather than hours.

### Technical Architecture: The Medallion Framework
The system implements a three-tier data lake architecture to maintain data integrity and support complex enrichment:
* **Bronze Layer (Ingestion)**: Captures raw IoT telemetry from message brokers and stores it as immutable data in S3-compatible object storage.
* **Silver Layer (Enrichment)**: A parallelized refinery that performs reverse geocoding and weather API integration. This layer transforms raw coordinates into validated location names and environmental context.
* **Gold Layer (Actionable Intelligence)**: A specialized control tower that surfaces high-risk alerts and provides precision tracking for stakeholders.



### Tech Stack
* **Languages**: Python (Pandas, Requests, Geopy).
* **Infrastructure**: Kafka (Message Broker), MinIO (Object Storage), Docker Compose.
* **Data Processing**: Multi-threaded ThreadPoolExecutor for parallel API enrichment.
* **Visualization**: Streamlit for real-time geospatial mapping and risk dashboarding.
* **Database**: PostgreSQL for structured metadata management.

### Data Engineering and Performance Optimization
A significant engineering challenge involved managing high-latency external API calls without stalling the pipeline. To maintain production-grade processing speeds:
* I implemented a **ThreadPoolExecutor** to parallelize requests, allowing the system to handle multiple wait states simultaneously.
* The refinery includes robust **exception handling** and verification fallbacks to ensure pipeline stability during network timeouts or rate-limiting events.
* The system successfully managed and enriched data for a diverse global fleet, identifying hundreds of high-risk shipments in a single audit cycle.

### Operational Visibility and Visuals
The final dashboard provides a dual-view interface for logistics oversight:
* **Precision Tracking**: Allows managers to spotlight a specific shipment to view its current position, localized weather conditions, and precise temperature metrics.
* **Fleet Overview**: Aggregates the entire global registry, automatically highlighting shipments in regions experiencing severe weather or exceeding thermal thresholds.



### Collaborative Development Methodology
This system was developed through a collaborative "vibe coding" framework, utilizing an adaptive AI mentor to accelerate the project lifecycle. This approach facilitated:
* Rapid prototyping of the parallel refinery logic and API integration.
* Efficient troubleshooting of infrastructure hurdles, including container orchestration and remote repository configurations.
* A focus on bridging the gap between raw data engineering and executive-ready intelligence.

### Execution Instructions
1. **Initialize Infrastructure**: Deploy the environment using `docker-compose up -d`.
2. **Data Ingestion**: Execute the ingestion scripts to populate the Bronze layer.
3. **Data Refinery**: Run `python refine_with_weather.py` to perform parallel enrichment.
4. **Launch Dashboard**: Execute `streamlit run app.py` to open the Control Tower.
