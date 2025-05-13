# Real-Time Tracking System with Kafka and Python

## Overview

This project implements a real-time location tracking system using Apache Kafka as the messaging backbone. The system consists of two main components:

1. **Staff Application**: Allows staff members to send their current GPS location
2. **User Application**: Allows users to view real-time location updates on a map

## Features

- Real-time location updates using WebSockets
- Kafka-based message queue for reliable delivery
- Interactive map interface using Google Maps API
- Address lookup from coordinates
- Multiple user tracking with distinct markers

## System Architecture

```
Staff Browser (WebSocket) → Producer API (FastAPI) → Kafka → Consumer API (FastAPI + Socket.IO) → User Browser
```

## Prerequisites

- Python 3.7+
- Apache Kafka (local or cloud)
- Google Maps API key
- Geopy for address lookup

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/realtime-tracking-kafka.git
   cd realtime-tracking-kafka
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Set up Kafka:
   - For local setup, follow the instructions in the Kafka documentation
   - For Confluent Cloud, configure your cloud credentials

4. Set environment variables:
   ```bash
   export KAFKA_BOOTSTRAP_SERVERS="your-kafka-server:9092"
   export GOOGLE_MAPS_API_KEY="your-api-key"
   ```

## Configuration

Edit the following files to match your environment:

1. `producer.py` and `consumer.py`:
   - Update Kafka bootstrap servers
   - Adjust topic names if needed

2. HTML templates:
   - Replace `YOUR_GOOGLE_MAPS_API_KEY` in both template files

## Running the System

1. Start Kafka (if running locally)

2. In separate terminals:
   ```bash
   # Start the producer (staff app)
   python producer.py

   # Start the consumer (user app)
   python consumer.py
   ```

3. Access the applications:
   - Staff interface: http://localhost:8000/staff
   - User interface: http://localhost:8001/

## Usage

### Staff Application

1. Open the staff interface in your browser
2. Enter your user ID (default: "staff-1")
3. Click "Send My Location" to share your current GPS coordinates
4. The system will automatically send updates to Kafka

### User Application

1. Open the user interface in your browser
2. View real-time location updates on the map
3. Tracked users appear as colored markers with identifiers
4. Address information is displayed in the user list

## Project Structure

```
realtime-tracking-kafka/
├── producer.py            # Staff app and Kafka producer
├── consumer.py            # User app and Kafka consumer
├── templates/
│   ├── staff.html         # Staff interface
│   └── user.html          # User interface
├── static/                # Static files (CSS, JS)
├── requirements.txt       # Python dependencies
└── README.md              # This file
```

## Troubleshooting

1. **No location updates appearing**:
   - Verify Kafka is running
   - Check browser console for WebSocket errors
   - Confirm Google Maps API key is valid

2. **Geolocation errors**:
   - Ensure browser has location permissions
   - Verify secure context (HTTPS or localhost)

3. **Kafka connection issues**:
   - Check bootstrap servers configuration
   - Verify topic exists and is accessible

## Future Enhancements

- [ ] Add user authentication
- [ ] Store location history in database
- [ ] Implement geofencing alerts
- [ ] Add mobile app support
- [ ] Improve error handling and logging

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- Apache Kafka
- FastAPI
- Socket.IO
- Google Maps API
- GeopyY

##system design for the indane gas delivery.

###functional requirements:

1. consumer can send its location and get the location of the producer in real time
2. producer can get locations of  all consumers and send its location to all other consumers.
   3.consumer cannot see other consumers.
3. producer can see all  others  consumers along with itself.
4. the traveled path by consumer would be visible with different color.

###non functional requirements:
high availability
scalable

###tool and technologies:
kafka : for realtime messeging
python- django for producer and admin  management
nextJs: for UI
