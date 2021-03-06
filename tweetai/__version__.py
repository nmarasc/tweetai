# -*- coding: utf-8 -*-

def getVersion(version):
    r"""Convert version tuple into PEP 440 compliant string.

    Parameters
    ----------
    version
        Version information

    Returns
    -------
    str
        PEP 440 compliant version string, X.Y.Z[{a|b|rc}N]

        a, b, rc for alpha, beta, release contender

        e.g. 1.2.3rc4

    Raises
    ------
    ValueError
        The fourth value in the version tuple was not a valid string

        Valid strings are 'alpha', 'beta', 'rc', 'final'
    """
    if version[3] not in ('alpha', 'beta', 'rc', 'final'):
        raise ValueError('Invalid fourth value in version tuple')

    # Main version is always of the form X.Y.Z
    main = '.'.join(str(x) for x in version[:3])

    sub = ''
    if version[3] != 'final':
        mapping = {'alpha': 'a', 'beta': 'b', 'rc': 'rc'}
        sub = mapping[version[3]] + str(version[4])

    return main + sub


VERSION = (1, 1, 3, 'final', 0)

__title__ = 'TweetAI'
__description__ = 'AI driven tweets trained on users.'
__url__ = 'https://gitlab.com/nmarasc/tweetai'
__version__ = getVersion(VERSION)
__author__ = 'Nick Marasco'
__author_email__ = 'nicdmarasco@gmail.com'
__license__ = 'MIT License'
__copyright__ = 'Copyright 2022 Nick Marasco'

if __name__ == '__main__':
    print(getVersion(VERSION))
