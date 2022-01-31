# -*- coding: utf-8 -*-
r"""Main module containing the HanAI class.

Classes
-------
HanAI
    Tweet generating bot that learns from an oni pirate
"""
import asyncio
import logging

import tweepy

__all__ = ['HanAI']

logger = logging.getLogger(__name__)


class HanAI:
    r"""Tweet generating bot that learns from an oni pirate.

    Parameters
    ----------
    key
        Twitter bearer key for the API
    user
        Twitter user id to fetch tweets from
    enabled: optional
        True if bot is allowed to post tweets, default is False

    Attributes
    ----------
    key
        Twitter bearer key for the API
    user
        Twitter user id to fetch tweets from
    enabled
        True if bot is allowed to post tweets
    loop
        Event loop for the bot

    Raises
    ------
    ValueError
        No bearer API key or user id was provided on creation
    """
    def __init__(self, key, user, enabled=False):
        if not key:
            logger.critical('No bearer key was provided!')
            raise ValueError('no key provided')
        if not user:
            logger.critical('User id was not provided!')
            raise ValueError('no user id provided')

        self.key = key
        self.enabled = enabled
        self.user = user
        self.loop = asyncio.get_event_loop()
        self.client = tweepy.Client(self.key)

    def run(self):
        response = self.client.get_users_tweets(self.user, exclude=['retweets'])
        print(response.meta)

        tweets = response.data
        for tweet in tweets:
            print(tweet.data)
