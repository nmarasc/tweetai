# -*- coding: utf-8 -*-
r"""Module for posting tweets.

Classes
-------
Mouth
    Class for posting and managing tweets
"""
import logging
import re
from unicodedata import normalize

logger = logging.getLogger(__name__)


class Mouth:
    r"""Class controlling the posting and managing of tweets.

    Parameters
    ----------
    client
        Tweepy client instance
    enabled
        True if bot is allowed to send out tweets

    Methods
    -------
    sendTweet
        Send a given text as a tweet
    """
    def __init__(self, client, enabled):
        self.client = client
        self.enabled = enabled

    def sendTweet(self, tweet):
        r"""Send a given text as a tweet.

        Parameters
        ----------
        tweet
            Text to send as a tweet
        """
        tweet = re.sub(r'#', 'hashtag ', tweet)
        logger.info(f'Tweet prepared: {tweet}')
        if self.enabled:
            try:
                self.client.create_tweet(text=normalize("NFC", tweet)[:279])
            except Exception as e:
                logger.error('Failed to post tweet with exception')
                logger.error(e)
        else:
            logger.info('Tweet posting is not enabled. Tweet not sent')
