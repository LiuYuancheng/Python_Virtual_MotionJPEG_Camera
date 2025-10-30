# Python_Virtual_Motion-JPEG_Camera_Simulator

**Project Design Purpose** : This project is designed to create a lightweight, extensible camera-simulation service program that exposes a Motion-JPEG (MJPEG) video stream over HTTP via a Flask web interface for the cyber ranges, red/blue exercises, and research where realistic camera endpoints are required without physical hardware. The simulated video stream can be generated from five different type of source:

- Local physical camera (embedded webcam or USB camera).

- External live stream (RTSP/HTTP source).

- Static or rotating image dataset (images loaded from a directory).

- OS Screen Recording (full or partial screen screenshot).

- Application-window capture (Windows-only; capture a running app window).

The simulator intentionally mimics the web UI and behavior of [Axis IP cameras](https://www.axis.com/en-sg) so it can be deployed as a believable camera honeypot or as a drop-in replacement for testing and integration. We will also show a use case of how this project is used to simulate 4 different cyber in the cyber range.

```python
# Author:      Yuancheng Liu
# Created:     2025/10/15 
# version:     v_0.0.3
# Copyright:   Copyright (c) 2025 LiuYuancheng
# License:     GNU General Public License V3
```

**Table of Contents** 

[TOC]

------

### Introduction

The Python Virtual Motion-JPEG Camera Simulator is a system that simulate the IP camera via VM and dockers to provide a realistic MJPEG camera endpoint that browsers or client programs can consume for testing, monitoring, or attack-scenario playback. The project contents 3 main parts as shown in the project architecture diagram:

![](doc/img/s_03.png)

- **Virtual Camera Client Lib**: A library module to convert five different video resource (physical camera, video stream, image dataset, screenshot, app window image captured) to Motion-JPEG (MJPEG) video stream with the user configured FPS rate. 
- **Flask Camera Server**: A Flask IP camera management website follows Axis-style layout for the user to control the basic camera configuration, the video stream API accessment, user control and view the simulated video stream. 
- **Multi-Camera View Monitor Dashboard** : A multi frame camera video display dashboard for display all the camera in one window for the user to monitor or project all camera's vide in big one screen.

#### Key Features of the System

**Flask-based web UI** that follows Axis-style layout and endpoints to improve realism for attackers and integration with existing tooling.

**MJPEG streaming** served over HTTP for maximum compatibility with browsers and common video clients.

**Five configurable capture sources**:

1. Local physical camera (embedded webcam or USB camera).
2. External live stream (RTSP/HTTP source).
3. Static or rotating image dataset (images loaded from a directory).
4. Desktop capture (full or partial screen screenshot).
5. Application-window capture (Windows-only; capture a running app window).

**Honeypot capability** — logging and optional telemetry capture of incoming connections and attacker interactions to build attack datasets.

**Multi-instance support** — run multiple virtual cameras simultaneously to represent an enterprise deployment or aggregated feeds on a dashboard.

**Simple API/config** for selecting sources, stream properties (frame rate, resolution), and logging behavior.



------

