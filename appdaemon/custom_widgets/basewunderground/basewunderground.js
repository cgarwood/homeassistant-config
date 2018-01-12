//Weather Underground Widget
//Designed for a (2x2) size

//TODO:
//- Switch from entity_picture to weather_icon

function basewunderground(widget_id, url, skin, parameters) {
	self = this;

	//TODO: Combine self.bg_mapping and self.weather_icons into a single object
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
	
	//Mapping Wunderground icons to background images
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
			if (!isNaN(day)) {
				self.set_field(self, "weather_icon_"+day+"d", state.attributes.entity_picture)
			} else {
				self.set_field(self, "weather_icon", state.attributes.entity_picture)
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