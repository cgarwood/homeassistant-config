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
        
        # Amount of time to wait before dimming lights
        self.dim_delay = 10
        
        # Amount of time to wait before turning lights off
        self.off_delay = 30
        
    def handle_light(self, entity, attribute, old, new, kwargs):
    
        # Is is daytime or nighttime? (Between 5:30 am and 11:30 pm)
        self.time = datetime.datetime.now().time()
        if (self.time >= datetime.time(5,30) and self.time <= datetime.time(23,30)):
            self.overnight = False
        else:
            self.overnight = True
            
        if (new == 'on'):
            # Motion Detected
            self.call_service('notify/ios',title = 'Bathroom Lights', message = 'debug: motion detected. lights on. timer cancelled.')
            if (not self.overnight):
                self.entity = 'light.guest_bathroom_fan_light_level'
                self.call_service('homeassistant/turn_on', entity_id = self.entity, brightness = '255')
            else:
                self.entity = 'light.guest_bathroom_vantiy_light_level'
                self.call_service('homeassistant/turn_on', entity_id = self.entity, brightness = '25')
            
            # Cancel the timers if one is started
            if (hasattr(self,'lights_off_timer')):
                self.cancel_timer(self.lights_off_timer)
            if (hasattr(self,'dim_lights_timer')):
                self.cancel_timer(self.dim_lights_timer)
            
        if (new == 'off'):
            # Wait a couple minutes for a re-trigger, otherwise turn lights off
            self.dim_lights_timer = self.run_in(self.dim_lights, self.dim_delay, entity_id = self.entity)
            self.call_service('notify/ios',title = 'Bathroom Lights', message = 'debug: no motion, starting turn off timer')
    
    def dim_lights(self, kwargs):
        # Dim the lights as a warning
        
        # TODO: check if overnight and adjust brightness accordingly
        # TODO: check if light was already turned off so we don't turn it back on to dim it
        self.call_service('light/turn_on', entity_id = kwargs['entity_id'], brightness = '100')
        self.call_service('notify/ios',title = 'Bathroom Lights', message = 'debug: lights dimmed')
        
        # Start a timer to turn the lights off
        self.lights_off_timer = self.run_in(self.lights_out, self.off_delay, entity_id = self.entity)
        
    def lights_out(self, kwargs):
        # TODO: Figure out how to handle the fact that there are two lights in each bathroom
        # only one is automatically turned on, but if the other is manually turned on we still
        # don't want to leave it on forever.
        self.call_service('homeassistant/turn_off', entity_id = kwargs['entity_id'])
        self.call_service('notify/ios',title = 'Bathroom Lights', message = 'debug: lights off')