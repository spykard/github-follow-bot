import random
from github import Github


class Bot():
    """Bot Class"""

    def __init__(self, access_token):
        """
        Class Constructor

        Args:
            access_token: the access token
        """
        self._client = Github(access_token)

    def get_random_users(self, count=1000, min_followers=10, min_follow=10):
        """
        Get Random Users

        Args:
            count: the total numbers of users
            min_followers: the minimum followers
            min_follow: the minimum follow

        Returns:
            a list of users
        """
        projects = [
            "python/cpython",
            "php/php-src",
            "ruby/ruby",
            "golang/go",
            "openjdk/jdk",
            "JetBrains/kotlin",
            "nodejs/node",
            "rust-lang/rust",
            "elixir-lang/elixir",
            "django/django",
            "laravel/laravel",
            "spring-projects/spring-boot",
            "spring-projects/spring-framework",
            "gin-gonic/gin",
            "labstack/echo",
            "rails/rails",
            "nodejs/node",
        ]
        i = 1
        random.shuffle(projects)
        yield self._client.get_user("clivern")
        for project in projects:
            repo = self._client.get_repo(project)
            for username in repo.get_stargazers():
                if self._is_user_followed(username):
                    continue
                if count <= i:
                    break
                i += 1
                yield username

    def follow_username(self, username):
        """
        Follow Username

        Args:
            username: the user to follow

        Returns:
            a boolean whether operation succeeded or not
        """
        self._client.get_user().add_to_following(username)

    def unfollow_username(self, username):
        """
        Un follow Username

        Args:
            username: the user to un follow

        Returns:
            a boolean whether operation succeeded or not
        """
        self._client.get_user().remove_from_following(username)


    def get_followers(self):
        """
        Get Followers

        Returns:
            A list of followers
        """
        return self._client.get_user().get_followers()

    def get_following(self):

        """
        Get Following

        Returns:
            A list of following
        """
        return self._client.get_user().get_following()

    def get_ratelimit(self):
        """
        Get rate limit and other related information for GitHub's API. The limit currently stands at 5000 request per hour.
        
        Returns:
            a value of requests remaining aand a value of request limit        
        """    
        return self._client.rate_limiting  

    def _is_user_followed(self, username):
        """
        Check if username is followed

        Args:
            username: the username

        Returns:
            a boolean whether username followed or not
        """
        return self._client.get_user().has_in_following(username)

    @property
    def client(self):
        return self._client
