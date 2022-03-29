import logging
import sys
import time
import csv
import configparser
from datetime import datetime

from bot import Bot


_logger = logging.getLogger(__name__)


def follow(access_token, followers_count, projects, interval, blacklist, active_since):
    bot = Bot(access_token)

    following = []
    for username in bot.get_following():
        following.append(username)

    if blacklist:
        blacklist_set = get_blacklist(blacklist)
    else:
        blacklist_set = {}

    for username in bot.get_random_users(followers_count, projects.split(), 5, 5, blacklist_set, active_since):
        if username not in following:       
            _logger.info("follow {}".format(username))
            if blacklist:
                log_follows(blacklist, username.login, datetime.utcnow())
            bot.follow_username(username)
        else:
            _logger.info("{} is already followed by the user".format(username))            
        time.sleep(interval)


def clean(access_token, whitelist, interval):
    bot = Bot(access_token)

    whitelist_arr = [bot.client.get_user(x) for x in whitelist.split()] # Could use less API Calls if implemented in the same way as the Blacklist

    followrs = whitelist_arr
    for username in bot.get_followers():
        followrs.append(username)

    for username in bot.get_following():
        if username not in followrs:
            _logger.info("unfollow {}".format(username))
            bot.unfollow_username(username)
        else:
            _logger.info("{} is one of your followers or is whitelisted".format(username))
        time.sleep(interval)


def get_ratelimit(access_token):
    """Get rate limit and other related information for GitHub's API. The limit currently stands at 5000 request per hour.
    """    
    bot = Bot(access_token)

    return(bot.get_ratelimit())


def get_blacklist(blacklist):
    """Get a list of usernames from a file to be used as a Blacklist to avoid re-following the same accounts in the future.
    """    
    rows = []
    with open(blacklist, 'r', encoding='UTF8') as f:
        reader = csv.reader(f)
        next(reader)
        for row in reader:
            rows.append(row[0])

    return(set(rows))


def log_follows(blacklist, username, followed_at):
    """Write usernames that were followed to a file.
    """    
    with open(blacklist, 'a', encoding='UTF8', newline='') as f:
        writer = csv.writer(f)
        writer.writerow([username, followed_at])


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
    _logger.info("Remaining API calls {} out of {}".format(str(ratelimit[0]), str(ratelimit[1])))

    if config['operation'] == "follow":
        while True:          
            try:
                follow(config['access_token'], int(config['followers_count']), config['projects'], int(config['interval']), config['blacklist'], int(config['active_since']))
                break
            except Exception as e:
                _logger.info(e)
                _logger.info("Rate limit reached, hold on for a while")
                time.sleep(int(config['interval']) + 60)

    elif config['operation'] == "clean":
        while True:
            try:
                clean(config['access_token'], config['whitelist'], int(config['interval']))
                break
            except Exception:
                _logger.info("Rate limit reached, hold on for a while")
                time.sleep(int(config['interval']) + 60)

    _logger.info("Bot finished")


if __name__ == "__main__":
    main()
