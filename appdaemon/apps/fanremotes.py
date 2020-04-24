##
# Handle Pico Remotes for Controlling Zigbee Fans
##

import appdaemon.plugins.hass.hassapi as hass


class FanRemotes(hass.Hass):

    def initialize(self):
        self.listen_state(self.handle_light, "sensor.office_light_pico")
        self.listen_state(self.handle_light,
                          "sensor.master_bedroom_light_pico")
        self.listen_state(self.handle_light, "sensor.nursery_light_pico")
        self.listen_state(self.handle_light,
                          "sensor.living_room_fan_light_pico")
        self.listen_state(self.handle_light,
                          "sensor.guest_bathroom_pico")
        self.listen_state(self.handle_light,
                          "sensor.zoey_s_bedroom_pico")
        self.listen_state(self.handle_light,
                          "sensor.master_bedroom_lamp_pico")
        self.listen_state(self.handle_fan, "sensor.office_fan_pico")
        self.listen_state(self.handle_fan, "sensor.master_bedroom_fan_pico")
        self.listen_state(self.handle_fan, "sensor.nursery_fan_pico")
        self.listen_state(self.handle_fan, "sensor.living_room_fan_pico")

    def handle_light(self, entity, attribute, old, new, kwargs):
        self.log('Pico Button Press: {} - {}'.format(entity, new))
        remotes = {
            "sensor.office_light_pico": {
                'controlled_entity': 'light.guest_bedroom',
                'favorite_level': 10,
                'tablet': 'zoeys_room'
            },
            "sensor.master_bedroom_light_pico": {
                'controlled_entity': 'light.master_bedroom',
                'favorite_level': 10,
                'tablet': 'master_bedroom'
            },
            "sensor.nursery_light_pico": {
                'controlled_entity': 'light.nursery',
                'favorite_level': 100,
                'tablet': 'nursery'
            },
            "sensor.living_room_fan_light_pico": {
                'controlled_entity': 'light.living_room',
                'favorite_level': 5,
                'tablet': 'living_room'
            },
            "sensor.guest_bathroom_pico": {
                'controlled_entity': 'light.guest_bathroom_fan_light_level',
                'favorite_level': 50,
            },
            "sensor.zoey_s_bedroom_pico": {
                'controlled_entity': 'light.zoeys_lamp',
                'favorite_level': 15,
            },
            "sensor.master_bedroom_lamp_pico": {
                'controlled_entity': 'light.master_bedroom_lamp',
                'favorite_level': 120,
            }
        }

        remote = remotes[entity]

        if (new == '1'):
            # On

            # Wake up TileBoard tablet if one is specified and the light was previously off
            if ('tablet' in remote.keys()):
                if (self.get_state(remote['controlled_entity']) == 'off'):
                    self.fire_event(
                        'tileboard', command='screen_on', target=remote['tablet'])

            # Turn light on (full)
            self.call_service('homeassistant/turn_on',
                              entity_id=remote['controlled_entity'], brightness=255)

        if (new == '2'):
            # Favorite
            self.call_service('homeassistant/turn_on',
                              entity_id=remote['controlled_entity'], brightness=remote['favorite_level'])

        if (new == '4'):
            # Off
            self.call_service('homeassistant/turn_off',
                              entity_id=remote['controlled_entity'])

        if (new == '8'):
            # Up
            previous_level = self.get_state(
                remote['controlled_entity'], attribute='brightness')
            if not previous_level:
                previous_level = 0

            new_level = previous_level + 26
            if (new_level > 255):
                new_level = 255

            self.call_service('homeassistant/turn_on',
                              entity_id=remote['controlled_entity'],
                              brightness=new_level)

        if (new == '16'):
            # Down
            previous_level = self.get_state(
                remote['controlled_entity'], attribute='brightness')
            if not previous_level:
                previous_level = 0

            new_level = previous_level - 26
            if (new_level < 1):
                self.call_service('homeassistant/turn_off',
                                  entity_id=remote['controlled_entity'])
            else:
                self.call_service('homeassistant/turn_on',
                                  entity_id=remote['controlled_entity'],
                                  brightness=new_level)

    def handle_fan(self, entity, attribute, old, new, kwargs):
        self.log('Pico Button Press: {} - {}'.format(entity, new))
        if (entity == "sensor.office_fan_pico"):
            controlled_entity = "fan.guest_bedroom"
        if (entity == "sensor.master_bedroom_fan_pico"):
            controlled_entity = "fan.master_bedroom_fan"
        if (entity == "sensor.nursery_fan_pico"):
            controlled_entity = "fan.nursery_fan"
        if (entity == "sensor.living_room_fan_pico"):
            controlled_entity = "fan.living_room_fan"

        if (new == '1'):
            # On
            self.call_service('fan/turn_on', entity_id=controlled_entity)

        if (new == '2'):
            # Favorite
            self.call_service(
                'fan/set_speed', entity_id=controlled_entity, speed='low')

        if (new == '4'):
            # Off
            self.call_service('homeassistant/turn_off',
                              entity_id=controlled_entity)

        if (new == '8'):
            # Up
            self.call_service(
                'fan/set_speed', entity_id=controlled_entity, speed='medium')

        if (new == '16'):
            # Down
            self.call_service(
                'fan/set_speed', entity_id=controlled_entity, speed='lowest')
