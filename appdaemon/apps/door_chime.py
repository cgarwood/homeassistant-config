##
# Plays a chime on HADashboard when exterior doors are opened or closed.
##

import appdaemon.plugins.hass.hassapi as hass

class DoorChime(hass.Hass):

    def initialize(self):
        self.listen_state(self.chime, "binary_sensor.front_door_sensor")
        self.listen_state(self.chime, "binary_sensor.back_door_sensor")
        self.listen_state(self.chime, "binary_sensor.garage_side_door")
        self.listen_state(self.chime, "binary_sensor.garage_inside_door")

    def chime(self, entity, attribute, old, new, kwargs):
        friendly_name = self.get_state(entity, attribute="friendly_name")
        
        if (new == "on"):
            self.fire_event("hadashboard", command="play_sound", sound="strings.mp3", tts=friendly_name + "opened")
        
        if (new == "off"):
            self.fire_event("hadashboard", command="play_sound", sound="strings2.mp3", tts=friendly_name + "closed")