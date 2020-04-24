##
# Set the color of the indicator LEDs on the Master Bathroom light switches
# based on work schedules.
##

import appdaemon.plugins.hass.hassapi as hass
import datetime
import dateutil.parser


class MasterBathroomIndicatorLights(hass.Hass):

    def initialize(self):
        green_time = datetime.time(6,30,0)
        self.run_daily(self.led_green, green_time)

        orange_time = datetime.time(7,0,0)
        self.run_daily(self.led_orange, orange_time)

        red_time = datetime.time(7,10,0)
        self.run_daily(self.led_red, red_time)

        reset_time = datetime.time(7,30,0)
        self.run_daily(self.reset, reset_time)

    def led_green(self, kwargs):
        self.set_color(80)

    def led_orange(self, kwargs):
        self.set_color(30)

    def led_red(self, kwargs):
        self.set_color(0)

    def reset(self, kwargs):
        self.set_color(170)

    def set_color(self, value):
        self.call_service('zwave/set_config_parameter', node_id=52, parameter=13, value=value)
        self.call_service('zwave/set_config_parameter', node_id=53, parameter=5, value=value)
        self.call_service('zwave/set_config_parameter', node_id=54, parameter=13, value=value)
