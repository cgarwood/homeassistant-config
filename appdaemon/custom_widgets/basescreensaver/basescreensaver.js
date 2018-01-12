//TODO:
//- Add news slide
//- Add slide(s) for weather alerts
//- Include camera(s) in slideshow?

function basescreensaver(widget_id, url, skin, parameters) {

	self = this
	self.widget_id = widget_id
	self.parameters = parameters
	
	self.OnButtonClick = OnButtonClick
	var callbacks = [
		{'selector': '#' + widget_id, 'action':'click','callback': self.OnButtonClick}
	]
	
	self.OnStateAvailable = OnStateAvailable;
	self.OnStateUpdate = OnStateUpdate;
	
	var monitored_entities = [
		{"entity": "sensor.pws_temp_f", "initial": self.OnStateAvailable, "update": self.OnStateUpdate},
		{"entity": "sensor.pws_relative_humidity", "initial": self.OnStateAvailable, "update": self.OnStateUpdate},
		{"entity": "sensor.pws_weather", "initial": self.OnStateAvailable, "update": self.OnStateUpdate},
		{"entity": "sensor.pws_wind_dir", "initial": self.OnStateAvailable, "update": self.OnStateUpdate},
		{"entity": "sensor.pws_wind_mph", "initial": self.OnStateAvailable, "update": self.OnStateUpdate},
		{"entity": "sensor.pws_precip_1d", "initial": self.OnStateAvailable, "update": self.OnStateUpdate},
		{"entity": "sensor.pws_temp_high_1d_f", "initial": self.OnStateAvailable, "update": self.OnStateUpdate},
		{"entity": "sensor.pws_temp_low_1d_f", "initial": self.OnStateAvailable, "update": self.OnStateUpdate},
		{"entity": "sensor.pws_temp_high_2d_f", "initial": self.OnStateAvailable, "update": self.OnStateUpdate},
		{"entity": "sensor.pws_temp_low_2d_f", "initial": self.OnStateAvailable, "update": self.OnStateUpdate},
		{"entity": "sensor.pws_temp_high_3d_f", "initial": self.OnStateAvailable, "update": self.OnStateUpdate},
		{"entity": "sensor.pws_temp_low_3d_f", "initial": self.OnStateAvailable, "update": self.OnStateUpdate},
		{"entity": "sensor.pws_weather_1d", "initial": self.OnStateAvailable, "update": self.OnStateUpdate},
		{"entity": "sensor.pws_weather_2d", "initial": self.OnStateAvailable, "update": self.OnStateUpdate},
		{"entity": "sensor.pws_weather_3d", "initial": self.OnStateAvailable, "update": self.OnStateUpdate},
		{"entity": "sensor.pws_alerts", "initial": self.OnStateAvailable, "update": self.OnStateUpdate}
	];
	
	//Mapping Wunderground icons to new icons and background images
	self.weather_mapping = {
		'chanceflurries' : {'icon':'&#xe036','bg':'snow.jpg'},
		'chancerain' : {'icon':'&#xe009', 'bg':'rain.jpg'},
		'chancesleet' : {'icon':'&#xe009g','bg':'rain.jpg'},
		'chancesnow' : {'icon':'&#xe036','bg':'snow.jpg'},
		'chancetstorms' : {'icon':'&#xe026','bg':'thunderstorm.jpg'},
		'clear' : {'icon':'&#xe028','bg':'sunny.jpg'},
		'cloudy' : {'icon':'&#xe000','bg':'cloudy.jpg'},
		'flurries' : {'icon':'&#xe036','bg':'snow.jpg'},
		'fog' : {'icon':'&#xe01b','bg':'fog.jpg'},
		'hazy' : {'icon':'&#xe01b','bg':'fog.jpg'},
		'mostlycloudy' : {'icon':'&#xe001','bg':'partlycloudy.jpg'},
		'mostlysunny' : {'icon':'&#xe001','bg':'sunny.jpg'},
		'partlycloudy' : {'icon':'&#xe001','bg':'partlycloudy.jpg'},
		'partlysunny' : {'icon':'&#xe001','bg':'partlycloudy.jpg'},
		'sleet' : {'icon':'&#xe009','bg':'rain.jpg'},
		'rain' : {'icon':'&#xe009','bg':'rain.jpg'},
		'snow' : {'icon':'&#xe036','bg':'snow.jpg'},
		'sunny' : {'icon':'&#xe028','bg':'sunny.jpg'},
		'tstorms' : {'icon':'&#xe025','bg':'thunderstorms.jpg'},
		'nt_chanceflurries' : {'icon':'&#xe036','bg':'nt_snow.jpg'},
		'nt_chancerain' : {'icon':'&#xe009','bg':'nt_rain.jpg'},
		'nt_chancesleet' : {'icon':'&#xe009','bg':'nt_rain.jpg'},
		'nt_chancesnow' : {'icon':'&#xe036','bg':'nt_snow.jpg'},
		'nt_chancetstorms' : {'icon':'&#xe027','bg':'nt_thunderstorm.jpg'},
		'nt_clear' : {'icon':'&#xe02d','bg':'nt_sunny.jpg'},
		'nt_cloudy' : {'icon':'&#xe000','bg':'nt_cloudy.jpg'},
		'nt_flurries' : {'icon':'&#xe036','bg':'nt_snow.jpg'},
		'nt_fog' : {'icon':'&#xe01b','bg':'nt_fog.jpg'},
		'nt_hazy' : {'icon':'&#xe01b','bg':'nt_fog.jpg'},
		'nt_mostlycloudy' : {'icon':'&#xe000','bg':'nt_cloudy.jpg'},
		'nt_mostlysunny' : {'icon':'&#xe02d','bg':'nt_sunny.jpg'},
		'nt_partlycloudy' : {'icon':'&#xe002','bg':'nt_cloudy.jpg'},
		'nt_partlysunny' : {'icon':'&#xe000','bg':'nt_cloudy.jpg'},
		'nt_sleet' : {'icon':'&#xe003','bg':'nt_rain.jpg'},
		'nt_rain' : {'icon':'&#xe009','bg':'nt_rain.jpg'},
		'nt_snow' : {'icon':'&#xe036','bg':'nt_snow.jpg'},
		'nt_sunny' : {'icon':'&#xe02d','bg':'nt_sunny.jpg'},
		'nt_tstorms' : {'icon':'&#xe025','bg':'nt_thunderstorm.jpg'}
	}
	
	self.weather_alert_count = 0;
	
	WidgetBase.call(self, widget_id, url, skin, parameters, monitored_entities, callbacks)  

	//Start the clock loop
	updateTime(self)
	setInterval(updateTime, 500, self)
	
	//Fetch pictures for the slideshow
	get_pictures()
	
	//Functions to update the clock
	function updateTime(self) {
		var today = new Date();
		h = today.getHours();
		m = today.getMinutes();
		s = today.getSeconds();
		m = formatTime(m);
		
		self.set_field(self, "date", today.toLocaleDateString());
		var weekdays = ["Sunday","Monday","Tuesday","Wednesday","Thursday","Friday","Saturday"];
		self.set_field(self, "dayOfWeek", weekdays[today.getDay()]);
		var months = ["January","February","March","April","May","June","July","August","September","October","November","December"];
		self.set_field(self, "monthText", months[today.getMonth()]);
		self.set_field(self, "day", today.getDate());
		
		if ("time_format" in self.parameters && self.parameters.time_format == "24hr") {
			time = h + ":" + m;
			pm = ""
		} else {
			time = formatHours(h) + ":" + m;
			pm = formatAmPm(h)
		}
		
		if ("show_seconds" in self.parameters && self.parameters.show_seconds == 1) {
			time = time + ":" + formatTime(s)
		}
		
		self.set_field(self, "time", time);
		self.set_field(self, "ampm", pm);
	}

	function formatTime(i) {
		if (i < 10 ) { return "0" + i; }
		else { return i; }
	}

	function formatAmPm(h) {
		if (h >= 12) { return "pm"; }
		else { return "am";	}
	}

	function formatHours(h)	{
		if (h > 12)	{ return h - 12; }
		else if (h == 0) { return 12; }
		else { return h; }
	}
	
	//Function to get the JSON list of pictures from the specified path and append it to the list of slides
	function get_pictures() {
		var photos = $.getJSON(self.parameters.picture_source, function(d) {
			for (var i = 0; i < d.length; i++) {
				var image_url = self.parameters.picture_path + d[i];
				$("#slides").append('<li class="slide" style="background-image: url(\''+image_url+'\');"></li>');
			}
		})
	}
	
	//Set up the slideshow
	var slides = document.querySelectorAll('#slides .slide');
	var currentSlide = 0;
	var slideTimer = 6000;
	if (slides[currentSlide].classList.contains('timer-double')) {
		var slideInterval = setTimeout(nextSlide,slideTimer * 2);
	} else {
		var slideInterval = setTimeout(nextSlide,slideTimer);
	}

	function nextSlide() {
		slides = document.querySelectorAll('#slides .slide');
		slides[currentSlide].classList.remove('showing');
		if (slides[(currentSlide+1)%slides.length].classList.contains('weather-alerts') && self.weather_alert_count == 0) {
			//Skip the weather alerts slide if there's not an active alert
			currentSlide = (currentSlide+2)%slides.length
		} else {
			currentSlide = (currentSlide+1)%slides.length;
		}
		slides[currentSlide].classList.add('showing');
		
		if (slides[currentSlide].classList.contains('no-overlay')) {
			document.getElementById('overlay').classList.remove('showing');
		} else {
			if (!document.getElementById('overlay').classList.contains('showing')) {
				document.getElementById('overlay').classList.add('showing');
			}
		}
		
		if (slides[currentSlide].classList.contains('timer-double')) {
			slideInterval = setTimeout(nextSlide,slideTimer*2);
		} else {
			slideInterval = setTimeout(nextSlide,slideTimer);
		}
	}
	
	
	function OnButtonClick(self) {
		if ("url" in parameters) {
			url = parameters.url
		} else {
			url = "/" + parameters.dashboard
		}
		var i = 0;

		if ("args" in parameters) {
			url = url + "?"	
			for (var key in parameters.args) {
				if (i != 0) {
					url = url + "&"
				}
				url = url + key + "=" + parameters.args[key]
				i++
			}
		}
		if ("skin" in parameters) {
			theskin = parameters.skin
		} else {
			theskin = skin
		}
		if (i == 0)	{
			url = url + "?skin=" + theskin
		} else {
			url = url + "&skin=" + theskin
		}
		command = "window.location.href = '" + url + "'"
		eval(command);
	}
	
	function OnStateUpdate(self, state) {
		if (state.entity_id == "sensor.pws_alerts") {
			if (parseInt(state.state) > 0) {
				self.set_field(self, "weather_alert_title", state.attributes.Description)
				self.set_field(self, "weather_alert_message", state.attributes.Messagereplace(/([^>\r\n\r\n]?)(\r\n\r\n|\n\r\n\r|\r\r|\n\n)/g, '$1' + '<br><br>' + '$2'))
				self.set_field(self, "weather_alert_expires", state.attributes.Expires)
				self.set_field(self, "weather_alert_date", state.attributes.Date)
			}
			self.weather_alert_count = state.state;
		}
		set_view(self, state)
	}

	function OnStateAvailable(self, state) {
		if (state.entity_id == "sensor.pws_temp_f") {
			self.set_field(self, "unit", state.attributes.unit_of_measurement)
		}
		if (state.entity_id == "sensor.pws_alerts") {
			if (parseInt(state.state) > 0) {
				self.set_field(self, "weather_alert_title", state.attributes.Description)
				self.set_field(self, "weather_alert_message", state.attributes.Message.replace(/([^>\r\n\r\n]?)(\r\n\r\n|\n\r\n\r|\r\r|\n\n)/g, '$1' + '<br><br>' + '$2'))
				self.set_field(self, "weather_alert_expires", state.attributes.Expires)
				self.set_field(self, "weather_alert_date", state.attributes.Date)
			}
			self.weather_alert_count = state.state;
		}
		set_view(self, state)
	}

	function set_view(self, state) {
		var extractIcons = ['sensor.pws_weather','sensor.pws_weather_1d','sensor.pws_weather_2d','sensor.pws_weather_3d']
		
		if (extractIcons.includes(state.entity_id)) {
			var len = state.entity_id.length
			var day = state.entity_id.substring(len-2, len-1)
			
			var string = state.attributes.entity_picture.split('/');
			var icon = string[string.length-1].split('.');
			if (self.weather_mapping[icon[0]]['icon'] !== undefined) {
				if (!isNaN(day)) {
					self.set_field(self, "weather_icon_"+day+"d", self.weather_mapping[icon[0]]['icon'])
				} else {
					self.set_field(self, "weather_icon", self.weather_mapping[icon[0]]['icon'])
				}
			}
		}
		if (state.entity_id == "sensor.pws_weather") {
			var string = state.attributes.entity_picture.split('/');
			var icon = string[string.length-1].split('.');
			if (self.weather_mapping[icon[0]]['bg'] !== undefined) {
				var background = self.weather_mapping[icon[0]]['bg'];
			} else {
				//Default background
				var background = 'partlycloudy.jpg';
			}
			self.set_field(self, "weather_background", self.parameters.weather_background_path + background)
		} else {
			var field = state.entity_id.split(".")[1];
			self.set_field(self, field, state.state)
		}
	}
}