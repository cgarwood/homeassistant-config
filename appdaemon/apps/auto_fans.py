##
# Automatically control bedroom fans
# Each room will have a target temperature. If the temperature
# is above the target the fan will turn on. If the temperature
# drops below the target, the fan will turn off.
##

import appdaemon.plugins.hass.hassapi as hass


class AutoFans(hass.Hass):

    def initialize(self):
        self.fans = [
            {
                'fan': 'fan.master_bedroom_fan',
                'temperature': 'sensor.master_bedroom_multisensor_temperature',
                'target': 'input_number.auto_fan_master_bedroom_target',
                'enabled': 'input_boolean.auto_fan_master_bedroom',
                'callbacks': {}
            },
            {
                'fan': 'fan.nursery_fan',
                'temperature': 'sensor.nursery_multisensor_temperature',
                'target': 'input_number.auto_fan_nursery_target',
                'enabled': 'input_boolean.auto_fan_nursery',
                'callbacks': {}
            },
        ]

        for fan in self.fans:
            self.listen_state(self.handle_enabled, fan['enabled'])
            if (self.get_state(fan['enabled']) == 'on'):
                fan['callbacks']['fan'] = self.listen_state(
                    self.handle_fan, fan['fan'])
                fan['callbacks']['temperature'] = self.listen_state(
                    self.handle_temperature, fan['temperature'])
                fan['callbacks']['target'] = self.listen_state(
                    self.handle_target, fan['target'])

    def handle_enabled(self, entity, attribute, old, new, kwargs):
        # Keep track of enabled status for each fan

        fan = self.fans[find(self.fans, 'enabled', entity)]

        if (new == 'on'):
            # Register callbacks to monitor states
            fan['callbacks']['fan'] = self.listen_state(
                self.handle_fan, fan['fan'])
            fan['callbacks']['temperature'] = self.listen_state(
                self.handle_temperature, fan['temperature'])
            fan['callbacks']['target'] = self.listen_state(
                self.handle_target, fan['target'])

            temperature = float(self.get_state(fan['temperature']))
            target = float(self.get_state(fan['target']))
            self.process(fan, temperature, target)

        if (new == 'off'):
            # Remove callbacks
            self.cancel_listen_state(fan['callbacks']['fan'])
            self.cancel_listen_state(fan['callbacks']['temperature'])
            self.cancel_listen_state(fan['callbacks']['target'])

    def handle_fan(self, entity, attribute, old, new, kwargs):
        # Keep track of fan state. Disable auto fan if fan is manually turned off
        # Requires appdaemon being able to pull context of the state change
        # as otherwise it will fire when this script auto turns off a fan.
        return

    def handle_temperature(self, entity, attribute, old, new, kwargs):
        # Handle temperature changes

        fan = self.fans[find(self.fans, 'temperature', entity)]
        temperature = float(new)
        target = float(self.get_state(fan['target']))
        self.process(fan, temperature, target)

    def handle_target(self, entity, attribute, old, new, kwargs):
        # Handle changes to target temperature

        fan = self.fans[find(self.fans, 'target', entity)]
        temperature = float(self.get_state(fan['temperature']))
        target = float(new)
        self.process(fan, temperature, target)

    def process(self, fan, temperature, target):
        # Process changes to temperature or target and send commands to the fan

        fan_state = self.get_state(fan['fan'])
        fan_speed = self.get_state(fan['fan'], attribute='speed')

        # Turn the fan off if we reach or drop below target temperature
        if (temperature <= target and fan_state == 'on'):
            self.call_service('fan/turn_off', entity_id=fan['fan'])

        # If we're above target temperature adjust speed based on how far above
        if (temperature > target):
            speed = 'low'
            if (temperature > target + 8):
                speed = 'medium'

            # Turn the fan on if it's off and we're more than 1 degree above target
            if (fan_state == 'off' and temperature > target + 1):
                self.call_service(
                    'fan/turn_on', entity_id=fan['fan'], speed=speed)

            # If current fan speed doesn't match what we think, adjust it
            if (fan_state == 'on' and fan_speed != speed):
                self.call_service(
                    'fan/set_speed', entity_id=fan['fan'], speed=speed)


def find(lst, key, value):
    for i, dic in enumerate(lst):
        if (dic[key] == value):
            return i
    raise ValueError
