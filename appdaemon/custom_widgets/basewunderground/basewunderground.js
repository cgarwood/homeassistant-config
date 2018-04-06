//Weather Underground Widget
//Designed for a (2x2) size

//TODO:
//- Switch from entity_picture to weather_icon

function basewunderground(widget_id, url, skin, parameters) {
	self = this;

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

	// Initialization
	self.widget_id = widget_id;

	// Parameters may come in useful later on
	self.parameters = parameters;

	var callbacks = [];

	// Define callbacks for entities - this model allows a widget to monitor multiple entities if needed
	// Initial will be called when the dashboard loads and state has been gathered for the entity
	// Update will be called every time an update occurs for that entity

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

	// Finally, call the parent constructor to get things moving
	WidgetBase.call(self, widget_id, url, skin, parameters, monitored_entities, callbacks);


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
			if (!isNaN(day)) {
				self.set_field(self, "weather_icon_"+day+"d", self.weather_mapping[icon[0]]['icon'])
			} else {
				self.set_field(self, "weather_icon", self.weather_mapping[icon[0]]['icon'])
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
			self.set_field(self, "weather_background", 'https://192.168.1.220/hadashboard/weather_backgrounds/' + background)
		} else {
			var field = state.entity_id.split(".")[1];
			self.set_field(self, field, state.state)
		}
	}
}