# Sunsynk / Deye Inverter Add-On Documentation

This add-on connects your Sunsynk, Deye, or compatible hybrid inverter to Home Assistant using Modbus (via direct USB-RS485, Modbus TCP gateway, or Solarman Wi-Fi dongle) and publishes all sensors and settings via MQTT.

---

## 1. Quick Start Configuration

A typical single-inverter setup requires:
1. `SENSOR_DEFINITIONS`: Your inverter type (`single-phase`, `single-phase-16kw`, `three-phase`, or `three-phase-hv`).
2. `SENSORS`: Sensor groups to poll (`energy_management`, `power_flow_card`, `pv1`, `pv2`).
3. `SENSORS_FIRST_INVERTER`: Configuration settings (`settings`, `battery`, `advanced`).
4. `INVERTERS`: An entry with your inverter's serial number, port, Modbus ID, and entity prefix.

```yaml
SENSOR_DEFINITIONS: single-phase

SENSORS:
  - energy_management
  - power_flow_card
  - pv1
  - pv2

SENSORS_FIRST_INVERTER:
  - settings
  - battery
  - advanced

INVERTERS:
  - SERIAL_NR: "1234567890"
    HA_PREFIX: Sunsynk
    MODBUS_ID: 1
    PORT: /dev/serial/by-id/usb-FTDI_FT232R_USB_UART_...-port0

READ_ALLOW_GAP: 2
READ_SENSORS_BATCH_SIZE: 8
READ_MESSAGE_SPACING: 0.15
READ_ATTEMPTS: 3
TIMEOUT: 3
STALE_INVERTER_AFTER_SECONDS: 120
STALE_INVERTER_SKIP_SECONDS: 600

SCHEDULES:
  - KEY: W
    READ_EVERY: 5
    REPORT_EVERY: 60
    CHANGE_ANY: false
    CHANGE_BY: 20
    CHANGE_PERCENT: 0
  - KEY: V
    READ_EVERY: 5
    REPORT_EVERY: 60
    CHANGE_ANY: true
  - KEY: A
    READ_EVERY: 5
    REPORT_EVERY: 60
    CHANGE_ANY: true
```

---

## 2. Inverter Connection & PORT Options

| Protocol / Connection | `PORT` Value Example | Details |
|---|---|---|
| **Direct USB RS485** | `/dev/serial/by-id/usb-FTDI...` | Use persistent `/dev/serial/by-id/` path. Set `READ_MESSAGE_SPACING: 0.15` and `READ_SENSORS_BATCH_SIZE: 8`. |
| **Modbus TCP Gateway** | `tcp://192.168.1.50:502` | Waveshare, USR-W630, or `mbusd` gateway converting Ethernet to RS485 RTU. |
| **RTU-over-TCP** | `serial-tcp://192.168.1.50:502` | Used when the gateway passes raw serial RTU frames over a TCP socket without Modbus TCP header translation. |
| **Solarman Dongle** | `solarman-tcp://192.168.1.182:8899` | Connects to the inverter's Solarman Wi-Fi/Ethernet data logger. Requires `DONGLE_SERIAL_NUMBER`. |

### Multiple Inverters on a Shared RS485 Bus
If multiple inverters are daisy-chained on the same physical RS485 bus:
- Repeat the **exact same `PORT`** on each `INVERTERS` entry.
- Assign distinct `MODBUS_ID` (1, 2, ...), `SERIAL_NR`, and `HA_PREFIX` for each unit.
- The add-on serializes all requests so the inverters never collide on the shared line.

---

## 3. Sensor Groups & Definitions

### Inverter Families (`SENSOR_DEFINITIONS`)
- `single-phase`: Standard 5kW, 8kW, and common hybrid low-voltage models.
- `single-phase-16kw`: Single-phase 16kW models with extended registers.
- `three-phase`: Three-phase low-voltage models.
- `three-phase-hv`: Three-phase high-voltage (HV) models with up to 8 MPPT inputs.

### Predefined Sensor Groups
- **`energy_management`**: Daily and total kWh counters for grid import/export, PV generation, and battery charge/discharge. Essential for Home Assistant Energy Dashboard.
- **`power_flow_card`**: Live telemetry for instantaneous Watts, Volts, Amps, frequencies, and grid/load powers. Powers the Sunsynk Power Flow Card.
- **`pv1`**, **`pv2`**, **`pv3`**, **`pv4`**: Individual MPPT power, voltage, and current sensors.
- **`settings`**: System mode, timer slots (Prog1–Prog6 times, powers, capacities, and grid charge switches). Put in `SENSORS_FIRST_INVERTER`.
- **`battery`**: Battery equalization, float, absorption voltages, and shutdown/restart thresholds.
- **`advanced`**: Inverter grid frequency, phase tracking, and UPS delay settings.
- **`diagnostics`**: Fault flags, BMS warnings, fan status, and internal temperatures.

---

## 4. RS485 Bus Timing & Reliability Settings

If you experience timeouts, CRC errors, or the inverter dropping offline:

- **`READ_MESSAGE_SPACING`** (Default: `0.15`): Enforces a silent turnaround delay between consecutive Modbus frames. Inverters and USB-RS485 transceivers require ~50–150ms between requests.
- **`READ_SENSORS_BATCH_SIZE`** (Default: `8`): Limits how many adjacent holding registers are queried in a single Modbus FC03 call. Lowering this from 20 to 8 greatly improves reliability on USB adapters.
- **`TIMEOUT`** (Default: `3`): Maximum wait time in seconds for an inverter to respond to a query before retrying.
- **`READ_ATTEMPTS`** (Default: `3`): Number of retries per register group before reporting a read error.
- **`STALE_INVERTER_AFTER_SECONDS`** (Default: `120`): If communication fails continuously for this duration, the add-on marks the inverter stale and pauses polling to prevent bus contention.
- **`STALE_INVERTER_SKIP_SECONDS`** (Default: `600`): How long the add-on pauses before probing the inverter to resume polling.

---

## 5. Schedules (`SCHEDULES`)

Schedules control how often sensors are read and reported:
- **`KEY: W`**: Controls Watt power sensors. Set `CHANGE_BY: 20` to catch early sunrise ramp-up and report immediately when output changes.
- **`KEY: V`**: Controls Voltage sensors. Set `CHANGE_ANY: true` to publish open-circuit and operating voltage shifts instantly.
- **`KEY: A`**: Controls Current sensors. Set `CHANGE_ANY: true` to report immediately on current changes.

---

## 6. MQTT Settings

- **Automatic Configuration**: On Home Assistant OS, leave `MQTT_CUSTOM: false` (or omitted). The add-on automatically discovers the Mosquitto broker and credentials from the Supervisor.
- **External Broker**: Set `MQTT_CUSTOM: true`, then configure `MQTT_HOST`, `MQTT_PORT`, `MQTT_USERNAME`, and `MQTT_PASSWORD`.

---

## 7. Fault Finding & Common Issues

1. **`No response on the Modbus interface`**:
   - Check RJ45 wiring: Sunsynk/Deye standard RJ45 port pins are typically Pin 7 (RS485-A) and Pin 8 (RS485-B), or Pin 1 (A) and Pin 2 (B) depending on model and port label (RS485/CAN).
   - Ensure the inverter screen shows Modbus SN matching `MODBUS_ID` (default is 1).
2. **`Inverter stale. Skip Modbus for 600s`**:
   - Increase `READ_MESSAGE_SPACING` to `0.15`.
   - Reduce `READ_SENSORS_BATCH_SIZE` to `6` or `8`.
   - Increase `TIMEOUT` to `5`.
3. **Values showing 0 at sunrise**:
   - Verify that your `W` schedule has `CHANGE_BY: 20` and `V`/`A` have `CHANGE_ANY: true`.
