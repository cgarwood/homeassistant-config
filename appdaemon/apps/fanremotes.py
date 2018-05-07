##
# Handle Pico Remotes for Controlling Zigbee Fans
##

import appdaemon.plugins.hass.hassapi as hass

class FanRemotes(hass.Hass):

    def initialize(self):
        self.listen_state(self.handle_light, "sensor.office_light_pico")
        self.listen_state(self.handle_light, "sensor.master_bedroom_light_pico")
        self.listen_state(self.handle_fan, "sensor.office_fan_pico")
        self.listen_state(self.handle_fan, "sensor.master_bedroom_fan_pico")
        
    def handle_light(self, entity, attribute, old, new, kwargs):
        if (entity == "sensor.office_light_pico"):
            controlled_entity = "light.office"
        if (entity == "sensor.master_bedroom_light_pico"):
            controlled_entity = "light.master_bedroom"
            
        if (new == '1'):
            # On
            self.call_service('homeassistant/turn_on', entity_id = controlled_entity, brightness = 255)
            
        if (new == '2'):
            # Favorite
            self.call_service('homeassistant/turn_on', entity_id = controlled_entity, brightness = 25)
            
        if (new == '4'):
            # Off
            self.call_service('homeassistant/turn_off', entity_id = controlled_entity)
            
        if (new == '8'):
            # Up
            pass
            
        if (new == '16'):
            # Down
            pass
            
    def handle_fan(self, entity, attribute, old, new, kwargs):
        
        if (entity == "sensor.office_fan_pico"):
            controlled_entity = "fan.office_fan"
        if (entity == "sensor.master_bedroom_fan_pico"):
            controlled_entity = "fan.master_bedroom_fan"
            
        if (new == '1'):
            # On
            self.call_service('fan/turn_on', entity_id = controlled_entity)
            
        if (new == '2'):
            # Favorite
            self.call_service('fan/set_speed', entity_id = controlled_entity, speed = 'low')
            
        if (new == '4'):
            # Off
            self.call_service('homeassistant/turn_off', entity_id = controlled_entity)
            
        if (new == '8'):
            # Up
            self.call_service('fan/set_speed', entity_id = controlled_entity, speed = 'medium')
            
        if (new == '16'):
            # Down
            self.call_service('fan/set_speed', entity_id = controlled_entity, speed = 'lowest')
            