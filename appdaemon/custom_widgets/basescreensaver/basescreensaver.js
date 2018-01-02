function basescreensaver(widget_id, url, skin, parameters) {

	self = this
	self.widget_id = widget_id
	self.parameters = parameters
	
	self.OnButtonClick = OnButtonClick
	var callbacks = [
	{'selector': '#' + widget_id, 'action':'click','callback': self.OnButtonClick}
	]
	
	var monitored_entities = []
	
	WidgetBase.call(self, widget_id, url, skin, parameters, monitored_entities, callbacks)  

	updateTime(self)
	setInterval(updateTime, 500, self)

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
		
		if ("time_format" in self.parameters && self.parameters.time_format == "24hr")
		{
			time = h + ":" + m;
			pm = ""
		}
		else
		{
			time = formatHours(h) + ":" + m;
			pm = formatAmPm(h)
		}
		
		if ("show_seconds" in self.parameters && self.parameters.show_seconds == 1)
		{
			time = time + ":" + formatTime(s)
		}
		
		//time = time + pm;
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
	
	get_pictures()
	
	function get_pictures() {
		var photos = $.getJSON(self.parameters.path, function(d) {
			for (var i = 0; i < d.length; i++) {
				$("#slides").append('<li class="slide" style="background-image: url(\'https://192.168.1.220'+d[i]+'\');"></li>');
			}
		})
	}
	
	var slides = document.querySelectorAll('#slides .slide');
	var currentSlide = 0;
	var slideInterval = setInterval(nextSlide,6000);

	function nextSlide() {
		slides = document.querySelectorAll('#slides .slide');
		
		slides[currentSlide].className = 'slide';
		currentSlide = (currentSlide+1)%slides.length;
		slides[currentSlide].className = 'slide showing';
	}
	
	
	function OnButtonClick(self) {
		if ("url" in parameters)
        {
            url = parameters.url
        }
        else
        {
            url = "/" + parameters.dashboard
        }
        var i = 0;

        if ("args" in parameters)
        {
            
            url = url + "?"
            
            for (var key in parameters.args)
            {
                if (i != 0)
                {
                    url = url + "&"
                }
                url = url + key + "=" + parameters.args[key]
                i++
            }
        }
        if ("skin" in parameters)
        {
            theskin = parameters.skin
        }
        else
        {
            theskin = skin
        }
        if (i == 0)
        {
            url = url + "?skin=" + theskin
        }
        else
        {
            url = url + "&skin=" + theskin
        }
        command = "window.location.href = '" + url + "'"
		eval(command);
    }

}