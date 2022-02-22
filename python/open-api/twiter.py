import tweepy

twitter_api_key = 'Et1m2IrzSLiBcZUdspCUvjCpa'
twitter_api_secret_key = 'EHSQ5ERixCcH8hW8ZLdAjaCQ0GnDfBASYwXkLq9hvn6Rleu3hP'
twitter_access_token = '1495916003775053832-b5saTpVnAzdwyAZ2SQQMJjkA54HMv8'
twitter_access_token_secret = 'ASTpViMV8GzCrlaYYtrkoktc85x6stUoVl5zcdA4OCs9B'

class SimpleStreamListener(tweepy.StreamListener):
    def on_status(self, status):
        print(status)

stream_listener = SimpleStreamListener()

auth = tweepy.OAuthHandler(twitter_api_key, twitter_api_secret_key)
auth.set_access_token(twitter_access_token, twitter_access_token_secret)

twitterStream = tweepy.Stream(auth, stream_listener)
twitterStream.filter(track=['nft'])