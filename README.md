# GitHub-Follow-Bot

🤖 GitHub Follow Bot to Get More Followers via Follow 4 Follow.

## Running the Tool

1. Install the required Python packages/dependencies (requirements.txt).
2. Set the appropriate configuration parameters, in the file `/config/config.ini`, using the following format:

``` ini
[Settings]
[DEFAULT]
access_token =
operation = follow
followers_count = 1000
interval = 2
verbosity = DEBUG
projects = python/cpython php/php-src ruby/ruby golang/go openjdk/jdk JetBrains/kotlin nodejs/node rust-lang/rust elixir-lang/elixir django/django laravel/laravel spring-projects/spring-boot spring-projects/spring-framework gin-gonic/gin labstack/echo rails/rails nodejs/node
blacklist =
whitelist = 

[Settings]
access_token =
operation = follow
followers_count = 100
interval = 4
verbosity = INFO
projects = python/cpython php/php-src ruby/ruby golang/go openjdk/jdk JetBrains/kotlin nodejs/node rust-lang/rust elixir-lang/elixir django/django laravel/laravel spring-projects/spring-boot spring-projects/spring-framework gin-gonic/gin labstack/echo rails/rails nodejs/node
blacklist = data/follow_log.csv
whitelist = jacquev6 sfdye
```

`access_token` : A GitHub access token, created at https://github.com/settings/tokens/new with required user permissions (read:user, user:email, user:follow).

`operation` : Choose the mode to execute, either `follow` or `clean`.

`followers_count` : Choose the number of users to follow.

`interval` : The bot interval in seconds.

`verbosity` : Set loglevel verbosity, possible values are `NOTSET`, `DEBUG`, `INFO`, `WARNING`, `ERROR` and `CRITICAL`.

`projects` : A set of github repositories which the bot will utilize in order to fetch usernames to be followed.

`blacklist` : If set, defines a filename to be used in order to save usernames as a Blacklist to avoid re-following the same accounts in the future. A simple .CSV file with the following header is required `username,followed_at`.

`whitelist` : A set of GitHub usernames seperated by space, which will not be unfollowed during the `clean` operation.

3. Run the Python script:

``` bash
python main.py
```

## Credits

- [Spyridon Kardakis](https://www.linkedin.com/in/kardakis/)
- [Opengribs](https://opengribs.org/)