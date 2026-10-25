"""Custom sensor overrides for Sunsynk Lynx Pro.

Alternative approach: try known Deye/Lynx register variants.
"""

from sunsynk import KWH
from sunsynk.definitions.single_phase import SENSORS
from sunsynk.sensors import Sensor, SensorDefinitions

# Create a new sensor definitions collection
CUSTOM = SensorDefinitions()
CUSTOM.all = SENSORS.all.copy()
CUSTOM.deprecated = SENSORS.deprecated.copy()

# Try alternative register mappings for Lynx Pro
# Some Lynx models use registers 60-65 for daily grid energy
alt_sensors = (
    Sensor(60, "day_grid_import_alt", KWH, 0.1),
    Sensor(61, "day_grid_export_alt", KWH, 0.1),
    Sensor(62, "day_grid_import_alt2", KWH, 0.1),
    Sensor(63, "day_grid_export_alt2", KWH, 0.1),
    Sensor(64, "total_grid_import_alt", KWH, 0.1),
    Sensor(65, "total_grid_export_alt", KWH, 0.1),
)

for sen in alt_sensors:
    CUSTOM.all[sen.id] = sen

SENSORS = CUSTOM
