# Sunsynk & Deye Inverter Documentation

Welcome to the documentation for the Sunsynk/Deye Home Assistant Add-On and Python library.

---

## Table of Contents

### 1. Guides & Deployment
- [**Overview**](guide/overview.md) — Introduction, key features, and architecture.
- [**Getting Started**](guide/getting-started.md) — Step-by-step installation in Home Assistant OS.
- [**Deployment Options**](guide/deployment-options.md) — Direct USB-RS485, Ethernet/WiFi gateways, and standalone setups.
- [**Standalone Deployment**](guide/standalone-deployment.md) — Running via Docker / Docker Compose without Home Assistant OS.
- [**Tested Inverters**](guide/tested-inverters.md) — Community-verified inverter models and protocols.

### 2. Hardware & Wiring
- [**Wiring Guide**](guide/wiring.md) — RJ45 pinouts for Sunsynk/Deye, RS485 USB adapters, WaveShare, and USR gateways.
- [**mbusd Gateway**](guide/mbusd.md) — Using `mbusd` to bridge USB serial to Modbus TCP.
- [**ESPHome Gateway**](guide/esp.md) — Using an ESP32/ESP8266 as an RS485-to-WiFi bridge.

### 3. Troubleshooting & Fault Finding
- [**Fault Finding Guide**](guide/fault-finding.md) — Step-by-step diagnostic checklist for connection failures and timeouts.
- [**Modbus Timeouts & Pacing**](timeouts.md) — Technical details on deadlines, bus pacing (`READ_MESSAGE_SPACING`), and stale inverter recovery.
- [**Modbus Connection Architecture**](modbus-connection.md) — Background on the v1.0.0 connection layer and protocol handling.

### 4. Configuration Reference
- [**Add-on Options**](reference/multi-options.md) — Full reference for `config.yaml` options (`INVERTERS`, `SCHEDULES`, `READ_SENSORS_BATCH_SIZE`, etc.).
- [**Sensor Definitions**](reference/definitions.md) — Register mappings and descriptions for single-phase inverters.
- [**3-Phase Sensor Definitions**](reference/definitions3ph.md) — Register mappings for 3-phase LV and HV inverters.
- [**Timer Schedules**](reference/schedules.md) — Configuring polling and reporting intervals per sensor or unit.
- [**Custom Sensors (`mysensors.py`)**](reference/mysensors.md) — Adding custom registers and calculated sensors.
- [**Sensor Modifiers**](reference/sensor-modifiers.md) — Overriding default sensor behaviour and offsets.

### 5. Dashboards, Visualizations & Automations
- [**Power Flow Card**](examples/lovelace.md) — Setting up the interactive power flow Lovelace card.
- [**Inverter Settings Card**](examples/lovelace-settings.md) — Controlling system mode, charge profiles, and timers from Home Assistant.
- [**Energy Management**](guide/energy-management.md) — Integrating inverter sensors with the Home Assistant Energy dashboard.
- [**Automation Examples**](examples/a-mode.md) — Example automations for load shedding, battery charging, and export management.
- [**Sensor Templates**](examples/templates.md) — Useful Home Assistant template sensors and helpers.
