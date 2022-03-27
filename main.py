import argparse
import logging
import sys
import time
import configparser

from bot import Bot


_logger = logging.getLogger(__name__)


def follow(access_token, followers_count, interval):
    bot = Bot(access_token)

    for username in bot.get_random_users(followers_count):
        _logger.info("follow {}".format(username))
        bot.follow_username(username)
        time.sleep(interval)


def clean(access_token, interval):
    bot = Bot(access_token)

    followrs = [bot.client.get_user("clivern")]

    for username in bot.get_followers():
        followrs.append(username)

    following = bot.get_following()

    for username in bot.get_following():
        if username not in followrs:
            _logger.info("unfollow {}".format(username))
            bot.unfollow_username(username)
        else:
            _logger.info("{} is one of your followers".format(username))
        time.sleep(interval)


def get_ratelimit(access_token):
    """Get rate limit and other related information for GitHub's API. The limit currently stands at 5000 request per hour.
    """    
    bot = Bot(access_token)

    return(bot.get_ratelimit())


def parse_config():
    """Parse configuration file for parameters
    """
    config = configparser.ConfigParser()
    config.read('config/config.ini')

    return(config['Settings'])


def setup_logging(loglevel):
    """Setup basic logging

    Args:
      loglevel (int): minimum loglevel for emitting messages
    """
    logformat = "[%(asctime)s] %(levelname)s:%(name)s:%(message)s"
    logging.basicConfig(
        level=loglevel, stream=sys.stdout, format=logformat, datefmt="%Y-%m-%d %H:%M:%S"
    )


def main():
    config = parse_config()
    setup_logging(config['verbosity'])

    _logger.info("Bot started")
    ratelimit = get_ratelimit(config['access_token'])
    _logger.info("Remaining API calls " + str(ratelimit[0]) + " out of " + str(ratelimit[1]))

    if config['operation'] == "follow":
        while True:
            try:
                follow(config['access_token'], int(config['followers_count']), int(config['interval']))
                break
            except Exception:
                _logger.info("Rate limit reached, hold on for a while")
                time.sleep(int(config['interval']) + 60)

    elif config['operation'] == "clean":
        while True:
            try:
                clean(config['access_token'], int(config['interval']))
                break
            except Exception:
                _logger.info("Rate limit reached, hold on for a while")
                time.sleep(int(config['interval']) + 60)

    _logger.info("Bot finished")


if __name__ == "__main__":
    main()