function basewunderground(widget_id, url, skin, parameters) {
	// Will be using "self" throughout for the various flavors of "this"
	// so for consistency ...

	self = this;

	self.weather_icons = {
		"rain": '&#xe009',
		"snow": '&#xe036',
		"sleet": '&#xe003',
		"wind": '&#xe021',
		"fog": '&#xe01b',
		"cloudy": '&#xe000',
		"clear-day": '&#xe028',
		"clear-night": '&#xe02d',
		"partly-cloudy-day": '&#xe001',
		"partly-cloudy-night": '&#xe002'    
	};
	
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

	// Store on brightness or fallback to a default

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

	// Function Definitions

	// The StateAvailable function will be called when
	// self.state[<entity>] has valid information for the requested entity
	// state is the initial state
	// Methods

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
        }
		else {
			var field = state.entity_id.split(".")[1];
			self.set_field(self, field, state.state)
		}
	}
}