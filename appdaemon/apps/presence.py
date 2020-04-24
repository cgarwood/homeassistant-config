##
# Extended presence-detection support
# Adapted from https://philhawthorne.com/making-home-assistants-presence-detection-not-so-binary/
##

import appdaemon.plugins.hass.hassapi as hass

class Presence(hass.Hass):

    def initialize(self):
        # Handle device trackers
        self.listen_state(self.handle_presence, "person.charles")
        self.listen_state(self.handle_presence, "person.tina")

        # Mark Home if Just Arrived for 10 minutes
        self.listen_state(self.mark_home, "input_select.charles_status", new = "Just Arrived", duration = 600)
        self.listen_state(self.mark_home, "input_select.tina_status", new = "Just Arrived", duration = 600)

        # Mark Away if Just Left for 10 minutes
        self.listen_state(self.mark_away, "input_select.charles_status", new = "Just Left", duration = 600)
        self.listen_state(self.mark_away, "input_select.tina_status", new = "Just Left", duration = 600)

        # Mark Extended Away if Away for 12 hours
        self.listen_state(self.mark_extended_away, "input_select.charles_status", new = "Away", duration = 43200)
        self.listen_state(self.mark_extended_away, "input_select.tina_status", new = "Away", duration = 43200)

        # Initialize event handlers
        self.handle_home = {'charles':None,'tina':None}
        self.handle_away = {'charles':None,'tina':None}
        self.handle_extended_away = {'charles':None,'tina':None}

    def handle_presence(self, entity, attribute, old, new, kwargs):
        # Figure out who based on entity_id
        person = self.get_person_by_entity_id(entity)

        # Get the person's current status
        current_status = self.get_state("input_select."+person+"_status")

        # If the person has come home
        if (new == "home"):
            # If they had Just Left, skip the Just Arrived portion and mark them Home
            if (current_status == "Just Left"):
                self.call_service('input_select/select_option', entity_id = 'input_select.'+person+'_status', option = 'Home')
            # Otherwise, if they were Away or another state, mark them as Just Arrived
            else:
                self.call_service('input_select/select_option', entity_id = 'input_select.'+person+'_status', option = 'Just Arrived')

        # If the person has left
        elif (new == "not_home"):
            self.call_service('input_select/select_option', entity_id = 'input_select.'+person+'_status', option = 'Just Left')

    def mark_home(self, entity, attribute, old, new, kwargs):
        person = self.get_person_by_entity_id(entity)
        self.call_service('input_select/select_option', entity_id = 'input_select.'+person+'_status', option = 'Home')

    def mark_away(self, entity, attribute, old, new, kwargs):
        person = self.get_person_by_entity_id(entity)
        self.call_service('input_select/select_option', entity_id = 'input_select.'+person+'_status', option = 'Away')

    def mark_extended_away(self, entity, attribute, old, new, kwargs):
        person = self.get_person_by_entity_id(entity)
        self.call_service('input_select/select_option', entity_id = 'input_select.'+person+'_status', option = 'Away')

    def get_person_by_entity_id(self, entity):
        if (entity == "person.charles" or entity == "input_select.charles_status"): person = "charles"
        elif (entity == "person.tina" or entity == "input_select.tina_status"): person = "tina"
        else: person = "unknown"
        return person