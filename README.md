# Code_dhtlight_mobius


## Overview  

This project is an educational material aimed at understanding how IoT sensor data can be integrated with the Mobius (oneM2M) platform.
It demonstrates the oneM2M resource hierarchy (AE / CNT / CIN) and applies this structure to implement sensor data transmission and construct an end-to-end IoT backend pipeline.

---
<img width="1164" height="684" alt="image" src="https://github.com/user-attachments/assets/2a55611e-fe5d-4f57-864e-4986391b9394" />


## 🛠 설명 영상
https://github.com/user-attachments/assets/99d0ffd2-3198-4620-a0a6-6ff986e496f8
## 🛠 시연 영상
https://github.com/user-attachments/assets/68d3db16-8525-42ba-b354-d48be339c535


## Purpose  
The goal of this project is to:

- Understand the oneM2M resource hierarchy (AE / CNT / CIN)
- Learn how Mobius handles HTTP/MQTT communication
- Implement real sensor data transmission to Mobius
- Understand MQTT broker integration (Mosquitto)
- Store and manage IoT data using PostgreSQL
- Provide structured learning material for competition participants

---

## What this project demonstrates

### 1. Sensor Data Collection  
- DHT sensor (temperature / humidity)
- Light sensor
- Raspberry Pi-based data acquisition using Python

### 2. oneM2M Resource Understanding  
- AE creation concept
- CNT structure
- CIN data insertion

### 3. Platform & Communication Integration  
- JSON payload formatting
- Periodic data transmission
- HTTP and MQTT communication flow
- Mobius server interaction

### 4. Backend & Data Pipeline Structure  
- MQTT broker integration using Mosquitto
- Node.js-based backend processing
- Data storage in PostgreSQL (v17)
- Spatial extension support using PostGIS (if applicable)

---

## Technology Stack

### Device Layer
- Raspberry Pi
- Python
- DHT Sensor
- Light Sensor

### Platform Layer
- Mobius (oneM2M)

### Communication Layer
- HTTP
- MQTT
- Mosquitto (MQTT Broker)

### Server & Database Layer
- Node.js v22
- PostgreSQL v17
- PostGIS


---

## Platform Reference  
Mobius (oneM2M Platform)  
https://github.com/IoTKETI/Mobius  
License: BSD-3-Clause






