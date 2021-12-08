# BCI_DOFBOT Client Subsystem

## Overview
This subsystem acts as a client that connects to a headset subsystem via the the SmartSockets and ClientInterfaceDriver libraries. It contains the main user code that utilizes the communication libraries mentioned above, GPIO, OLED, and Arm control libraries.

### File Structure
- main.py: The main entry code for this subsystem. Handles the user logic and system mode control.
- ClientInterfaceDriver.py: The Client driver communicates with the headset server driver via SmartSockets and implements the headset API for use by the client.
    - See CDL=>HERE for more details about the SmartSocket Library.
- control.py: The control library for the robotic arm. Handles moving the arm and taking pictures with the built in camera. This file uses the Yahboom Dofbot robotic arm driver library included in the system image.
- UserIOInteraction.py: This file simplifies the user interface widgets to allow for interaction with either the GPIO Buttons and OLED or only in the console. This file uses IODriver.py and OLEDDriver.py to interact with the GPIO and OLED display.
- IODriver.py: This file handles the instantiation and configuration of the Raspberry Pi GPIO for edge triggered events.
- OLEDDriver.py: This file handles the interface with the OLED display. It allows for writing/clearing one of three lines on the 128x32 OLED display.

### Other Files
- HeadsetAPIWrapperTest.py: This is a wrapper class that mimics the API described in ClientInterfaceDriver.py to allow for development and testing without the headset subsystem connected.
- splashscreen.py: This file is a script which moves the arm to a default position and resets the OLED screen. It can be run on startup/when triggered using the systemd service file bci_arm_main.service.

## Configuration and Running the System

### Client System (main program)

```bash
# Before running the system, make sure the headset server is running

# Make sure to change the configuration options described at the bottom of main.py in the main statement before running the system

# Run the client system with the following command
python3 main.py
```

### Splashscreen/Startup Script

```bash
# Option 1: Run the splashscreen script locally
python3 splashscreen.py

# Option 2: Run the splashscreen script via systemctl
sudo systemctl start bci_arm_main.service

# This script will also be run on startup if the systemd service is configured right
```

## Setup

### Client System (main program)

After cloning this repository on the Dofbot system image, a few steps are required to setup the main script system.

### Install SmartSocket Library

```bash
# Run the following command to clone the library
git clone https://github.com/Clloyd3267/SmartSockets.git
```

### Install and Compile Protobuf Protocol Buffers

See CDL=> readme for more details

### Splashscreen/Startup Script

```bash
# Move the service file into position
sudo mv bci_arm_main.service /etc/systemd/system/

# Reload the systemctl dameon
sudo systemctl daemon-reload

# Enable the service so it runs on startup
sudo systemctl enable bci_arm_main.service
```
