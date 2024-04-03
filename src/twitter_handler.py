import tweepy

# Remplacez ces valeurs par vos propres clés obtenues de Twitter
api_key = ""
api_secret_key = ""
access_token = ""
access_token_secret = ""

# Authentification avec l'API de Twitter
auth = tweepy.OAuthHandler(api_key, api_secret_key)
auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth)

# Remplacez 'ID_DU_TWEET' par l'ID réel du tweet que vous souhaitez récupérer
tweet_id = 'ID_DU_TWEET'

# Récupérer le tweet en utilisant son ID
tweet = api.get_status(tweet_id, tweet_mode='extended')  # tweet_mode='extended' pour obtenir tout le texte du tweet

# Afficher le contenu du tweet
print(tweet.full_text)
