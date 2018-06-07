##
# WeatherUnderground Weather Alerts
# Monitors specific alert types and plays an alert tone & TTS on tablets
#
# TODO: Different alert tones for different alert types?
##

import appdaemon.plugins.hass.hassapi as hass

class WeatherAlerts(hass.Hass):

    def initialize(self):
        self.listen_state(self.handle_alerts, "sensor.pws_alerts", attribute = "all")
    
    def handle_alerts(self, entity, attribute, old, new, kwargs):
        
        # Alert types to monitor and send alert tone/TTS:
        monitored_alerts = {
            "TOR" : "Tornado Warning",
            "WRN" : "Severe Thunderstorm Warning",
            "SPE" : "Special Weather Statement",
            "SVR" : "Severe Weather Statement"
        }
        
        alert = False
        
        # If the sensor state is only 1, the alert type is not appended to the attributes.
        if (int(new['state']) == 1):
            for k,v in monitored_alerts.items():
                # Check if the alert should be monitored
                if (new['attributes']['Description'] == v):
                    if (int(old['state']) > 1):
                        # Check if it's the same alert so we don't fire the alert tone again
                        if (new['attributes']['Message'] != old['attributes']['Message_' + k]):
                            # We have a new alert message
                            alert = True
                    else:
                        # Check if the message has changed
                        if (new['attributes']['Message'] != old['attributes']['Message']):
                            alert = True
                           
            # If we have a new alert, fire off the alert tone and read the TTS
            if (alert == True):
                message = new['attributes']['Message'].split('Lat...Lon')[0]
                self.fire_event('hadashboard', command='play_sound', sound = 'eas.mp3', tts = message)
        
        # If the state is > 1, the alert type is appended to the attributes
        elif (int(new['state']) > 1):
            for k,v in monitored_alerts.items():
                if ('Description_'+k in new['attributes']):
                    # We have a monitored alert, see if it's new
                    
                    if (int(old['state']) < 2):
                        oldMessage = old['attributes']['Message'];
                    else:
                        oldMessage = old['attributes']['Message_'+k];
                        
                    if (new['attributes']['Message_'+k] != oldMessage):
                        # New message
                        alert = True
                        message = new['attributes']['Message_'+k].split('Lat...Lon')[0]
                        
            if (alert == True):
                self.fire_event('hadashboard', command='play_sound', sound = 'eas.mp3', tts = message)
                