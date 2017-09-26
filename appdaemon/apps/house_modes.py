##
# Support for House Modes (Home/Away/Asleep/Vacation)
# Monitors the state of various entities/devices as well as date and time to
# do some automated changing of the House Mode
##

import appdaemon.appapi as appapi

class HouseModes(appapi.AppDaemon):

    def initialize(self):