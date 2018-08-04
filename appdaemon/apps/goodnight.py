##
# Automatically lock doors, turn off lights, and leave a dim night 
# light on for a few seconds so you can see to get down the hallway. 
##

import appdaemon.plugins.hass.hassapi as hass
from datetime import datetime, time

class GoodNight(hass.Hass):

    def initialize(self):
        self.listen_state(self.goodnight, "input_boolean.goodnight", new = "on")

        # Turn off at 6:15am
        self.run_daily(self.goodmorning, time(6,15,0))
        
    def goodnight(self, entity, attribute, old, new, kwargs):
        # Sanity Check
        if (self.time_in_range(time(20,00), time(23,59), datetime.now().time()) or self.time_in_range(time(00,00), time(5,00), datetime.now().time())):
            # Check if the front door is closed, and lock it if so
            if (self.get_state('binary_sensor.front_door_sensor') == 'off'):
                self.call_service('lock/lock', entity_id = 'lock.front_door_lock_locked')
            else:
                # Send a notification to close the door and lock it
                self.fire_event('tileboard', command='notify', target = 'living_room', title = 'Front Door Open', message = 'The Front Door is still open. Please close and lock the door.', sound = '/sounds/connected.mp3', type = 'error')
                # Abort the rest of the execution
                self.call_service('input_boolean/turn_off', entity_id = 'input_boolean.goodnight')
                return

            # TODO: make a better function for these so there's not so much repeat code.
            # Check if back door is open
            if (self.get_state('binary_sensor.back_door_sensor') == 'on'):
                # Send a notification to close the door and lock it
                self.fire_event('tileboard', command='notify', target = 'living_room', title = 'Back Door Open', message = 'The Back Door is still open. Please close and lock the door.', sound = '/sounds/connected.mp3', type = 'error')
                # Abort the rest of the execution
                self.call_service('input_boolean/turn_off', entity_id = 'input_boolean.goodnight')
                return
                
            # Check if the garage door is open
            if (self.get_state('binary_sensor.garage_door_sensor') == 'on'):
                # Send a notification to close the door and lock it
                self.fire_event('tileboard', command='notify', target = 'living_room', title = 'Garage Door Open', message = 'The Garage Door is still open. Please close it.', sound = '/sounds/connected.mp3', type = 'error')
                # Abort the rest of the execution
                self.call_service('input_boolean/turn_off', entity_id = 'input_boolean.goodnight')
                return
                
            # Check if the garage inside door is open
            if (self.get_state('binary_sensor.garage_inside_door') == 'on'):
                # Send a notification to close the door and lock it
                self.fire_event('tileboard', command='notify', target = 'living_room', title = 'Garage Inside Door Open', message = 'The inside Garage Door is still open. Please close and lock the door.', sound = '/sounds/connected.mp3', type = 'error')
                # Abort the rest of the execution
                self.call_service('input_boolean/turn_off', entity_id = 'input_boolean.goodnight')
                return
                
            # Check if the garage side door is open
            if (self.get_state('binary_sensor.garage_side_door') == 'on'):
                # Send a notification to close the door and lock it
                self.fire_event('tileboard', command='notify', target = 'living_room', title = 'Garage Side Door Open', message = 'The Garage Side Door is still open. Please close and lock the door.', sound = '/sounds/connected.mp3', type = 'error')
                # Abort the rest of the execution
                self.call_service('input_boolean/turn_off', entity_id = 'input_boolean.goodnight')
                return

            # Turn off TV
            self.call_service('homeassistant/turn_off', entity_id = 'media_player.living_room_tv')

            # Turn off Misc Devices
            self.call_service('homeassistant/turn_off', entity_id = 'switch.wax_melt_switch')
            self.call_service('homeassistant/turn_off', entity_id = 'switch.guest_bathroom_smartplug')
            
            # Turn off lights in communal areas (not bathrooms or bedrooms)
            self.call_service('homeassistant/turn_off', entity_id = 'light.back_porch_light')
            self.call_service('homeassistant/turn_off', entity_id = 'light.front_porch_light')
            self.call_service('homeassistant/turn_off', entity_id = 'light.kitchen_light')
            self.call_service('homeassistant/turn_off', entity_id = 'light.entryway_light')
            self.call_service('homeassistant/turn_off', entity_id = 'light.hallway_light')
            self.call_service('homeassistant/turn_off', entity_id = 'fan.living_room_fan')
            
            # If Living Room or Cabinet lights are on, set them to dim for ~30 seconds then turn off
            self.timer = False
            if (self.get_state('light.kitchen_cabinet_lights') == 'on'):
                self.timer = True
                self.call_service('homeassistant/turn_on', entity_id = 'light.kitchen_cabinet_lights', brightness = 10)
            if (self.get_state('light.living_room') == 'on' and self.get_state('light.living_room_accent_lights') == 'on'):
                self.timer = True
                self.call_service('homeassistant/turn_on', entity_id = 'light.living_room_accent_lights', brightness = 120)
                self.call_service('homeassistant/turn_off', entity_id = 'light.living_room')
            elif (self.get_state('light.living_room') == 'on'):
                self.timer = True
                self.call_service('homeassistant/turn_on', entity_id = 'light.living_room', brightness = 10)
            elif (self.get_state('light.living_room_accent_lights') == 'on'):
                self.timer = True
                self.call_service('homeassistant/turn_on', entity_id = 'light.living_room_accent_lights', brightness = 120)

            if (self.timer):
                self.handle = self.run_in(self.lightsout, 30)
            
            # Turn off Kindle Screens
            self.fire_event('tileboard', command='screen_off')
        else:
            self.fire_event('tileboard', command='notify', target = 'living_room', title = 'Are you sure?', message = 'It\'s too early for Goodnight. Try again between 8pm and 5am.', sound = '/sounds/connected.mp3', type = 'error', lifetime = 30)
            # Abort the rest of the execution
            self.call_service('input_boolean/turn_off', entity_id = 'input_boolean.goodnight')
            return
        
    # Turn off remaining lights after 30s timer
    def lightsout(self, kwargs):
        self.call_service('homeassistant/turn_off', entity_id = 'light.living_room')
        self.call_service('homeassistant/turn_off', entity_id = 'light.living_room_accent_lights')
        self.call_service('homeassistant/turn_off', entity_id = 'light.kitchen_cabinet_lights')
        
    def goodmorning(self, kwargs):
        self.call_service('input_boolean/turn_off', entity_id = 'input_boolean.goodnight')
        
    # Helper Functions
    def time_in_range(self, start, end, x):
        if start <= end:
            return start <= x <= end
        else:
            return start <= x or x <= end