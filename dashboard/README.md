# Sunsynk Solar Monitoring Dashboard

This folder contains a complete solar monitoring solution tailored for Sunsynk / Deye inverters using the `sunsynkgm` MQTT sensor prefix.

---

## Files Included

| File | Description |
| :--- | :--- |
| [`index.html`](./index.html) | Standalone interactive web dashboard with animated SVG power flow, real-time Chart.js graphs, program schedules matrix, telemetry cards, and live MQTT-over-WebSocket client. |
| [`homeassistant-dashboard.yaml`](./homeassistant-dashboard.yaml) | Complete Home Assistant Lovelace dashboard configuration using `custom:sunsynk-power-flow-card`, `custom:apexcharts-card`, and program schedule views mapped directly to `sensor.sunsynkgm_*`. |
| [`mqtt-sensors.yaml`](./mqtt-sensors.yaml) | Home Assistant MQTT sensor definitions for all published topics if manual MQTT configuration is needed. |

---

## 1. Standalone Web Dashboard (`index.html`)

### Features
- **Animated SVG Power Flow Card**: Real-time flowing energy lines between Solar PV (PV1 & PV2), Hybrid Inverter, Battery, National Grid, and Home Loads (Essential + Non-Essential). Lines change direction dynamically based on charging/discharging or import/export.
- **Dynamic Chart.js Graphs**:
  - **Live Power History**: Multi-line real-time graph of Load vs Grid vs Solar vs Battery.
  - **Daily Energy Balance**: Bar chart comparing Daily PV produced, Load consumed, Grid import/export, and Battery throughput.
- **Time-of-Use Program Matrix**: Clean view of Prog 1 through Prog 6 (Time, Target SOC %, Charge mode, and Power limits).
- **Inverter & Battery Diagnostics**: Telemetry view of voltages, currents, frequencies, CT power, float/absorption/cutoff limits.
- **Live MQTT over WebSocket Support**: Built-in client (Paho / MQTT.js) supporting configurable broker URL (e.g., `ws://your-broker-ip:9001`), username/password, and topic prefix (`sunsynkgm`).
- **Demo / Simulation Mode**: Built-in toggle to test animations and live updates immediately without needing an active broker connection.

### How to Run
Simply open `index.html` in any modern web browser:
```bash
# Direct launch
xdg-open index.html

# Or serve via Python
python3 -m http.server 8080 -d .
# Then open http://localhost:8080/index.html
```

To embed inside Home Assistant:
1. Copy `index.html` to your Home Assistant `/config/www/sunsynk/index.html` folder.
2. In Lovelace, add a **Webpage Card** with URL: `/local/sunsynk/index.html`.

---

## 2. Home Assistant Lovelace Dashboard (`homeassistant-dashboard.yaml`)

This dashboard configuration is pre-configured with all your sensor entity IDs (`sunsynkgm_*`).

### Required Custom Cards (installable via HACS)
1. **[Sunsynk Power Flow Card](https://github.com/slipx06/sunsynk-power-flow-card)** (`custom:sunsynk-power-flow-card`)
2. **[ApexCharts Card](https://github.com/RomRider/apexcharts-card)** (`custom:apexcharts-card`)

### How to Install
1. Open Home Assistant &rarr; **Dashboards** &rarr; **Add Dashboard** (or edit an existing one in Raw Configuration Editor).
2. Paste the contents of [`homeassistant-dashboard.yaml`](./homeassistant-dashboard.yaml).
3. Save and refresh.

---

## 3. MQTT Sensor Mapping Summary

All sensors published by your inverter under `sunsynkgm`:

- **Solar**: `pv_power`, `pv1_power`, `pv1_voltage`, `pv1_current`, `pv2_power`, `pv2_voltage`, `pv2_current`, `day_pv_energy`, `total_pv_energy`
- **Battery**: `battery_power`, `battery_soc`, `battery_voltage`, `battery_current`, `day_battery_charge`, `day_battery_discharge`, `battery_float_voltage`, `battery_absorption_voltage`, `battery_low_capacity`, `battery_shutdown_capacity`, etc.
- **Grid**: `grid_power`, `grid_ct_power`, `grid_frequency`, `grid_voltage`, `grid_current`, `grid_connected`, `day_grid_import`, `day_grid_export`
- **Load & Inverter**: `load_power`, `essential_power`, `non_essential_power`, `aux_power`, `inverter_power`, `overall_state`, `load_limit`
- **Programs**: `prog1_time` ... `prog6_time`, `prog1_capacity` ... `prog6_capacity`, `prog1_charge` ... `prog6_charge`, `prog1_power` ... `prog6_power`
