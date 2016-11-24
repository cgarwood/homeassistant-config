# Home Assistant Configuration

Configuration files from my Home-Assistant installation, running on a Raspberry Pi 3.

Equipment includes:
- Lutron Caseta Light Switches (via Wink hub)
- GE Zwave Light Switches
- Nest Thermostat
- First Alert Zwave Smoke/CO Detector
- Ubiquiti Unifi Wifi (device_tracker)
- Amazon FireTV & Google Chromecast
- CyberPower UPS


## TODO List
- Clean-up/Organize and split configuration.yaml into multiple files
- UPS Automations
  - Push notifications when power goes out and comes back
  - Remote hibernate main PC when battery starts getting low (https://blogs.msdn.microsoft.com/powershell/2014/09/29/simple-http-api-for-executing-powershell-scripts/)
- Smoke/CO Detector should shut off HVAC when activated
- Push notification if doors are open and nobody is home
- Fix Guest Bathroom Auto Light automations


## TODO List (requires new devices/$$)
- Garage Door open/close sensor
- Smart Garage Door Opener
- Turn on closet light when door opened, turn off after 5-10 minutes or when door closed _(need 1x door sensor, 1x zwave switch)_
- Turn on attic lights when hatch pulled down, turn off when hatch put up. Push notification if attic lights are on more than a few hours _(need 1x door sensor, 2x zwave switch)_
- Auto-lock doors at night or when nobody home _(need 1x smart deadbolt)_
- Flood sensors & zwave water valve