##
# Send notifications if mailbox is opened
##

import appdaemon.plugins.hass.hassapi as hass
from datetime import datetime, time

class Mailbox(hass.Hass):
    def initialize(self):
        self.listen_state(self.chime, "binary_sensor.mailbox_sensor")

    def chime(self, entity, attribute, old, new, kwargs):

        if (new == "on"):
            self.call_service('camera/snapshot', entity_id="camera.driveway_cam", filename=f"{self.args['tmp_path']}/driveway.jpg")
            url = f"{self.args['tmp_url']}/driveway.jpg"
            self.log(f"url is {url}")
            attachment = {
                "content-type": "jpeg",
                "url": url
            }
            self.call_service('notify/charles', title="\uD83D\uDCEC You've Got Mail", message="", data={"attachment":attachment})

            if (self.get_state("input_boolean.goodnight") == "off"):
                self.fire_event("tileboard", command="play_sound", sound="/sounds/yougotmail.mp3")
