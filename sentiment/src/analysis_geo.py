from bokeh.plotting import figure

def getLocations(df_tws):
	# count sentiments from each tweet
	tw_pos = sum(df_tws['sentiment'] == 1)
	tw_neu = sum(df_tws['sentiment'] == 0)
	tw_neg = sum(df_tws['sentiment'] == -1)

	# plot results
	group = ['Negative', 'Neutral', 'Positive']
	counts = [tw_neg, tw_neu, tw_pos]
	p = figure(plot_height=400, x_range=group, title='Sentiment Analysis', toolbar_location=None, tools='')
	p.vbar(x=group, top=counts, width=0.8)  # , source=source)
	p.y_range.start = 0
	p.xgrid.grid_line_color = None
	p.xaxis.axis_label = 'Hashtags'
	p.xaxis.major_label_orientation = 1.2
	p.outline_line_color = None
	return p