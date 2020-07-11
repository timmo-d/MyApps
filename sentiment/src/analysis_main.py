import sentiment.src.GetOldTweets.got3 as got

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
	df_tws['text'] = clean_tweets(df_tws['text'])

	return df_tws