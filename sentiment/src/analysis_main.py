import sentiment.src.GetOldTweets.got3 as got
from sqlalchemy import create_engine
import pandas as pd
from sentiment.src.senti import clean_tweets, sentiment_analyzer_scores

def getData(seachquery, from_date, to_date, max_tweets=10):
	tweetCriteria = got.manager.TweetCriteria().setQuerySearch(seachquery).setSince(from_date).setUntil(
		to_date).setMaxTweets(max_tweets)
	# TODO: create user defined dates
	# TODO: user defined field for max tweets to retrieve
	tweets = got.manager.TweetManager.getTweets(tweetCriteria)

	# add tweets to dataframe
	rows = []
	for t in tweets:
		rows.append(
			[t.username, t.date, t.geo, t.retweets, t.text, t.mentions, t.hashtags, sentiment_analyzer_scores(t.text)])
	df_tws = pd.DataFrame(rows, columns=['username', 'date', 'location', 'retweets', 'text', 'mentions', 'hashtags',
										 'sentiment'])

	return df_tws

def getLocalData(seachquery, from_date, to_date, max_tweets=10):
	query = "SELECT * FROM tweets WHERE keyword='music'"
	engine = create_engine("mysql+mysqlconnector://{user}:{pw}@127.0.0.1:33066/{db}"
						   .format(user="root",
								   pw="Xanglesprat",
								   db="tweets_db",
								   echo=True))

	df_tws = pd.read_sql_query(query, engine)
	return df_tws