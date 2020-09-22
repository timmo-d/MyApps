import pandas as pd

from bokeh.models import ColumnDataSource, TableColumn, DataTable, HTMLTemplateFormatter


def getSummary(df_tws):
	# ANOVA in Python: https://www.pythonfordatascience.org/anova-python/

	results_data=pd.DataFrame(df_tws.describe())
	df_results = results_data.reset_index()

	source = ColumnDataSource(df_results)
	template = """
	<div style="background:<%= 
	    (function colorfromint(){
	        if(value == 1){
	            return("blue")}
	        else{return("red")}
	        }()) %>; 
	    color: white"> 
	<%= value %></div>
	"""

	formater = HTMLTemplateFormatter(template=template)
	columns = [TableColumn(field='index', title='Statistic'),
			   TableColumn(field='retweets', title='Retweets'),
			   TableColumn(field='favorites', title='Favourites'),
			   TableColumn(field='sentiment', title='Sentiment',formatter=formater)]

	data_table = DataTable(source=source, columns=columns, width=350, height=280, editable=False, index_position=None)

	return data_table