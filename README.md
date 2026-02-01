# Supply Chain Intelligence System: A Medallion Architecture Implementation

### Project Genesis and Development Philosophy
This system is an original application concept designed to solve the "Visibility Gap" in global logistics. To bring this complex architecture to life, I utilized a **"Vibe Coding"** methodology—leveraging **Gemini** and **AI Agents** as collaborative engineering partners. This approach allowed me to maintain a high-level focus on system design and business logic while using AI to accelerate the development of robust, production-grade components.

### Business Problem and Project Necessity
Global logistics operations frequently face a visibility gap where raw data is abundant but actionable intelligence is scarce. High-frequency IoT telemetry—such as GPS coordinates and temperature readings—provides a pulse on a fleet but lacks the environmental context necessary for proactive risk management.

This system was engineered to address three specific operational challenges:
* **Contextual Blindness**: Converting abstract latitude and longitude into human-readable locations to identify regional accountability.
* **Environmental Risk Mitigation**: Automatically cross-referencing fleet positions with real-time weather and thermal data to identify shipments at risk.
* **Processing Throughput**: Implementing high-performance engineering to ensure a global fleet can be audited in minutes rather than hours.

### Technical Architecture: The Medallion Framework
The system implements a three-tier data lake architecture to maintain data integrity and support complex enrichment:

* **Bronze Layer (Ingestion)**: Captures raw IoT telemetry from message brokers and stores it as immutable data.
> **[Insert Screenshot of MinIO Console showing raw JSON files here]**

* **Silver Layer (Enrichment)**: A parallelized refinery that performs reverse geocoding and weather API integration. This transforms raw coordinates into validated location names.

* **Gold Layer (Actionable Intelligence)**: A specialized control tower providing precision tracking and risk alerts.
> **[Insert Screenshot of Streamlit Dashboard map and alerts here]**

### Tech Stack and Infrastructure
* **Languages**: Python (Pandas, Requests, Geopy).
* **Infrastructure**: Kafka (Message Broker), MinIO (Object Storage), Docker Compose.
* **Messaging**: Managed via a Kafka UI for real-time stream monitoring.
> **[Insert Screenshot of Kafka UI showing active topics here]**
* **Data Processing**: Multi-threaded ThreadPoolExecutor for parallel API enrichment.
* **Visualization**: Streamlit for real-time geospatial mapping.

### Data Engineering and Performance Optimization
A significant engineering challenge involved managing high-latency external API calls. By utilizing the "vibe coding" framework with AI agents, I was able to rapidly iterate on a **ThreadPoolExecutor** implementation. This parallelization allows the system to handle multiple API wait-states simultaneously, ensuring that the processing of a global fleet remains efficient and scalable.

### Execution Instructions
1. **Initialize Infrastructure**: Deploy the environment using `docker-compose up -d`.
2. **Data Ingestion**: Execute the ingestion scripts to populate the Bronze layer.
3. **Data Refinery**: Run `python refine_with_weather.py` to perform parallel enrichment.
4. **Launch Dashboard**: Execute `streamlit run app.py` to open the Control Tower.
