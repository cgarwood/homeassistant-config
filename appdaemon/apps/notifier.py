##
# Manage audible notifications to tablets
##

import appdaemon.plugins.hass.hassapi as hass
from datetime import datetime, time

class Notifier(hass.Hass):
    def initialize(self):
        self.listen_event(self.notify, "snapcast_notify")

    def notify(self, event_name, data, kwargs):
        self.target = data.get('target', "primary")
        self.max_volume = data.get('max_volume', False)
        self.sound = data.get('sound')
        self.message = data.get('tts')
        
        self.entity = f"group.snapcast_kiosks_{self.target}"

        # Take a snapshot of current player configuration
        self.call_service('snapcast/snapshot', entity_id=self.entity)

        # Switch to notifications source
        self.call_service('media_player/select_source', entity_id=self.entity, source="notifications")

        # If max volume is set, turn the volume up
        if (self.max_volume):
            self.call_service("media_player/set_volume", entity_id=self.entity, level=1)

        # If we have a sound file, play it
        if self.sound is not None:
            if (self.sound[0:6] == "local:"):
                self.sound = f"{self.args['sounds_url']}/{self.sound[6:]}"
            self.call_service(
                "media_player/play_media",
                entity_id="media_player.mpd_notifications",
                media_content_type="music",
                media_content_id=self.sound
            )

            # If we have both a sound file and a TTS, wait for the sound to finish before playing the TTS
            if self.message is not None:
                self.listen_state(self.wait_then_tts, 'media_player.mpd_notifications', new="off", oneshot=True)
                return
            
            # Restore snapcast media players
            self.listen_state(self.restore, 'media_player.mpd_notifications', new="off", oneshot=True)
            return

        # If we have a TTS but no sound, go ahead and play the TTS
        if self.message is not None:
            self.tts()


    def wait_then_tts(self, entity, attribute, old, new, kwargs):
        self.tts()

    def tts(self):
        # Play the TTS
        print("playing tts", self.message)
        self.call_service('tts/cloud_say', 
            entity_id="media_player.mpd_notifications",
            message=self.message
        )

        # Restore snapcast media players
        self.listen_state(self.restore, 'media_player.mpd_notifications', new="stopped", oneshot=True)

    def restore(self, entity, attribute, old, new, kwargs):
        self.call_service('snapcast/restore', entity_id=self.entity)