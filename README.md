# Python_Virtual_Motion-JPEG_Camera_Simulator

**Project Design Purpose** : This project is designed to create a lightweight, extensible camera-simulation service program that exposes a Motion-JPEG (MJPEG) video stream over HTTP via a Flask web interface for the cyber ranges, red/blue exercises, and research where realistic camera endpoints are required without physical hardware. The simulated video stream can be generated from five different type of source:

- Local physical camera (embedded webcam or USB camera).

- External live stream (RTSP/HTTP source).

- Static or rotating image dataset (images loaded from a directory).

- OS Desktop capture (full or partial screen screenshot).

- Application-window capture (Windows-only; capture a running app window).

The simulator intentionally mimics the web UI and behavior of [Axis IP cameras](https://www.axis.com/en-sg) so it can be deployed as a believable camera honeypot or as a drop-in replacement for testing and integration. 

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