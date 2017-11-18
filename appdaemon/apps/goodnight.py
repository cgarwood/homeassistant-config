##
# Automatically lock doors, turn off lights, and leave a dim night 
# light on for a few seconds so you can see to get down the hallway. 
##

import appdaemon.appapi as appapi

class GoodNight(appapi.AppDaemon):

    def initialize(self):
        self.listen_state(self.goodnight, "input_select.house_mode", new = "Asleep")

    def goodnight(self, entity, attribute, old, new, kwargs):
        # Check if the front door is closed, and lock it if so
        if (self.get_state('binary_sensor.front_door_sensor') == 'off'):
            self.call_service('lock/lock', entity_id = 'lock.front_door_lock_locked')
        else:
            # Send a notification to close the door and lock it
            self.call_service('notify/hatouch', title = 'Door Open', message = 'The Front Door is still open. Please close and lock the door.', data = {'tts':'The front door is still open. Please close and lock the front door', 'sound':'attention.mp3', 'type':'error'})
            # Abort the rest of the execution
            self.call_service('input_select/select_option', entity_id = 'input_select.house_mode', option = 'Home')
            return

        # Check if back door is open
        if (self.get_state('binary_sensor.back_door_sensor') == 'on'):
            # Send a notification to close the door and lock it
            self.call_service('notify/hatouch', title = 'Back Door Open', message = 'The Back Door is still open. Please close and lock the door.', data = {'tts':'The back door is still open. Please close and lock the back door', 'sound':'attention.mp3', 'type':'error'})
            # Abort the rest of the execution
            self.call_service('input_select/select_option', entity_id = 'input_select.house_mode', option = 'Home')
            return

        # Turn off TV
        self.call_service('homeassistant/turn_off', entity_id = 'media_player.living_room_tv')

        # Turn off Misc Devices
        self.call_service('homeassistant/turn_off', entity_id = 'switch.wax_melt_switch')
        
        # Turn off lights in communal areas (not bathrooms or bedrooms)
        self.call_service('homeassistant/turn_off', entity_id = 'light.back_porch')
        self.call_service('homeassistant/turn_off', entity_id = 'light.front_porch')
        self.call_service('homeassistant/turn_off', entity_id = 'light.kitchen')
        self.call_service('homeassistant/turn_off', entity_id = 'light.entryway')
        self.call_service('homeassistant/turn_off', entity_id = 'light.hallway')
        self.call_service('homeassistant/turn_off', entity_id = 'fan.living_room_fan')
        
        # If Living Room or Cabinet lights are on, set them to dim for ~30 seconds then turn off
        self.timer = False
        if (self.get_state('light.cabinet_lights') == 'on'):
            self.timer = True
            self.call_service('homeassistant/turn_on', entity_id = 'light.cabinet_lights', brightness = 10)
        if (self.get_state('light.living_room_fan_light') == 'on' and self.get_state('light.living_room') == 'on'):
            self.timer = True
            self.call_service('homeassistant/turn_on', entity_id = 'light.living_room', brightness = 120)
            self.call_service('homeassistant/turn_off', entity_id = 'light.living_room_fan_light')
        elif (self.get_state('light.living_room_fan_light') == 'on'):
            self.timer = True
            self.call_service('homeassistant/turn_on', entity_id = 'light.living_room_fan_light', brightness = 10)
        elif (self.get_state('light.living_room') == 'on'):
            self.timer = True
            self.call_service('homeassistant/turn_on', entity_id = 'light.living_room', brightness = 120)

        if (self.timer):
            self.handle = self.run_in(self.lightsout, 30)

        # Tell everyone goodnight :)
        self.call_service('notify/hatouch', title = 'Goodnight', message = 'Goodnight', data = {'tts':'Good night', 'persist':False})
        
        # Turn off Kindle/HATouch Screens
        self.call_service('hatouch/screen_off')
        
        
    # Turn off remaining lights after 30s timer
    def lightsout(self, kwargs):
        self.call_service('homeassistant/turn_off', entity_id = 'light.living_room_fan_light')
        self.call_service('homeassistant/turn_off', entity_id = 'light.living_room')
        self.call_service('homeassistant/turn_off', entity_id = 'light.cabinet_lights')