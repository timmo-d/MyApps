import pandas as pd
from datetime import datetime
from bokeh.io import output_file, show
from bokeh.plotting import figure, curdoc
from bokeh.models import ColumnDataSource
from bokeh.palettes import Spectral3
from bokeh.models import BoxAnnotation, ColorPicker, CustomJS, CustomJSFilter, CDSView, Select, IndexFilter
from bokeh.models.widgets import Slider,CheckboxGroup,DataTable,MultiSelect,TableColumn,Select
from bokeh.models.layouts import WidgetBox
from bokeh.embed import components
from bokeh.util.browser import view
from bokeh.resources import INLINE
from bokeh.plotting import ColumnDataSource, curdoc
from bokeh.models import CustomJS, ColumnDataSource, Slider
from bokeh.plotting import Figure, output_file, show
from bokeh.layouts import *
from bokeh.models import CustomJS, ColumnDataSource, Slider
from bokeh.plotting import figure, output_file, show
from bokeh.models.sources import ColumnDataSource
from bokeh.models.widgets import Button, DataTable, TableColumn
from bokeh.layouts import layout, widgetbox, column, row
from bokeh.layouts import column
from bokeh.models import ColumnDataSource, CustomJS, Slider
from bokeh.plotting import Figure, output_file, show

def getTimeSeries(df_tws):
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

	layout = column(slider, plot)

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