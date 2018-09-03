##
# Monitor Zwave Smoke & Carbon Monoxide Detectors
# Turn on lights, handle HVAC, and send alerts if an alarm goes off
##

import appdaemon.plugins.hass.hassapi as hass

class SmokeDetectors(hass.Hass):

    def initialize(self):
        entities = [
            'sensor.garage_smoke_detector_alarm_type',
            'sensor.hallway_smoke_detector_alarm_type',
            'sensor.nursery_smoke_detector_alarm_type',
            'sensor.office_smoke_detector_alarm_type'
        ]
        
        for e in entities:
            self.listen_state(self.handle_alarm, e)
            
    def handle_alarm(self, entity, attribute, old, new, kwargs):
    
        # Actions for all alarms
        if (new == '1' or new == '2' or new == '12'):
            # Turn on lights so we can see to get out
            self.call_service('homeassistant/turn_on', entity_id = 'group.emergency_lights')
               
            # Unlock the front door
            self.call_service('lock/unlock', entity_id = 'lock.front_door_lock_locked')
            
            # Turn off HVAC
            self.call_service('climate/set_operation_mode', entity_id = 'climate.hallway', operation_mode = 'off')
        
            # Get alarm location
            attributes = self.get_state(entity, attribute = 'all')
            location = attributes['attributes']['friendly_name'].split(' ')[0]

            # Turn on TileBoard displays
            self.fire_event('tileboard', command='screen_on')
            
        # Custom actions depending on alarm type
        if (new == '1'):
            # Smoke
            
            # Turn off fans
            self.call_service('homeassistant/turn_off', entity_id = 'group.all_fans')
            self.call_service('homeassistant/turn_off', entity_id = 'switch.guest_bathroom_fan_switch')
            
            # Send an alert
            self.call_service('notify/ios', title = "Smoke Detected", message = 'Smoke detected in ' + location)
            self.fire_event('tileboard', command='notify', title = 'Smoke Detected', message = 'Smoke detected in ' + location, sound = '/sounds/fire.mp3', type = 'error')
            
        elif (new == '2'):
            # Carbon Monoxide
            
            # Turn on exhaust fans
            self.call_service('homeassistant/turn_on', entity_id = 'switch.guest_bathroom_fan_switch')

            # FUTURE: Open garage door if CO detected in garage (need a smart garage door opener first)
            
            # Send an alert
            self.call_service('notify/ios', title = "Carbon Monoxide Detected", message = 'Carbon Monoxide detected in ' + location)
            self.fire_event('tileboard', command='notify', title = 'Carbon Monoxide Detected', message = 'Carbon Monoxide detected in ' + location, sound = '/sounds/fire.mp3', type = 'error')

        elif (new == '12'):
            # Test Button

            # Send an alert
            self.call_service('notify/ios', title = "Smoke Detector Test", message = 'Testing ' + location + ' smoke detector')
            self.fire_event('tileboard', command='notify', title = 'Smoke Detector Test', message = 'Testing ' + location + ' smoke detector', sound = '/sounds/fire.mp3', type = 'error')
