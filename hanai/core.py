# -*- coding: utf-8 -*-
r"""Main module containing the HanAI class.

Classes
-------
HanAI
    Tweet generating bot that learns from an oni pirate
"""
import logging
import asyncio
from datetime import datetime, timedelta

import tweepy

from .brain import Brain
from .mouth import Mouth

__all__ = ['HanAI']

logger = logging.getLogger(__name__)


class HanAI:
    r"""Tweet generating bot that learns from an oni pirate.

    Parameters
    ----------
    auth
        dictionary containing all the required auth tokens and secrets, see:auth section
    user
        Twitter username to read tweets from
    enabled: optional
        True if bot is allowed to post tweets, default is False

    Auth
    ----
    bearer_token
        Twitter bearer token for the API
    consumer_key
        App consumer api key
    consumer_secret
        App consumer api secret key
    access_token
        OAuth access token for bot
    access_secret
        OAuth access token secret for bot

    Attributes
    ----------
    username
        Twitter user name to base tweets on
    enabled
        True if bot is allowed to post tweets
    brain
        AI processing and text generating instance
    mouth
        Tweet processing and posting instance

    Raises
    ------
    ValueError
        API tokens or user was not provided on creation
    """
    def __init__(self, *, auth, user, enabled=False):
        if not auth['bearer_token']:
            logger.critical('No bearer token was provided!')
            raise ValueError('no bearer token provided')
        if not auth['consumer_key'] or not auth['consumer_secret']:
            logger.critical('One of consumer key or consumer secret was not provided!')
            raise ValueError('no consumer key or consumer secret provided')
        if not auth['access_token'] or not auth['access_secret']:
            logger.critical('One of access token or access token secret was not provided!')
            raise ValueError('no access token or access token secret provided')
        if not user:
            logger.critical('User was not provided!')
            raise ValueError('no user provided')

        self.enabled = enabled
        self.username = user
        client = tweepy.Client(
            bearer_token=auth['bearer_token'],
            consumer_key=auth['consumer_key'],
            consumer_secret=auth['consumer_secret'],
            access_token=auth['access_token'],
            access_token_secret=auth['access_secret']
        )
        self.brain = Brain(client, self.username)
        self.mouth = Mouth(client)
        self.loop = asyncio.get_event_loop()

    def run(self):
        r"""Begin execution of the bot.

        Starts generating and posting tweets occasionally.
        """
        self._running = True
        self.loop.create_task(self._tweet())
        try:
            logger.info('Executing main event loop')
            self.loop.run_forever()
        except KeyboardInterrupt:
            logger.info('Keyboard interrupt detected')
        finally:
            logger.info('Stopping tasks now')
            self._running = False
            tasks = asyncio.all_tasks(self.loop)
            for task in tasks:
                task.cancel()
            self.loop.run_until_complete(asyncio.gather(*tasks))
            self.loop.stop()
        self.loop.close()

    async def _tweet(self):
        r"""Tweet task method.

        Controls the timed posting of tweets.
        """
        while self._running:
            now = datetime.now()
            next_time = now + (datetime.min - now) % timedelta(hours=2)
            try:
                await asyncio.sleep((next_time - now).seconds)
                tweet = self.brain.getTweet()
                self.mouth.sendTweet(tweet)
                await asyncio.sleep(1)
            except asyncio.CancelledError:
                logger.warning('Task cancelled: _tweet')
