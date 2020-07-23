from django.shortcuts import render
from bokeh.embed import components

# Each tab is drawn by one script
from .src.analysis_main import getData, getLocalData
from .src.analysis_sentiment import getSentiment
from .src.analysis_table import getSummary
from .src.analysis_geo import getLocations
from .src.analysis_timeseries import getTimeSeries


# Create your views here.
def index(request):
	if request.method == "GET":
		return render(request, 'sentiment/index.html')

	elif request.method == "POST":
		#get tweets as per search criteria
		seachquery = request.POST['tw_search']
		from_date = request.POST['start_date']
		to_date = request.POST['end_date']
		max_tweets = request.POST['max_tweets']
		# from_date = '2020-05-01'
		# to_date = '2020-05-02'
		# max_tweets = 0
		df_tws = getLocalData(seachquery, from_date, to_date, int(max_tweets))
		print(df_tws)

		# get results from each analysis
		summary = getSummary(df_tws)
		sentiment = getSentiment(df_tws)
		geo = getLocations(df_tws)
		timeseries = getTimeSeries(df_tws)

		# return analysis results to webpage
		script, div = components(summary)
		script2, div2 = components(sentiment)
		script3, div3 = components(geo)
		script4, div4 = components(timeseries)

		return render(request, 'sentiment/index.html', {'script' : script , 'div' : div,
														'div2' : div2, 'script2' : script2,
														'div3' : div3, 'script3' : script3,
														'div4' : div4, 'script4' : script4} )


	else:
		pass





