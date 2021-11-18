# Python Script to Extract tweets of a
# particular Hashtag using Tweepy


# import modules

import tweepy
import json
from PIL import Image
import requests
from io import BytesIO

#credentials for developer.twitter
consumer_key = "XXXXXX"
consumer_secret = "XXXXXX"
access_key = "XXXXX"
access_secret = "XXXX"
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_key, access_secret)
api = tweepy.API(auth)

# function to display data of each tweet
def printtweetdata(n, ith_tweet):
	print()
	print(f"Tweet {n}:")
	print(f"Username:{ith_tweet[0]}")
	print(f"Description:{ith_tweet[1]}")
	print(f"Location:{ith_tweet[2]}")
	#generally contians null so need to check for null conditions 
	#need to send location for a heat map for visualization of count of people talking about a keyword in a particular area
	#can be done via the google maps API, need API key for that
	heatMapLocationData(ith_tweet[2])
	print(f"Following Count:{ith_tweet[3]}")
	print(f"Follower Count:{ith_tweet[4]}")
	if ith_tweet[4] > 100 :
		changeBackgroundImg('aws.amazon.com/legend.jpg',ith_tweet[0])
	print(f"Total Tweets:{ith_tweet[5]}")
	if ith_tweet[5]>10000:
		giveThisUserAMedal(ith_tweet[5],ith_tweet[0])
	print(f"Retweet Count:{ith_tweet[6]}")
	print(f"Tweet Text:{ith_tweet[7]}")
	print(f"Hashtags Used:{ith_tweet[8]}")
	# we can run these through a trained model to predict if a particular hashtag
	# can be trending or not
	print(f"Source used:{ith_tweet[9]}")
	if "iPhone" in ith_tweet[9]:
		SendReplyOfiWatchAd(ith_tweet[8])


#scraping data
def scrape(words, numtweet):
	
	
	# We are using .Cursor() to search through twitter for the required tweets.
	tweets = tweepy.Cursor(api.search_tweets, q=words, lang="en",tweet_mode='extended').items(numtweet)
	
    #getting information for every tweet
	list_tweets = [tweet for tweet in tweets]
	
	# Counter to maintain Tweet Count
	i = 1
	
	# we will iterate over each tweet in the list for extracting information about each tweet
	for tweet in list_tweets:
		username = tweet.user.screen_name
		description = tweet.user.description
		location = tweet.user.location
		following = tweet.user.friends_count
		followers = tweet.user.followers_count
		totaltweets = tweet.user.statuses_count
		retweetcount = tweet.retweet_count
		hashtags = tweet.entities['hashtags']
		source = tweet.source
		
		# Retweets can be distinguished by a retweeted_status attribute,
		# in case it is an invalid reference, except block will be executed
		try:
			text = tweet.retweeted_status.full_text
		except AttributeError:
			text = tweet.full_text
		hashtext = list()
		#count and enumerate hashtags used by a user
		for j in range(0, len(hashtags)):
			hashtext.append(hashtags[j]['text'])
		
		# appending all the extracted information in the DataFrame to be sent for validation and printing
		ith_tweet = [username, description, location, following,
					followers, totaltweets, retweetcount, text, hashtext,source]
		
		
		# printing tweet data on screen
		# calling methods within loops is not object oriented, I'd use a list and send it out and loop there or
		#put the printing code here , since we have to do validations and may be call APIs, refactoring is required
		# to make calls to different async services I'd gather differnt lists and send it over so that we dont have to
		# wait for everyiteration of the entire object of the tweet
		printtweetdata(i, ith_tweet)
		i = i+1
	
	
	
	return list_tweets

#to show heat map on google for a particular location
def heatmapLocationData(location):
    query = getLatLng(location);
    #adding location to existing data to update the heat map
    response = requests.get('http://api.open-notify.org/iss-pass.json', params=query)
    
    print(response.json())

#get latitude and longitude values from the location text, like for Hyderabad 17.38,78.48
def getLatLng(location):
    resp = requests.get('http://googlemapsapi.com',params=location)
    return resp

#change background image for the user's page with consent
def changeBackgroundImg(url,user_name):
    response = requests.get(url)
    img = Image.open(BytesIO(response.content))
    #prompt user to change background image with a preview
    #logic to add img for the user_name

#congratulate user on a milestone tweet
def giveThisUserAMedal(noOfTweets,user_name):
    #check the last digit of number of tweets to write 1st, 2nd, 3rd or th for rest of the digits
    if noOfTweets%10 == 1:
        print(f"Congratulations on the {noOfTweets}st Tweet")
    elif noOfTweets%10 == 2:
        print(f"Congratulations on the {noOfTweets}nd Tweet")
    elif noOfTweets%10 == 3:
        print(f"Congratulations on the {noOfTweets}rd Tweet")
    else:
        print(f"Congratulations on the {noOfTweets}th Tweet")

#reply ad to iphone users sending them links to popular e-commerce sites
def SendReplyOfiWatchAd(tweet_text):
    #check if replies are on 
    print(f"Reply with iWatch ad as reply to the existing {tweet_text}")
    #otherwise create a follow request by the e-commerce twitter handle e.g. @Amazon


def lambda_handler(event, context):
    # TODO implement
    result = scrape(str(event['queryString']), 10) 
    return {
        'statusCode': 200,
        'body': json.loads(json.dumps(result, default=str))
    }

