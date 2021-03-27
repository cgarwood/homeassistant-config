##
# National Weather Service Weather Alerts
# Monitors specific alert types and plays an alert tone & TTS on tablets
#
# TODO: Different alert tones for different alert types?
##

import appdaemon.plugins.hass.hassapi as hass
import datetime
import requests


class WeatherAlerts(hass.Hass):

    def initialize(self):
        self.alerts = {}
        self.monitored_alerts = [
            "Tornado Warning",
            "Severe Thunderstorm Warning",
            # "Severe Thunderstorm Watch",
            "Severe Weather Statement",
            # "Special Weather Statement"
        ]
        now = datetime.datetime.now() + datetime.timedelta(seconds=1)
        self.run_every(self.check_alerts, now, 2 * 60)

    def check_alerts(self, kwargs):
        url = self.args["alerts_url"]
        resp = requests.get(url)
        data = resp.json()

        for alert in data['features']:
            alert = alert['properties']
            # self.log("Processing alert: {}".format(alert['event']))

            # Only track specific alert types
            if (alert['event'] not in self.monitored_alerts):
                # self.log("Ignoring alert: {}".format(alert['event']))
                continue

            # If we already have the alert in the list, check and see if the details have changed
            if (alert['id'] in self.alerts.keys()):
                if (alert['description'] == self.alerts[alert['id']]['description']):
                    # It's the same, do nothing
                    # self.log("Alert Unchanged: {}".format(alert['event']))
                    continue

            # Update our local cache
            self.alerts[alert['id']] = alert
            self.log("New alert: {}".format(alert['event']))

            # Set message for TTS announcement
            message = alert['description'].replace("*","")
            message = message.replace('\n',"")

            self.fire_event('snapcast_notify', sound='local:eas2.mp3', tts=message)
