##
# Automatic Bathroom Lights
# Based on motion/humidity and time of day
##

# TODO: Set brightness based on time of day. Full if between 5:30 am and 11:30pm, otherwise ~25%
#       Possibly base it on house mode when that's finished (If house == asleep, then dim)
# TODO: adjust lights_off_timer based on humidity (don't turn lights off if someone's in the shower)

import appdaemon.plugins.hass.hassapi as hass
import datetime

class AutoBathroomLights(hass.Hass):

    def initialize(self):
        self.listen_state(self.handle_light, "binary_sensor.guest_bathroom_multisensor_motion")
        
    def handle_light(self, entity, attribute, old, new, kwargs):
        self.time = datetime.datetime.now().time()
        
        if (new == 'on'):
            # Motion Detected
            self.call_service('notify/ios',title = 'Bathroom Lights', message = 'debug: motion detected. lights on. timer cancelled.')
            if (self.time >= datetime.time(5,30) and self.time <= datetime.time(23,30)):
                self.entity = 'light.guest_bathroom_fan_light_level'
                self.call_service('homeassistant/turn_on', entity_id = self.entity)
            else:
                self.entity = 'light.guest_bathroom_vantiy_light_level'
                self.call_service('homeassistant/turn_on', entity_id = self.entity, brightness = '25')
            
            # Cancel the timer if one is started
            if (hasattr(self,'lights_off_timer')):
                self.cancel_timer(self.lights_off_timer)
            
        if (new == 'off'):
            # Wait a couple minutes for a re-trigger, otherwise turn lights off
            self.lights_off_timer = self.run_in(self.lights_out, 180, entity_id = self.entity)
            self.call_service('notify/ios',title = 'Bathroom Lights', message = 'debug: no motion, starting turn off timer')
    
    def lights_out(self, kwargs):
        self.call_service('homeassistant/turn_off', entity_id = kwargs['entity_id'])        