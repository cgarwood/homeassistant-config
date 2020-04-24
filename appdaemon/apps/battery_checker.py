##
# Send alert if battery-powered sensors haven't updated
# for a specific period of time
#
# For monitoring battery powered zwave/zigbee sensors that
# have poor battery_level reporting
##

import appdaemon.plugins.hass.hassapi as hass
import datetime
import dateutil.parser


class BatteryChecker(hass.Hass):

    def initialize(self):
        runtime = datetime.time(0, 0, 0)
        self.run_hourly(self.check_sensors, runtime)

    def check_sensors(self, kwargs):
        sensors = [
            'sensor.living_room_multisensor_temperature',
            'sensor.nursery_multisensor_temperature',
            'sensor.guest_bedroom_multisensor_temperature',
            'sensor.guest_bathroom_multisensor_temperature',
            'sensor.master_bedroom_multisensor_temperature',
            'sensor.master_bathroom_multisensor_temperature',
            'sensor.attic_temperature',
            'sensor.hvac_supply_temperature',
            'sensor.hvac_return_temperature',
        ]

        for sensor in sensors:
            last_updated = dateutil.parser.parse(self.get_state(
                sensor, attribute='last_updated')).timestamp()

            current_time = datetime.datetime.now().timestamp()

            if (current_time - last_updated > 8 * 60 * 60):
                short_name = sensor.split('.')[1]
                self.call_service('persistent_notification/create', notification_id='check_sensor_'+short_name, title='Check Sensor',
                                  message='The following sensor has not updated for more than 8 hours. Battery dead? - ' + sensor)
