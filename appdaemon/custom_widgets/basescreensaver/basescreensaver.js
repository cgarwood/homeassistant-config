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
	];
	
	//Mapping Wunderground icons to background images
	//TODO: Combine self.bg_mapping and self.weather_icons into a single object
	self.bg_mapping = {
		'chanceflurries' : 'snow.jpg',
		'chancerain' : 'rain.jpg',
		'chancesleet' : 'rain.jpg',
		'chancesnow' : 'snow.jpg',
		'chancetstorms' : 'thunderstorm.jpg',
		'clear' : 'sunny.jpg',
		'cloudy' : 'cloudy.jpg',
		'flurries' : 'snow.jpg',
		'fog' : 'fog.jpg',
		'hazy' : 'fog.jpg',
		'mostlycloudy' : 'partlycloudy.jpg',
		'mostlysunny' : 'partlycloudy.jpg',
		'partlycloudy' : 'partlycloudy.jpg',
		'partlysunny' : 'partlycloudy.jpg',
		'sleet' : 'rain.jpg',
		'rain' : 'rain.jpg',
		'snow' : 'snow.jpg',
		'sunny' : 'sunny.jpg',
		'tstorms' : 'thunderstorm.jpg',
		'nt_chanceflurries' : 'nt_snow.jpg',
		'nt_chancerain' : 'nt_rain.jpg',
		'nt_chancesleet' : 'nt_rain.jpg',
		'nt_chancesnow' : 'nt_snow.jpg',
		'nt_chancetstorms' : 'nt_thunderstorm.jpg',
		'nt_clear' : 'nt_sunny.jpg',
		'nt_cloudy' : 'nt_cloudy.jpg',
		'nt_flurries' : 'nt_snow.jpg',
		'nt_fog' : 'nt_fog.jpg',
		'nt_hazy' : 'nt_fog.jpg',
		'nt_mostlycloudy' : 'nt_cloudy.jpg',
		'nt_mostlysunny' : 'nt_sunny.jpg',
		'nt_partlycloudy' : 'nt_cloudy.jpg',
		'nt_partlysunny' : 'nt_cloudy.jpg',
		'nt_sleet' : 'nt_rain.jpg',
		'nt_rain' : 'nt_rain.jpg',
		'nt_snow' : 'nt_snow.jpg',
		'nt_sunny' : 'nt_sunny.jpg',
		'nt_tstorms' : 'nt_thunderstorm.jpg'
	}
	self.weather_icons = {
		'chanceflurries' : '&#xe036',
		'chancerain' : '&#xe009',
		'chancesleet' : '&#xe009g',
		'chancesnow' : '&#xe036',
		'chancetstorms' : '&#xe026',
		'clear' : '&#xe028',
		'cloudy' : '&#xe000',
		'flurries' : '&#xe036',
		'fog' : '&#xe01b',
		'hazy' : '&#xe01b',
		'mostlycloudy' : '&#xe001',
		'mostlysunny' : '&#xe001',
		'partlycloudy' : '&#xe001',
		'partlysunny' : '&#xe001',
		'sleet' : '&#xe009',
		'rain' : '&#xe009',
		'snow' : '&#xe036',
		'sunny' : '&#xe028',
		'tstorms' : '&#xe025',
		'nt_chanceflurries' : '&#xe036',
		'nt_chancerain' : '&#xe009',
		'nt_chancesleet' : '&#xe009',
		'nt_chancesnow' : '&#xe036',
		'nt_chancetstorms' : '&#xe027',
		'nt_clear' : '&#xe02d',
		'nt_cloudy' : '&#xe000',
		'nt_flurries' : '&#xe036',
		'nt_fog' : '&#xe01b',
		'nt_hazy' : '&#xe01b',
		'nt_mostlycloudy' : '&#xe000',
		'nt_mostlysunny' : '&#xe02d',
		'nt_partlycloudy' : '&#xe002',
		'nt_partlysunny' : '&#xe000',
		'nt_sleet' : '&#xe003',
		'nt_rain' : '&#xe009',
		'nt_snow' : '&#xe036',
		'nt_sunny' : '&#xe02d',
		'nt_tstorms' : '&#xe025'
	};
	
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
	//TODO: convert hardcoded background-image url to config variable
	function get_pictures() {
		var photos = $.getJSON(self.parameters.path, function(d) {
			for (var i = 0; i < d.length; i++) {
				$("#slides").append('<li class="slide" style="background-image: url(\'https://192.168.1.220'+d[i]+'\');"></li>');
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
		currentSlide = (currentSlide+1)%slides.length;
		slides[currentSlide].classList.add('showing');
		
		if (slides[currentSlide].classList.contains('noclock')) {
			document.getElementById('datetime').classList.remove('showing');
		} else {
			if (!document.getElementById('datetime').classList.contains('showing')) {
				document.getElementById('datetime').classList.add('showing');
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
		set_view(self, state)
	}

	function OnStateAvailable(self, state) {
		if (state.entity_id == "sensor.pws_temp_f") {
			self.set_field(self, "unit", state.attributes.unit_of_measurement)
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
			if (self.bg_mapping[icon[0]] !== undefined) {
				if (!isNaN(day)) {
					self.set_field(self, "weather_icon_"+day+"d", self.weather_icons[icon[0]])
				} else {
					self.set_field(self, "weather_icon", self.weather_icons[icon[0]])
				}
			}
		}
		if (state.entity_id == "sensor.pws_weather") {
			var string = state.attributes.entity_picture.split('/');
			var icon = string[string.length-1].split('.');
			if (self.bg_mapping[icon[0]] !== undefined) {
				var background = self.bg_mapping[icon[0]];
			} else {
				//Default background
				var background = 'partlycloudy.jpg';
			}
			self.set_field(self, "weather_background", 'https://192.168.1.220/hadashboard/weather_backgrounds/' + background)
		} else {
			var field = state.entity_id.split(".")[1];
			self.set_field(self, field, state.state)
		}
	}

}