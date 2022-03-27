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
whitelist = 

[Settings]
access_token =
operation = follow
followers_count = 100
interval = 4
verbosity = INFO
whitelist = jacquev6 sfdye
```

`access_token` : A GitHub access token, created at https://github.com/settings/tokens/new with required user permissions (read:user, user:email, user:follow).

`operation` : Choose the mode to execute, either `follow` or `clean`.

`followers_count` : Choose the number of users to follow.

`interval` : The bot interval in seconds.

`verbose` : Set loglevel verbosity, possible values are `NOTSET`, `DEBUG`, `INFO`, `WARNING`, `ERROR` and `CRITICAL`.

`whitelist` : A set of GitHub usernames seperated by space, which will not be unfollowed during the `clean` operation.

3. Run the Python script:

``` bash
python main.py
```