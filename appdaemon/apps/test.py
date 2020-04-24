##
# Plays a chime on Tileboard when exterior doors are opened or closed.
##

import appdaemon.plugins.hass.hassapi as hass

class Test(hass.Hass):

    async def initialize(self):
        self.listen_state(self.test, "input_boolean.test")

    async def test(self, entity, attribute, old, new, kwargs):
        if (new == "on"):
            self.call_service('media_player/play_media',
                              entity_id='media_player.living_room_echo',
                              media_content_type='sound',
                              media_content_id='amzn_sfx_doorbell_chime_01')
            #await self.sleep(1)
            self.call_service('media_player/play_media',
                              entity_id='media_player.master_bedroom_echo',
                              media_content_type='sound',
                              media_content_id='amzn_sfx_doorbell_chime_01')
            await self.sleep(1)
            self.call_service('notify/alexa_media',
                              target=['media_player.living_room_echo', 'media_player.master_bedroom_echo'],
                              data={'type':'announce'},
                              message='doorbell test ding dong')