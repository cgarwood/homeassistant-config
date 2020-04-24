##
# Guest Bathroom Light Watcher
# Since guests are bad at our paddle dimmers.
# If light brightness is below ~15% for more than a few minutes, 
# reset to full brightness and turn the light off
##

import appdaemon.plugins.hass.hassapi as hass
import datetime

class GuestBathroomLightWatcher(hass.Hass):

    def initialize(self):
        self.handles = {}
        
        self.listen_state(self.handle_light, "light.guest_bathroom_vanity_light_level", attribute = "brightness")
        self.listen_state(self.handle_light, "light.guest_bathroom_fan_light_level", attribute = "brightness")
        
    def handle_light(self, entity, attribute, old, new, kwargs):
        if (new != None):
            if (new > 0 and new < 40):
                self.handles[entity] = self.run_in(self.lightsout, 20, entity_id = entity)
            elif (new >= 40):
                if (hasattr(self.handles,entity)):
                    self.cancel_timer(self.handles[entity])

    def lightsout(self, kwargs):
        entity_id = kwargs["entity_id"]
        self.call_service('homeassistant/turn_on', entity_id = entity_id, brightness = 255)
        self.call_service('homeassistant/turn_off', entity_id = entity_id)