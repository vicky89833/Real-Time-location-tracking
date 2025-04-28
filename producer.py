import json
from confluent_kafka import Producer
import time
import socketio
import socket
from fastapi import FastAPI, Request, WebSocket
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import uvicorn
from geopy.geocoders import Nominatim

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

# Kafka configuration
conf = {
    'bootstrap.servers': 'localhost:9092',  # Change to your Kafka server
    'client.id': socket.gethostname()
}
producer = Producer(conf)

geolocator = Nominatim(user_agent="tracking_app")

@app.get("/staff")
async def staff_page(request: Request):
    return templates.TemplateResponse("staff.html", {"request": request})

@app.websocket("/ws/location")
async def websocket_location(websocket: WebSocket):
    await websocket.accept()
    try:
        while True:
            data = await websocket.receive_text()
            try:
                location_data = json.loads(data)
                user_id = location_data.get("user_id")
                lat = location_data.get("lat")
                lng = location_data.get("lng")
                
                # Get address from coordinates
                location = geolocator.reverse(f"{lat}, {lng}")
                address = location.address if location else "Unknown location"
                
                message = {
                    "user_id": user_id,
                    "lat": lat,
                    "lng": lng,
                    "timestamp": int(time.time()),
                    "address": address
                }
                
                # Send to Kafka
                producer.produce("user-locations", value=json.dumps(message))
                producer.flush()
                
                await websocket.send_text(json.dumps({"status": "success"}))
            except json.JSONDecodeError:
                await websocket.send_text(json.dumps({"status": "error", "message": "Invalid JSON"}))
    except Exception as e:
        print(f"Error: {e}")
    finally:
        await websocket.close()

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
