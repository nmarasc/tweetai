#!/usr/bin/env python3.10
# -*- coding: utf-8 -*-
r"""Main driver script for HanAI."""
import os
import logging
import logging.config
import argparse
import json

from hanai import HanAI

LOGDIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), '.log')


def main(config):
    args = parseCL()
    if args.debug:
        config['root']['level'] = 'DEBUG'
    if args.verbose:
        config['root']['handlers'].append('console')
    if args.temporary in ['all', 'log']:
        config['root']['handlers'].remove('default')

    os.makedirs(LOGDIR, exist_ok=True)
    logging.config.dictConfig(config)
    logger = logging.getLogger(__name__)
    logger.info('Logging configured and initialized')

    with open('.auth/oauth.json') as auth:
        data = json.load(auth)

    hanAI = HanAI(
        os.getenv('BEARER_TOKEN'),
        data['oauth_token'],
        data['oauth_token_secret'],
        os.getenv('TWTUSER'),
        args.enable
    )
    hanAI.run()


def parseCL():
    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=(
            'options:\n'
            '   log\tlogging messages are temporary\n'
            '   all\tAll above options are temporary, default'
        )
    )

    parser.add_argument(
        '-d', '--debug', action='store_true',
        help='\tadd debug messages to the log')
    parser.add_argument(
        '-v', '--verbose', action='store_true',
        help='\tprint log messages to the console')
    parser.add_argument(
        '-t', '--temporary', action='store', const='all',
        nargs='?', metavar='option',
        help='\tdo not write values to disk')
    parser.add_argument(
        '-e', '--enable', action='store_true',
        help='\tallow the bot to start tweeting')

    args = parser.parse_args()
    if args.temporary not in [None, 'all', 'log']:
        raise ValueError(f'option not recognized: {args.temporary}')
    return args


if __name__ == '__main__':

    config = {
        'version': 1,
        'disable_existing_loggers': False,
        'formatters': {
            'standard': {
                'format': '%(asctime)s [%(levelname)-8s] %(name)s: %(message)s'
            }
        },
        'handlers': {
            'default': {
                'level': 'DEBUG',
                'formatter': 'standard',
                'class': 'logging.handlers.RotatingFileHandler',
                'filename': f'{LOGDIR}/output.log',
                'mode': 'a',
                'maxBytes': 10485760,
                'backupCount': 5
            },
            'console': {
                'level': 'DEBUG',
                'formatter': 'standard',
                'class': 'logging.StreamHandler'
            }
        },
        'root': {
            'handlers': ['default'],
            'level': 'INFO'
        }
    }

    main(config)
