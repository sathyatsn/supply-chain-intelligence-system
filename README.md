# Supply Chain Intelligence System: A Medallion Architecture Implementation

### Project Genesis and Development Methodology
This system is an original application concept designed to bridge the visibility gap in global logistics. The project was developed using a **"vibe coding"** methodology, leveraging **Gemini** and specialized **AI Agents** as collaborative engineering partners. This approach allowed for high-level architectural focus while utilizing AI to accelerate the implementation of complex components like parallel processing and real-time data streaming.

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
> [MinIO Silver Layer Storage]
> <img width="1502" height="830" alt="Screenshot 2026-01-31 at 23 23 08" src="https://github.com/user-attachments/assets/31ca4655-dafd-4534-9acc-82f5814ef48c" />

* **Gold Layer (Actionable Intelligence)**: A specialized control tower that surfaces high-risk alerts and provides precision tracking for stakeholders via a real-time dashboard.
> [Supply Chain Control Tower Dashboard]
> <img width="2552" height="1183" alt="image" src="https://github.com/user-attachments/assets/7c31767e-9db1-4266-81eb-01ef84fbf956" />


### Tech Stack
* **Languages**: Python (Pandas, Requests, Geopy).
* **Infrastructure**: Kafka (Message Broker), MinIO (Object Storage), Docker Compose.
* **Data Processing**: Multi-threaded ThreadPoolExecutor for parallel API enrichment.
* **Visualization**: Streamlit for real-time geospatial mapping and risk dashboarding.
* **Development Environment**: PyCharm with integrated Git version control.
> [PyCharm Git Configuration]
> <img width="1502" height="981" alt="Screenshot 2026-01-31 at 23 35 30" src="https://github.com/user-attachments/assets/a50a7b3d-b225-47f8-8dfd-9ac0ed26bd66" />


### Data Engineering and Performance Optimization
A significant engineering challenge involved managing high-latency external API calls without stalling the pipeline. With the assistance of AI agents to optimize the logic, I implemented a **ThreadPoolExecutor** to parallelize requests. This allows the system to handle multiple wait states simultaneously, ensuring pipeline stability during network timeouts or rate-limiting events. The system successfully managed and enriched data for a diverse global fleet in a single audit cycle.

### Operational Visibility
The dashboard provides a dual-view interface for logistics oversight:
* **Precision Tracking**: Allows managers to spotlight a specific shipment to view its current position and localized weather conditions.
* **Fleet Overview**: Aggregates the global registry, automatically highlighting shipments in regions experiencing severe weather or exceeding thermal thresholds.

### Execution Instructions
1. **Initialize Infrastructure**: Deploy the environment using `docker-compose up -d`.
2. **Data Ingestion**: Execute the ingestion scripts to populate the Bronze layer.
3. **Data Refinery**: Run `python refine_with_weather.py` to perform parallel enrichment.
4. **Launch Dashboard**: Execute `streamlit run app.py` to open the Control Tower.
