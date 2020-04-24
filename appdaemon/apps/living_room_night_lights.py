##
# Motion-activated overnight lighting in living room/kitchen
##

import appdaemon.plugins.hass.hassapi as hass
import datetime
import dateutil.parser


class LivingRoomNightLights(hass.Hass):

    def initialize(self):
        self.listen_state(self.handle_motion,
                          "binary_sensor.living_room_multisensor_motion")

    def handle_motion(self, entity, attribute, old, new, kwargs):

        goodnight_state = self.get_state('input_boolean.goodnight')
        goodnight_time = dateutil.parser.parse(self.get_state(
            'input_boolean.goodnight', attribute='last_updated')).timestamp()
        current_time = datetime.datetime.now().timestamp()

        # Only trigger if the house has been "Goodnight" for > 45 seconds
        if (goodnight_state == 'on' and (current_time - goodnight_time > 45)):
            goodnight = True
        else:
            goodnight = False

        if (new == 'on' and goodnight):
            self.call_service(
                'homeassistant/turn_on', entity_id='light.living_room_accent_lights', brightness='50')
            self.call_service(
                'homeassistant/turn_on', entity_id='light.kitchen_cabinet_lights', brightness='50')

            # If a timer is already running, cancel it
            if (hasattr(self, 'lights_off_timer')):
                self.cancel_timer(self.lights_off_timer)

        if (new == 'off' and goodnight):
            # Start a lights off timer
            self.light_off_timer = self.run_in(self.lights_out, 300) # was 30

    def lights_out(self, kwargs):
        self.call_service('homeassistant/turn_off',
                          entity_id='light.living_room_accent_lights')
        self.call_service('homeassistant/turn_off',
                          entity_id='light.kitchen_cabinet_lights')
