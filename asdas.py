"""
Program name: Keep Yourself Safe

Abbreviation: kys

Program Description: Motivate depressed individuals on the social media platform called X by using ChatGPT to create AI
generated motivational quotes based on a topic chosen by the account admin every day.

Version: 10.5

Changelog:
v6.0 - Added a changes section + reformatted document to improve readability.
v7.0 - Switched the changes section for a change log + in order to improve the concept of reflection in our code and to
increase efficiency when changing older program parts + coded the user_choose_topic function + allowed user to choose
whether their quote topic would be random or chosen by them.
v8.0 - Function 3 worked on, will finish.
v9.0 - Quotes can generate. Twitter don't work.
v10.0 - Minor fixes in Function 2(quote generation) in the circumstance of function 1 user chooses the random option. (Selection added)
+ fixed calls to each method at the bottom of the code.
"""

# Import required libraries for use with Twitter/X API and OpenAI API
import tweepy
import openai
from openai import OpenAI

# Set up the keys:

# Twitter API keys set up using dictionary data structure
twitterAPI = {"client_ID": 'SmUtVjB2YnRMWmJqOEJrQmlTNTg6MTpjaQ', "client_secret": 'qlRumOCDKIUIUP4wCUiVVvIM_zMybfEPYPMi8-57nLz1qAGZKl',
              "access_token": '751828828905877504-0WVKpLgBmYZyVKtnVh4b5dv84Rs32KE',
              "access_token_secret": 'tCzzkvoV2h15quDzGsI5JyPZcmTm7P9USO8IAdPIsXjgG', "bearer_token": "AAAAAAAAAAAAAAAAAAAAAGoPtgEAAAAAlpd6YzcY37Q4MwBCSxhJOFXoyIw%3D7BaDQ55YSxdd4haKUmfBImqePM28VMbjEtgeziaCmNlI3nv73N",
              "api_key": "2pBmwUULykvoV9tDqwzz6vsqw", "api_key_secret": "EIROsWN0AkdXZCIl81z3Ax0lEYQNtnGfAIAOQemal4F3NEqMTj"}


# Set up Tweepy with our Twitter API keys

# auth = requests_oauthlib.OAuth1(client_key=twitterAPI["client_ID"], client_secret=twitterAPI["client_secret"], resource_owner_key=twitterAPI["access_token"], resource_owner_secret=twitterAPI["access_token_secret"])

# Don't use oauth bearer token - needs to be either OAuth1.0a User Handler or OAuth2 User Handler
# auth = tweepy.OAuth2BearerHandler(twitterAPI["bearer_token"])

# This can be used but twitter client will already set up OAuth 1.0a User Context during setup
# auth = tweepy.OAuth1UserHandler(consumer_key=twitterAPI["client_ID"], consumer_secret=twitterAPI["client_secret"], access_token=twitterAPI["access_token"], access_token_secret=twitterAPI["access_token_secret"])

# Twitter client should automatically setup OAuth 1.0a User Context with this as stated by documentation.
twitter_client = tweepy.Client(consumer_key=twitterAPI["client_ID"], consumer_secret=twitterAPI["client_secret"], access_token=twitterAPI["access_token"], access_token_secret=twitterAPI["access_token_secret"])

# Set up the ChatGPT API key
openai.api_key = 'sk-proj-1AxJLINN8uRmG56osnFsT3BlbkFJvhcz5MmHuuN6oRijxrG9'

client = OpenAI(
    # This is the default and can be omitted
    api_key='sk-proj-1AxJLINN8uRmG56osnFsT3BlbkFJvhcz5MmHuuN6oRijxrG9',
)


# Function 1: Admin User Topic Input + main function(calls the other functions from this function)
# Returns either "random" or the user's quote
# "random" option means that the topic will also be AI generated
def user_choose_topic():
    # User chooses if they would like to choose
    while True:
        userChoose = input("Would you like to choose the quote topic? If chosen no, the topic will be random (Y/N): ")
        if userChoose.lower().strip() in ("y", "yes"):
            break
        elif userChoose.lower().strip() in ("n", "no"):
            print("The quotes generated will be of a random topic. Please wait while the quotes are being generated. \n")
            return "random"
    # Continue and let user choose a prompt
    while True:
        choice = input("\nPlease choose the topic for the AI quote generation prompt: ")

        confirmation = input("Are you sure? (Y/N): ").lower()
        if confirmation in ["y", "yes"]:
            print("Please wait while the quotes are being generated. \n")
            return choice


# Function 2: ChatGPT AI Quote Generation
# Takes in input from function 1, generates quote based on user topic from function 1
# OR generates random quote if user chose random in function 1.
# Return value: a list of possible quotes
def generate_motivational_quote(topic):
    # If the user does not choose the topic, the quote generate should be random.
    if topic == "random":
        prompt = "Generate 10 original motivational quote in varying random topics (seperate them with new lines \\n)): "
    # User chosen topic used
    else:
        prompt = "Generate 10 original motivational quote in this topic (seperate them with new lines \\n)): " + str(topic)

    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": prompt,
            }
        ],
        model="gpt-3.5-turbo",
    )
    responses = chat_completion.choices[0].message.content.split("\n")
    return responses


# Function 3: Admin User selects the quote from list for upload to X/Twitter
# Come up with a function that allows user to chose a quote they want from the list.
def select_quote(quotes):
    for i in range(len(quotes)):
        print(quotes[i])
    while True:
        try:
            index = int(input("\nEnter the index of the quote you want to select: "))
            if 1 <= index <= len(quotes):
                return quotes[index - 1]
            else:
                print("Invalid index. Please enter a valid index.")
        except ValueError:
            print("Invalid input. Please enter a valid integer.")


# Function 4: Post it to X/Twitter through Tweepy API
def post_motivational_tweet(quote):
    """
    try:
        request = requests.post(url = "https://api.twitter.com/2/tweets", auth = auth, json = {quote}, headers={"Content-Type": "application/json"})
    except requests.exceptions as e:
        print("Error posting: ", e)
    """

    try:
        twitter_client.create_tweet(text = quote, user_auth=True)
        print("Tweet posted:", quote)
    except tweepy.TweepyException as e:
        print("Error posting tweet:", e)



# Run the program
topic = user_choose_topic()

listofquotes = generate_motivational_quote(topic)

quote = select_quote(listofquotes)

# Post the selected quote to Twitter
post_motivational_tweet(quote)
