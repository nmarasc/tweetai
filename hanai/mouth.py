# -*- coding: utf-8 -*-
r"""Module for posting tweets.

Classes
-------
Mouth
    Class for posting and managing tweets
"""
import logging
import re

logger = logging.getLogger(__name__)


class Mouth:
    r"""Class controlling the posting and managing of tweets.

    Parameters
    ----------
    client
        Tweepy client instance

    Methods
    -------
    sendTweet
        Send a given text as a tweet
    """
    def __init__(self, client):
        self.client = client

    def sendTweet(self, tweet):
        r"""Send a given text as a tweet.

        Parameters
        ----------
        tweet
            Text to send as a tweet
        """
        logger.info(f'Sending tweet: {tweet}')
        tweet = re.sub(r'#', 'hashtag ', tweet)
        self.client.create_tweet(text=tweet)
