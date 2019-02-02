##
# Quick and Dirty
# Send alert if temperature drops below certain thresholds
# Thanks -20 degree air temp with -45 degree wind chills!
##

import appdaemon.plugins.hass.hassapi as hass


class TemperatureAlerts(hass.Hass):

    def initialize(self):
        self.listen_state(self.temperature_change,
                          "sensor.nursery_multisensor_temperature")
        self.listen_state(self.temperature_change,
                          "sensor.living_room_multisensor_temperature")
        self.listen_state(self.temperature_change,
                          "sensor.garage_multisensor_temperature")
        self.listen_state(self.temperature_change,
                          "sensor.master_bedroom_multisensor_temperature")
        self.listen_state(self.temperature_change,
                          "sensor.master_bathroom_multisensor_temperature")

    def temperature_change(self, entity, attribute, old, new, kwargs):
        min_temp = 64
        if (entity == 'sensor.living_room_multisensor_temperature'):
            min_temp = 62

        if (entity == 'sensor.master_bedroom_multisensor_temperature'):
            min_temp = 62

        if (entity == 'sensor.garage_multisensor_temperature'):
            min_temp = 30

        if (float(new) <= min_temp and float(old) > min_temp):
            self.fire_event('tileboard', command='screen_on',
                            target='master_bedroom')
            self.fire_event('tileboard', command='open_page',
                            target='master_bedroom', page='temperatures')

            message = "{} below temperature threshold. Current: {} - Minimum: {}".format(
                entity, new, min_temp)
            self.fire_event('tileboard', command='notify', target='master_bedroom', title='Temperature Alert',
                            message=message, sound='/sounds/alarm2.mp3', type='error')
            self.call_service(
                'notify/ios', title="Temperature Alert", message=message)
