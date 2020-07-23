import os
import pandas as pd
import sentiment.src.GetOldTweets.got3 as got
import datetime

from sqlalchemy import create_engine
from sentiment.src.senti import *

def getQueryDates():
	"""Determine dates where tweets already exist in database for this keyword"""
	since_date='2020-02-01'
	until_date='2020-03-01'
	# engine = start_engine()
	# with engine.connect() as con:
	# 	since_date = con.execute("SELECT date FROM updates WHERE keyword='music' ORDER BY date DESC LIMIT 1;")
	# print(since_date)
	# since_date = since_date.date.strftime("%Y-%m-%d %H:%M")
	# until_date = since_date + datetime.timedelta(days=10)

	return since_date, until_date


def getDownloads():
	"""Download tweets according to criteria and upload into database."""
	since_date, until_date = getQueryDates()

	try:
		tweetCriteria = got.manager.TweetCriteria()
		tweetCriteria.username = ''
		tweetCriteria.since = since_date
		tweetCriteria.until = until_date
		tweetCriteria.querySearch = 'music'
		tweetCriteria.topTweets = True
		tweetCriteria.maxTweets = 20
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

	except:
		print('An error occurred')
	finally:
		print('Download complete.')

def stageTweets(df_tweets, df_update):
	"""This function appends downloaded tweets to the staging table."""

	try:
		engine = start_engine()
		# engine = create_engine("mysql+mysqlconnector://{user}:{pw}@127.0.0.1:33066/{db}"
		# 				   .format(user="root",
		# 						   pw="Xanglesprat",
		# 						   db="tweets_db",
		# 						   echo=True))

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
		# engine = create_engine("mysql+mysqlconnector://{user}:{pw}@127.0.0.1:33066/{db}"
		# 					   .format(user="root",
		# 							   pw="Xanglesprat",
		# 							   db="tweets_db",
		# 							   echo=True))

		sql_df = pd.read_sql('tweetsstaging', con=engine, parse_dates=['date'])

		print('Done. Now updating dataframe...')
		#sql_df = sql_df.head()
		df_tweets = pd.concat([sql_df, pd.DataFrame(columns=['clean_tweet', 'sentiment'])])
		for i, row in df_tweets.iterrows():
			df_tweets.at[i, 'clean_tweet'] = str(clean_tweets(df_tweets['text'][i]))
			df_tweets.at[i, 'sentiment'] = sentiment_analyzer_scores(df_tweets['text'][i])

		print('Done. Now updating staging table...')
		#engine = start_engine() # start engine again incase of database timeout from big dataframe processing above
		df_tweets.to_sql(name='tweetstemp', con=engine, schema='tweets_db', if_exists='replace', index=False, chunksize = 20000)

	except:
		print('Error updating tweets table.')

def updateProdTable():
	"""Extract items from staging table and add unique rows to production table"""
	print('Done. Now updating production table.')
	try:
		engine = start_engine()
		# engine = create_engine("mysql+mysqlconnector://{user}:{pw}@127.0.0.1:33066/{db}"
		# 					   .format(user="root",
		# 							   pw="Xanglesprat",
		# 							   db="tweets_db",
		# 							   echo=True))

		with engine.connect() as con:
			rs = con.execute('insert ignore into tweets(select * from tweetstemp);')

		print('Downloaded tweets added to database successfully.')
	except:
		print('Error uploading tweets to production table.')

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

	getDownloads()
	addSentiments()
	updateProdTable()


