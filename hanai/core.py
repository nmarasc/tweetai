# -*- coding: utf-8 -*-
r"""Main module containing the HanAI class.

Classes
-------
HanAI
    Tweet generating bot that learns from an oni pirate
"""
import logging

import tweepy

__all__ = ['HanAI']

logger = logging.getLogger(__name__)


class HanAI:
    r"""Tweet generating bot that learns from an oni pirate.

    Parameters
    ----------
    token
        Twitter bearer token for the API
    access_token
        OAuth access token for bot
    access_token_secret
        OAuth access token secret for bot
    user
        Twitter username to read tweets from
    enabled: optional
        True if bot is allowed to post tweets, default is False

    Attributes
    ----------
    user
        Twitter user id to read tweets from
    enabled
        True if bot is allowed to post tweets
    client
        Tweepy client instance

    Raises
    ------
    ValueError
        API tokens or user was not provided on creation
    """
    def __init__(self, token, access_token, access_token_secret, user, enabled=False):
        if not token:
            logger.critical('No bearer token was provided!')
            raise ValueError('no bearer token provided')
        if not access_token or not access_token_secret:
            logger.critical('One of access token or access token secret was not provided!')
            raise ValueError('no access token or access token secret provided')
        if not user:
            logger.critical('User was not provided!')
            raise ValueError('no user provided')

        self.enabled = enabled
        self.client = tweepy.Client(
            bearer_token=token,
            access_token=access_token,
            access_token_secret=access_token_secret
        )
        self.user = self.client.get_user(username=user).data['id']

    def run(self):
        response = self.client.get_users_tweets(self.user, max_results=50, exclude=['retweets', 'replies'])
        print(response.meta)
        print(response.meta['newest_id'])

        tweets = response.data
        for tweet in tweets:
            print(tweet.data)
