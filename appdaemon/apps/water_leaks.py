##
# Notify and shut off water main if a leak is detected
##

import appdaemon.plugins.hass.hassapi as hass

class WaterLeaks(hass.Hass):

    def initialize(self):
        self.sensors = [
            "binary_sensor.garage_water_sensor"
        ]
        for sensor in self.sensors:
            self.listen_state(self.water_leak, sensor)

    def water_leak(self, entity, attribute, old, new, kwargs):
        if (new == "on"):
            state = self.get_state(entity, attribute="all")

            if (self.get_state("input_boolean.water_valve_maintenance_mode") == "on"):
                self.call_service('notify/charles', title="\uD83D\uDCA7 (TEST MODE) Water Leak Detected", message=f"TEST MODE\n{state['attributes']['friendly_name']} detected water.")
                self.fire_event("snapcast_notify", sound="local:attention.mp3", tts=f"This is a test. Water leak detected by {state['attributes']['friendly_name']}. This is a test.")
            else:
                self.call_service('notify/charles', title="\uD83D\uDCA7 Water Leak Detected", message=f"{state['attributes']['friendly_name']} detected water. Closing main valve.")
                self.call_service('switch/turn_off', entity_id="switch.water_main_valve")
                self.fire_event("snapcast_notify", sound="local:warning.wav", tts=f"Water leak detected by {state['attributes']['friendly_name']}. Closing main valve.")
