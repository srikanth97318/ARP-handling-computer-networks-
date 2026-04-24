# ARP-handling-computer-networks-

# SDN-Based ARP Management and Flow Optimization

**PES University - Software Defined Networking Project**

[![License](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Python](https://img.shields.io/badge/Python-3.6+-green.svg)](https://www.python.org/)

## 📋 Table of Contents

- [Project Overview](#-project-overview)
- [Technical Architecture](#-technical-architecture)
- [Features & Logic](#-features--logic)
- [Installation & Setup](#-installation--setup)
- [Execution & Testing](#-execution--testing)
- [Performance Analysis](#-performance-analysis)
- [Author](#-author)
- [Contributing](#-contributing)
- [License](#-license)

## 📌 Project Overview

This project implements a Software Defined Networking (SDN) application that manages **ARP (Address Resolution Protocol)** and optimizes network traffic through **Flow Rule Installation**.

By using the **POX Controller** and **Mininet**, we demonstrate how a centralized control plane can intercept host discovery requests and program the data plane (Open vSwitch) to handle subsequent packets at hardware speeds.

## 🛠️ Technical Architecture

- **Control Plane:** POX Controller (Python)
- **Data Plane:** Open vSwitch (OVS)
- **Southbound Interface:** OpenFlow v1.0
- **Topology:** Single Switch with 2 Hosts ($h1$, $h2$)

## 🚀 Features & Logic

1. **Packet_In Handling:** The switch sends all unknown ARP packets to the controller.
2. **MAC Learning:** The controller parses the Ethernet headers to map Source MAC addresses to their respective Switch Ports.
3. **ARP Flooding:** The controller manages the ARP broadcast to facilitate host discovery.
4. **Flow Mod (Optimization):** Once a path is identified, the controller pushes an `ofp_flow_mod` rule to the switch. This ensures that future pings between the two hosts skip the controller entirely.

## 💻 Installation & Setup

### Prerequisites

Ensure you have Mininet and POX installed on your Linux environment:

```bash
sudo apt update
sudo apt install mininet
git clone https://github.com/noxrepo/pox
```

### Deployment

Move the `arp-controller.py` script to the POX extension directory:

```bash
cp arp-controller.py ~/pox/ext/
```

## 🧪 Execution & Testing

### Step 1: Start the POX Controller

Open a terminal and launch the controller with debug logging:

```bash
cd ~/pox
./pox.py log.level --DEBUG arp_controller
```

### Step 2: Start the Mininet Topology

Open a second terminal and create the network:

```bash
sudo mn --controller=remote,ip=127.0.0.1 --topo=single,2
```

### Step 3: Verify Results

Run a ping test in the Mininet prompt:

```bash
mininet> h1 ping -c 4 h2
```

**Observation:**
- **First Ping:** High latency (~5-10ms) as it travels to the Controller.
- **Subsequent Pings:** Low latency (~0.1ms) as they are handled by the Switch Flow Table.

Check the installed flow rules:

```bash
mininet> sh ovs-ofctl dump-flows s1
```

## 📊 Performance Analysis

| Packet Number | Path | Latency (Approx) |
|---------------|------|------------------|
| Packet 1 (ARP + ICMP) | Host -> Switch -> Controller -> Switch -> Host | ~7.42 ms |
| Packet 2-4 (ICMP) | Host -> Switch (Flow Match) -> Host | ~0.08 ms |

## 👤 Author

**Sri Kanth G**  
University: PES University, Bengaluru  
Specialization: B.Tech CSE (AI & ML)
