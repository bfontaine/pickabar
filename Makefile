CSS = static/css

$(CSS)/app.css: $(CSS)/app.scss
	scss $^ >| $@
