# -*- coding: utf-8 -*-
r"""Module for the AI processing class.

Classes
-------
Brain
    Class for AI processing and generating text
"""
import os
import logging
import csv
import re
from time import sleep

import gpt_2_simple as gpt2

logger = logging.getLogger(__name__)


class Brain:
    r"""AI processing and text generation class.

    Parameters
    ----------
    client
        Tweepy client instance
    username
        Twitter username of whom to base tweets on

    Attributes
    ----------
    client
        Tweepy client instance
    username
        Twitter username of whom to base tweets on
    userid
        Twitter user id of the username provided
    session
        Gpt2 artificial intelligence session
    run_name
        Name of AI model training run
    tweets
        List of tweets ready to be used
    newest_tweet
        Tweet id of the most recent tweet fetched for data

    Methods
    -------
    getTweet
        Retrieves a single tweet, ready to post
    """
    def __init__(self, client, username):
        self.client = client
        self.username = username
        self.userid = self.client.get_user(username=username).data['id']
        self.tweets = []
        self._initializeModel()
        self._generateTweetSet()

    def getTweet(self):
        r"""Get a tweet.

        Returns
        -------
        str
            Text ready to be sent as a tweet
        """
        if len(self.tweets) == 0:
            self._generateTweetSet()
        return self.tweets.pop(0)

    def _generateTweet(self):
        r"""Generate a single tweet.

        Returns
        -------
        str
            Text of a tweet
        """
        tweet = re.sub(r'<\|startoftext\|>', '', self._generateN(1)[0])
        while not self._uniqueTweet(tweet):
            tweet = re.sub(r'<\|startoftext\|>', '', self._generateN(1)[0])
        return tweet

    def _generateTweetSet(self):
        r"""Generate a set of about 10 tweets.

        Attempts to generate a list of 10 tweets. If any of the generated tweets are
        exactly the same text as a tweet from the data, it is not included. So the
        list length may be less than 10.

        Returns
        -------
        list
            List of generated tweets

        Warning
        -------
        List size is not guaranteed to be exactly 10 due to not including certain generated text
        """
        self.tweets = []
        tweet_list = self._generateN(10)
        for tweet in tweet_list:
            tweet = re.sub(r'<\|startoftext\|>', '', tweet)
            if self._uniqueTweet(tweet):
                self.tweets.append(tweet)
        gpt2.reset_session(self.session)
        self.session = None

    def _initializeModel(self):
        r"""Check if a new AI model needs to be trained."""
        self.session = None

        model_name = '355M'
        if not os.path.isdir(os.path.join('models', model_name)):
            logger.info(f'Downloading {model_name} model...')
            gpt2.download_gpt2(model_name=model_name)

        self.run_name = 'run1'
        if not os.path.isdir(os.path.join('checkpoint', self.run_name)):
            logger.info('Need to train a new model. This could take a while...')
            if not os.path.isfile(f'{self.username}.csv'):
                logger.info('Fetching new twitter data...')
                self._getNewTwitterData()
                logger.info('Finished gathering twitter data')

            logger.info('Starting model training. Please be patient...')
            self.session = gpt2.start_tf_sess()
            gpt2.finetune(self.session, dataset=f'{self.username}.csv',
                          steps=100, model_name=model_name,
                          restore_from='fresh', run_name=self.run_name,
                          save_every=50, print_every=10)
            logger.info('Model training complete')
        logger.info('Brain initialized')

    def _generateN(self, num):
        r"""Generate a number of tweets based on the supplied parameter.

        Parameters
        ----------
        num
            Number of tweets to generate

        Returns
        -------
        list
            List containing the generated text
        """
        if self.session is None:
            logger.info('Loading model...')
            self.session = gpt2.start_tf_sess()
            gpt2.load_gpt2(self.session, run_name=self.run_name)
        logger.info(f'Generating {num} tweet(s)...')
        return gpt2.generate(
            self.session,
            length=200, temperature=1.0, top_p=0.9,
            prefix='<|startoftext|>', truncate='<|endoftext|>',
            nsamples=num, return_as_list=True
        )

    def _uniqueTweet(self, tweet):
        r"""Check if the generated text is in the training data.

        Parameters
        ----------
        tweet
            Text to check against the training data

        Returns
        -------
        bool
            False if the text is in the training data, True otherwise
        """
        with open(f'{self.username}.csv') as db:
            for line in db.readlines():
                if tweet in line:
                    return False
        return True

    def _getNewTwitterData(self):
        r"""Set up csv writer to get tweet data."""
        with open(f'{self.username}.csv', 'w', encoding='utf8') as f:
            writer = csv.writer(f)
            writer.writerow(['Tweets'])
            self._downloadTweets(writer)

    def _downloadTweets(self, writer):
        r"""Download and write tweet data to a file.

        Parameters
        ----------
        writer
            csv writer used to add the data to the file
        """
        logger.info(f'Getting tweet data for user @{self.username}')

        response = self.client.get_users_tweets(
            self.userid, max_results=100,
            exclude=['retweets'],
            start_time='2010-05-01T00:00:00Z',
        )
        for tweet in response.data:
            text = self._cleanText(tweet['text'])
            if text != '':
                writer.writerow([text])

        self.newest_tweet = response.meta['newest_id']

        while response.meta['result_count'] >= 100:
            sleep(2)
            response = self.client.get_users_tweets(
                self.userid, max_results=100,
                exclude=['retweets'],
                start_time='2010-05-01T00:00:00Z',
                pagination_token=response.meta['next_token']
            )
            for tweet in response.data:
                text = self._cleanText(tweet['text'])
                if text != '':
                    writer.writerow([text])

    def _cleanText(self, text):
        r"""Remove unwanted text from downloaded data.

        Text such as user mentions and links are removed from the text.

        Parameters
        ----------
        text
            Text to remove from

        Returns
        -------
        str
            Cleaned text
        """
        while re.search(r'^@/?[a-zA-Z0-9_]+', text):
            text = re.sub(r'^@/?[a-zA-Z0-9_]+', '', text).strip()

        regex = r'http\S+|pic\.\S+|\xa0|…|@/?[a-zA-Z0-9_]+|#\S+'
        text = re.sub(regex, '', text).strip()

        return text
