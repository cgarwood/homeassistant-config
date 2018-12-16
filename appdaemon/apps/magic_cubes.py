##
# Trigger functions based on Xiaomi Magic Cube Events
##

import appdaemon.plugins.hass.hassapi as hass

class MagicCubes(hass.Hass):
    def initialize(self):
        self.listen_event(self.handle_cube, 'zha_event')

    def handle_cube(self, event_name, data, kwargs):
        # Event IDs
        # zha_event.zha_029bd185_2 - master bedroom cube events
        # zha_event.zha_029bd185_3 - master bedroom cube rotation
        # zha_event.zha_027d8b2b_2 - master bedroom 2 events
        # zha_event.zha_027d8b2b_3 - master bedroom 2  rotation
        print(data)
        if (data['unique_id'] == 'zha_event.zha_029bd185_2'):
            if (data['command'] == 'flip'):
                self.call_service('homeassistant/toggle', entity_id = 'group.christmas')

        if (data['unique_id'] == 'zha_event.zha_029bd185_3'):
            if (data['command'] == 'rotate_left'):
                self.call_service('homeassistant/turn_off', entity_id = 'light.entryway_light')
            if (data['command'] == 'rotate_right'):
                self.call_service('homeassistant/turn_on', entity_id = 'light.entryway_light', brightness = 255)

