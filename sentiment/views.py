from django.shortcuts import render
from bokeh.plotting import figure, output_file, show
from bokeh.resources import CDN
from bokeh.embed import components
import math
from bokeh.models import ColumnDataSource
from bokeh.plotting import figure
from bokeh.sampledata.periodic_table import elements
from bokeh.transform import dodge, factor_cmap

import colorcet as cc
from numpy import linspace
from scipy.stats.kde import gaussian_kde

from bokeh.io import output_file, show
from bokeh.models import ColumnDataSource, FixedTicker, PrintfTickFormatter
from bokeh.plotting import figure
from bokeh.sampledata.perceptions import probly
import sentiment.src.GetOldTweets.got3 as got
import pandas as pd

from bokeh.io import output_file, show
from bokeh.models import ColumnDataSource
from bokeh.palettes import Spectral5
from bokeh.plotting import figure
from bokeh.sampledata.autompg import autompg as df
from bokeh.transform import factor_cmap
from sentiment.src.senti import *

# Create your views here.
def index(request):
    if request.method == "GET":
        return render(request, 'sentiment/index.html')

    elif request.method == "POST":
        #TODO: create Bokeh tabs to display multiple analyses
        #get tweets as per search criteria
        seachquery = request.POST['tw_search']
        tweetCriteria = got.manager.TweetCriteria().setQuerySearch(seachquery).setSince("2020-05-01").setUntil("2020-05-02").setMaxTweets(0)
        #TODO: create user defined dates
        #TODO: user defined field for max tweets to retrieve
        tweets = got.manager.TweetManager.getTweets(tweetCriteria)

        # add tweets to dataframe
        rows = []
        for t in tweets:
            rows.append([t.username, t.date, t.geo, t.retweets, t.text, t.mentions, t.hashtags, sentiment_analyzer_scores(t.text)])
        df_tws = pd.DataFrame(rows, columns=['username', 'date', 'location', 'retweets', 'text', 'mentions','hashtags', 'sentiment'])
        df_tws['text'] = clean_tweets(df_tws['text'])
        print(df_tws)

        # count sentiments from each tweet
        tw_pos = sum(df_tws['sentiment'] == 1)
        tw_neu = sum(df_tws['sentiment'] == 0)
        tw_neg = sum(df_tws['sentiment'] == -1)

        # plot results
        group = ['Negative', 'Neutral', 'Positive']
        counts = [tw_neg, tw_neu, tw_pos]
        p = figure(plot_height=450, x_range=group, title='Sentiment Analysis', toolbar_location=None, tools='')
        p.vbar(x=group, top=counts, width=0.8) #, source=source)
        p.y_range.start = 0
        p.xgrid.grid_line_color = None
        p.xaxis.axis_label = 'Hashtags'
        p.xaxis.major_label_orientation = 1.2
        p.outline_line_color = None


        # return chart results to webpage
        script, div = components(p)
        return render(request, 'sentiment/index.html', {'script' : script , 'div' : div} )
    else:
        pass





def periodicTable(request):
    periods = ["I", "II", "III", "IV", "V", "VI", "VII"]
    groups = [str(x) for x in range(1, 19)]

    df = elements.copy()
    df["atomic mass"] = df["atomic mass"].astype(str)
    df["group"] = df["group"].astype(str)
    df["period"] = [periods[x - 1] for x in df.period]
    df = df[df.group != "-"]
    df = df[df.symbol != "Lr"]
    df = df[df.symbol != "Lu"]

    cmap = {
        "alkali metal": "#a6cee3",
        "alkaline earth metal": "#1f78b4",
        "metal": "#d93b43",
        "halogen": "#999d9a",
        "metalloid": "#e08d49",
        "noble gas": "#eaeaea",
        "nonmetal": "#f1d4Af",
        "transition metal": "#599d7A",
    }

    source = ColumnDataSource(df)

    p = figure(plot_width=900, plot_height=500, title="Periodic Table (omitting LA and AC Series)",
               x_range=groups, y_range=list(reversed(periods)), toolbar_location=None, tools="hover")

    p.rect("group", "period", 0.95, 0.95, source=source, fill_alpha=0.6, legend_field="metal",
           color=factor_cmap('metal', palette=list(cmap.values()), factors=list(cmap.keys())))

    text_props = {"source": source, "text_align": "left", "text_baseline": "middle"}

    x = dodge("group", -0.4, range=p.x_range)

    r = p.text(x=x, y="period", text="symbol", **text_props)
    r.glyph.text_font_style = "bold"

    r = p.text(x=x, y=dodge("period", 0.3, range=p.y_range), text="atomic number", **text_props)
    r.glyph.text_font_size = "11px"

    r = p.text(x=x, y=dodge("period", -0.35, range=p.y_range), text="name", **text_props)
    r.glyph.text_font_size = "7px"

    r = p.text(x=x, y=dodge("period", -0.2, range=p.y_range), text="atomic mass", **text_props)
    r.glyph.text_font_size = "7px"

    p.text(x=["3", "3"], y=["VI", "VII"], text=["LA", "AC"], text_align="center", text_baseline="middle")

    p.hover.tooltips = [
        ("Name", "@name"),
        ("Atomic number", "@{atomic number}"),
        ("Atomic mass", "@{atomic mass}"),
        ("Type", "@metal"),
        ("CPK color", "$color[hex, swatch]:CPK"),
        ("Electronic configuration", "@{electronic configuration}"),
    ]

    p.outline_line_color = None
    p.grid.grid_line_color = None
    p.axis.axis_line_color = None
    p.axis.major_tick_line_color = None
    p.axis.major_label_standoff = 0
    p.legend.orientation = "horizontal"
    p.legend.location = "top_center"




    script, div = components(p)
    return render(request, 'sentiment/index.html', {'script' : script , 'div' : div} )

