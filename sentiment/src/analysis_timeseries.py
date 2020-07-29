import pandas as pd
import numpy as np

from bokeh import events
from bokeh.models import BoxAnnotation, ColorPicker, CustomJSFilter, Button, Div, ColumnDataSource, CustomJS, HoverTool
from bokeh.models.widgets import Slider, CheckboxGroup, Select
from bokeh.plotting import Figure
from bokeh.layouts import column, row
from bokeh.palettes import Spectral4
from bokeh.plotting import figure, output_file, show
from bokeh.sampledata.stocks import AAPL, GOOG, IBM, MSFT
#https://docs.bokeh.org/en/latest/docs/user_guide/interaction/callbacks.html

def getTimeSeries_notworking(df_tws):
	"""Plots a line for twitter counts for each keyword."""

	df_tws['date'] = pd.to_datetime(df_tws['date'], format='%m/%d/%Y')
	grouped = df_tws.groupby([pd.Grouper(key='date', freq='D'),'keyword'])['sentiment'].count().to_frame(name = 'count').reset_index()
	#grouped = grouped.pivot(index='date', columns = 'keyword', values='count')
	#print(grouped)
	source = ColumnDataSource(grouped)

	tools = ["box_select", "hover", "reset"]
	p = figure(plot_height=400, x_axis_type='datetime', tools=tools)
	# #TODO Make time series plot versatile so it can handle any amount of series.
	# p.line(x='date', y='art', source=source, line_width=2, color='blue', alpha=0.8, legend_label='art')
	# p.line(x='date', y='music', source=source, line_width=2, color='red', alpha=0.8, legend_label='music')
	# p.line(x='date', y='sing', source=source, line_width=2, color='green', alpha=0.8, legend_label='sing')

	p.vbar(x='date', source=source, top="art", line_color="white", width=1)
	p.legend.location = "top_left"
	p.legend.click_policy = "hide"

	#output_file("interactive_legend.html", title="interactive_legend.py example")

	return p

def getTimeSeries(df_tws):
	"""Plots a line for twitter counts for each keyword."""

	df_tws['date'] = pd.to_datetime(df_tws['date'], format='%m/%d/%Y')
	grouped = df_tws.groupby([pd.Grouper(key='date', freq='D'),'keyword'])['sentiment'].count().to_frame(name = 'count').reset_index()
	grouped = grouped.pivot(index='date', columns = 'keyword', values='count')
	#print(grouped)
	source = ColumnDataSource(grouped)

	tools = ["box_select", "hover", "reset"]
	p = figure(plot_height=400, x_axis_type='datetime', tools=tools)
	#TODO Make time series plot versatile so it can handle any amount of series.
	p.line(x='date', y='art', source=source, line_width=2, color='blue', alpha=0.8, legend_label='art')
	p.line(x='date', y='music', source=source, line_width=2, color='red', alpha=0.8, legend_label='music')
	p.line(x='date', y='sing', source=source, line_width=2, color='green', alpha=0.8, legend_label='sing')

	p.legend.location = "top_left"
	p.legend.click_policy = "hide"

	#output_file("interactive_legend.html", title="interactive_legend.py example")

	return p



""" ************************************************
	All the functions below are examples from internet. 
********************************************************"""
def getTimeSeries_interactivelegendworks(df_tws):
	p = figure(plot_width=800, plot_height=250, x_axis_type="datetime")
	p.title.text = 'Click on legend entries to hide the corresponding lines'

	#bokeh.sampledata.download()
	for data, name, color in zip([AAPL, IBM, MSFT, GOOG], ["AAPL", "IBM", "MSFT", "GOOG"], Spectral4):
		df = pd.DataFrame(data)
		df['date'] = pd.to_datetime(df['date'])
		p.line(df['date'], df['close'], line_width=2, color=color, alpha=0.8, legend_label=name)
	print(df.head())
	p.legend.location = "top_left"
	p.legend.click_policy = "hide"

	output_file("interactive_legend.html", title="interactive_legend.py example")

	return p

def getTimeSeries_works_3(df_tws):
	output_file("hover_callback.html")

	# define some points and a little graph between them
	x = [2, 3, 5, 6, 8, 7]
	y = [6, 4, 3, 8, 7, 5]
	links = {
		0: [1, 2],
		1: [0, 3, 4],
		2: [0, 5],
		3: [1, 4],
		4: [1, 3],
		5: [2, 3, 4]
	}

	p = figure(plot_width=400, plot_height=400, tools="", toolbar_location=None, title='Hover over points')

	source = ColumnDataSource({'x0': [], 'y0': [], 'x1': [], 'y1': []})
	sr = p.segment(x0='x0', y0='y0', x1='x1', y1='y1', color='olive', alpha=0.6, line_width=3, source=source, )
	cr = p.circle(x, y, color='olive', size=30, alpha=0.4, hover_color='olive', hover_alpha=1.0)

	# Add a hover tool, that sets the link data for a hovered circle
	code = """
	const links = %s
	const data = {'x0': [], 'y0': [], 'x1': [], 'y1': []}
	const indices = cb_data.index.indices
	for (var i = 0; i < indices.length; i++) {
	    const start = indices[i]
	    for (var j = 0; j < links[start].length; j++) {
	        const end = links[start][j]
	        data['x0'].push(circle.data.x[start])
	        data['y0'].push(circle.data.y[start])
	        data['x1'].push(circle.data.x[end])
	        data['y1'].push(circle.data.y[end])
	    }
	}
	segment.data = data
	""" % links

	callback = CustomJS(args={'circle': cr.data_source, 'segment': sr.data_source}, code=code)
	p.add_tools(HoverTool(tooltips=None, callback=callback, renderers=[cr]))

	return p




def getTimeSeries_works2(df_tws):
	def display_event(div, attributes=[], style='float:left;clear:left;font_size=13px'):
		"Build a suitable CustomJS to display the current event in the div model."
		return CustomJS(args=dict(div=div), code="""
	        var attrs = %s; var args = [];
	        for (var i = 0; i<attrs.length; i++) {
	            args.push(attrs[i] + '=' + Number(cb_obj[attrs[i]]).toFixed(2));
	        }
	        var line = "<span style=%r><b>" + cb_obj.event_name + "</b>(" + args.join(", ") + ")</span>\\n";
	        var text = div.text.concat(line);
	        var lines = text.split("\\n")
	        if (lines.length > 35)
	            lines.shift();
	        div.text = lines.join("\\n");
	    """ % (attributes, style))

	x = np.random.random(size=4000) * 100
	y = np.random.random(size=4000) * 100
	radii = np.random.random(size=4000) * 1.5
	colors = ["#%02x%02x%02x" % (int(r), int(g), 150) for r, g in zip(50 + 2 * x, 30 + 2 * y)]

	p = figure(tools="pan,wheel_zoom,zoom_in,zoom_out,reset")
	p.scatter(x, y, radius=np.random.random(size=4000) * 1.5,
			  fill_color=colors, fill_alpha=0.6, line_color=None)

	div = Div(width=400, height=p.plot_height, height_policy="fixed")
	button = Button(label="Button", button_type="success")
	layout = column(button, row(p, div))

	## Events with no attributes
	button.js_on_event(events.ButtonClick, display_event(div))  # Button click
	p.js_on_event(events.LODStart, display_event(div))  # Start of LOD display
	p.js_on_event(events.LODEnd, display_event(div))  # End of LOD display

	## Events with attributes
	point_attributes = ['x', 'y', 'sx', 'sy']  # Point events
	wheel_attributes = point_attributes + ['delta']  # Mouse wheel event
	pan_attributes = point_attributes + ['delta_x', 'delta_y']  # Pan event
	pinch_attributes = point_attributes + ['scale']  # Pinch event

	point_events = [
		events.Tap, events.DoubleTap, events.Press, events.PressUp,
		events.MouseMove, events.MouseEnter, events.MouseLeave,
		events.PanStart, events.PanEnd, events.PinchStart, events.PinchEnd,
	]

	for event in point_events:
		p.js_on_event(event, display_event(div, attributes=point_attributes))

	p.js_on_event(events.MouseWheel, display_event(div, attributes=wheel_attributes))
	p.js_on_event(events.Pan, display_event(div, attributes=pan_attributes))
	p.js_on_event(events.Pinch, display_event(div, attributes=pinch_attributes))

	output_file("js_events.html", title="JS Events Example")


	return layout

def getTimeSeries_works(df_tws):
	output_file("js_on_change.html")

	x = [x * 0.005 for x in range(0, 200)]
	y = x

	source = ColumnDataSource(data=dict(x=x, y=y))

	plot = Figure(plot_width=400, plot_height=400)
	plot.line('x', 'y', source=source, line_width=3, line_alpha=0.6)

	callback = CustomJS(args=dict(source=source), code="""
	    var data = source.data;
	    var f = cb_obj.value
	    var x = data['x']
	    var y = data['y']
	    for (var i = 0; i < x.length; i++) {
	        y[i] = Math.pow(x[i], f)
	    }
	    source.change.emit();
	""")

	slider = Slider(start=0.1, end=4, value=1, step=.1, title="power")
	slider.js_on_change('value', callback)

	layout = column(plot, slider)

	return layout


def getTimeSeries_newish(df_tws):
	df_tws['date'] = pd.to_datetime(df_tws['date'], format='%m/%d/%Y')
	grouped = df_tws.groupby([pd.Grouper(key='date', freq='M'), 'keyword'])['sentiment'].count().to_frame(
		name='count').reset_index()

	print(grouped)
	source = ColumnDataSource(grouped)
	p = figure(plot_height=400, x_axis_type='datetime')
	p.line(x='date', y='count', line_width=2, source=source, legend='Music')
	p.line(x='date', y='count', line_width=2, source=source, legend='Art')
	p.yaxis.axis_label = 'Number of Tweets'

	s = Select(title="test", value="music", options=['art', 'music'])
	w2 = CheckboxGroup(labels=["One", "Two", "Three"], active=[1, 1, 1])

	callback = CustomJS(args=dict(src=source), code='''
	    src.change.emit();
	''')

	js_filter = CustomJSFilter(code='''
	var indices = [];
	for (var i = 0; i < src.get_length(); i++){
	    if (src.data['keyword'][i] == select.value){
	        indices.push(true);
	    } else {
	        indices.push(false);
	    }
	}
	return indices;
	''')
	s.js_on_change('value', callback)

	return p, s, w2


def getTimeSeries_working(df_tws):

	df_tws['date'] = pd.to_datetime(df_tws['date'], format='%m/%d/%Y')
	grouped = df_tws.groupby([pd.Grouper(key='date', freq='M'),'keyword'])['sentiment'].count().to_frame(name = 'count').reset_index()
	# pivot = df_tws.pivot_table(index='date', columns=pd.Grouper(key = 'date', freq='W'), values  = 'sentiment', aggfunc='count')
	# print(pivot.info())
	# grouped = pivot.groupby(pd.Grouper(key='date', freq='D'))['keyword'].count()
	print(grouped)
	source = ColumnDataSource(grouped)
	p = figure(plot_height=400, x_axis_type='datetime')
	p.line(x='date', y='count', line_width=2, source=source, legend='Music')
	p.line(x='date', y='count', line_width=2, source=source, legend='Art')
	p.yaxis.axis_label = 'Number of Tweets'

	color_picker = ColorPicker(color="#ff4466", title="Choose color:", width=200)
	#p.add_layout(color_picker)
	show(color_picker)
	return p


def getTimeSeries_old(df_tws):

	df_tws['date'] = pd.to_datetime(df_tws['date'], format='%m/%d/%Y')
	print(df_tws)
	#grouped = df_tws.groupby('date')['sentiment'].sum()
	grouped = df_tws.groupby(pd.Grouper(key='date', freq='D'))['sentiment', 'sentiment'].count()
	source = ColumnDataSource(grouped)
	p = figure(plot_height=400, x_axis_type='datetime')
	p.line(x='date', y='sentiment', line_width=2, source=source, legend='sentiment')
	p.line(x='date', y='sentiment', line_width=2, source=source, legend='sentiment')
	p.yaxis.axis_label = 'Number of Tweets'



	box_left = pd.to_datetime('25-2-2020')
	box_right = pd.to_datetime('5-3-2020')
	box = BoxAnnotation(left=box_left, right=box_right,
						line_width=1, line_color='black', line_dash='dashed',
						fill_alpha=0.2, fill_color='orange')

	p.add_layout(box)




	return p