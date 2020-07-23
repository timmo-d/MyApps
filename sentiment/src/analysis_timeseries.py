import pandas as pd
from datetime import datetime

from bokeh.plotting import figure
from bokeh.models import ColumnDataSource
from bokeh.palettes import Spectral3
from bokeh.models import BoxAnnotation

def getTimeSeries(df_tws):

	df_tws['date'] = pd.to_datetime(df_tws['date'], format='%m/%d/%Y')
	print(df_tws)
	#grouped = df_tws.groupby('date')['sentiment'].sum()
	grouped = df_tws.groupby(pd.Grouper(key='date', freq='D'))['sentiment', 'sentiment', 'sentiment'].count()
	source = ColumnDataSource(grouped)
	p = figure(x_axis_type='datetime')
	p.line(x='date', y='sentiment', line_width=2, source=source, legend='Sentiment')
	p.line(x='date', y='sentiment', line_width=2, source=source, legend='Sentiment')
	p.line(x='date', y='sentiment', line_width=2, source=source, legend='Sentiment')
	p.yaxis.axis_label = 'Sentiment Over Time'



	box_left = pd.to_datetime('1-1-2020')
	box_right = pd.to_datetime('13-1-2020')
	box = BoxAnnotation(left=box_left, right=box_right,
						line_width=1, line_color='black', line_dash='dashed',
						fill_alpha=0.2, fill_color='orange')

	p.add_layout(box)




	return p