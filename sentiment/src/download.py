import os
import pandas as pd
import sentiment.src.GetOldTweets.got3 as got
import datetime

from sqlalchemy import create_engine
from sentiment.src.senti import *

def getQueryDates(keyword):
	"""Determine dates where tweets already exist in database for this keyword"""

	try:
		engine = start_engine()
		query=str("SELECT date FROM updates WHERE keyword='%s' ORDER BY date DESC LIMIT 1;" % keyword)
		rs = pd.read_sql(query, con=engine, parse_dates=['date'])
		since_date = rs['date'].iloc[0]
		until_date = since_date + datetime.timedelta(days=90)
		since_date = datetime.datetime.strftime(since_date,"%Y-%m-%d")
		until_date = datetime.datetime.strftime(until_date,"%Y-%m-%d")
		print('keyword: ' + keyword + ' from: '+ since_date + ' to: ' + until_date)

	except:
		print('An error occurred discovering last update date. Not found?')
		since_date='2020-01-01'
		until_date='2020-01-31'
		pass

	return since_date, until_date


def getDownloads(keyword,max_tweets):
	"""Download tweets according to criteria and upload into database."""
	since_date, until_date = getQueryDates(keyword)
	# print(keyword)
	# print(max_tweets)
	# print(since_date)
	# print(until_date)

	try:
		tweetCriteria = got.manager.TweetCriteria()
		tweetCriteria.username = ''
		tweetCriteria.since = since_date
		tweetCriteria.until = until_date
		tweetCriteria.querySearch = keyword
		tweetCriteria.topTweets = True
		tweetCriteria.maxTweets = max_tweets
		tweetCriteria.near = '"' + 'Perth, WA' + '"'
		tweetCriteria.within = '"' + '50km' + '"'

		print('Searching...\n')

		def receiveBuffer(tweets):
			"""Process downloaded batch of tweets."""
			keyword = tweetCriteria.querySearch
			tweet_list = [[]]

			for t in tweets:
				tweet_list.append(
					[t.id, keyword, t.username, t.date.strftime("%Y-%m-%d %H:%M"), t.retweets, t.favorites,
					 t.text, t.geo, t.mentions, t.hashtags, t.permalink])
				last_date = t.date.strftime("%Y-%m-%d %H:%M")

			df_tweets = pd.DataFrame(tweet_list,
									 columns=['id', 'keyword','username', 'date', 'retweets', 'favorites', 'text', 'geo', 'mentions',
											  'hashtags', 'permalink'])

			df_tweets = df_tweets.iloc[1:] # delete first row as it contains nulls
			df_tweets['date'] = df_tweets['date'].astype('datetime64')

			df_update = pd.DataFrame([[keyword, last_date]],
							   columns=['keyword', 'date'])

			stageTweets(df_tweets, df_update)
			print('Another %d tweets saved to database...' % len(tweets))

		got.manager.TweetManager.getTweets(tweetCriteria, receiveBuffer)
		success=True
	except:
		print('An error occurred')
		success=False
	finally:
		print('Download complete.')
		return success

def stageTweets(df_tweets, df_update):
	"""This function appends downloaded tweets to the staging table."""

	try:
		engine = start_engine()
		df_tweets.to_sql(name='tweetsstaging', con=engine, schema='tweets_db', if_exists='append', index=False)
		df_update.to_sql(name='updates', con=engine, schema='tweets_db', if_exists = 'append', index=False)

	except:
		print('Failed to upload tweets to database.')
	# 	pass
	# finally:
	# 	print('Exit stageTweets')


def addSentiments():
	"""Perform sentiment analysis on each row in database and store result."""
	print('Loading tweets from database...')

	try:
		engine = start_engine()
		sql_df = pd.read_sql('tweetsstaging', con=engine, parse_dates=['date'])

		print('Done. Now updating dataframe...')
		#sql_df = sql_df.head()
		df_tweets = pd.concat([sql_df, pd.DataFrame(columns=['clean_tweet', 'sentiment'])])
		for i, row in df_tweets.iterrows():
			df_tweets.at[i, 'clean_tweet'] = str(clean_tweets(df_tweets['text'][i]))
			df_tweets.at[i, 'sentiment'] = sentiment_analyzer_scores(df_tweets['text'][i])

		print('Done. Now updating staging table...')
		df_tweets.to_sql(name='tweetstemp', con=engine, schema='tweets_db', if_exists='replace', index=False, chunksize = 20000)
		success = True
	except:
		print('Error updating tweets table.')
		success = False
	finally:
		return success

def updateProdTable():
	"""Extract items from staging table and add unique rows to production table"""
	print('Done. Now updating production table.')
	try:
		engine = start_engine()
		with engine.connect() as con:
			rs = con.execute('insert ignore into tweets(select * from tweetstemp);')
		clearStagingTable()
		print('Downloaded tweets added to database successfully.')
	except:
		print('Error uploading tweets to production table.')

def clearStagingTable():
	engine = start_engine()
	with engine.connect() as con:
		rs = con.execute('DELETE FROM tweetsstaging;')
	print('Done. Staging table cleared.')


def start_engine():
	db_user=os.environ.get("db_user")
	db_pw=os.environ.get("db_pw")
	engine = create_engine("mysql+mysqlconnector://{user}:{pw}@127.0.0.1:33066/{db}"
						   .format(user=db_user,
								   pw=db_pw,
								   db="tweets_db",
								   echo=True))
	return engine
if __name__ == "__main__":
	keyword='art'
	max_tweets=0
	num_errors = 0
	#getQueryDates(keyword)
	ok = getDownloads(keyword, max_tweets)
	if ok:
		ok = addSentiments()
	else:
		num_errors=num_errors + 1
		if num_errors<5:
			ok = getDownloads(keyword, max_tweets)
	if ok:
		updateProdTable()






