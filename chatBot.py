import time
import random
import json
import re
import ezgmail
from nltk.sentiment import SentimentIntensityAnalyzer as sia
#import nltk


# GLOBAL CONSTANTS
H_WEIGHT = 0.5   # history weight (on aggression calculator)
AGGRESSION_CAP = 29 # maximum agression value (how long the response lists are minus 1)
SENTIMENT_WEIGHT = 10 # weight on negative sentiment analysis to calculate beg aggression variable a
RANDOM_WEIGHT = 5 # weight on randomness factor
PAUSE_TIME = 60 # pause time in between email scans (in seconds)

# regexs for which response list to choose from
qRe = re.compile(r'wat|what|\?|wut|whaat|who|why|where') # question flags
gRe = re.compile(r'hey|hi|hello|heey|greetings')    # greeting flags
pRe = re.compile(r'bye|goodbye|goobye|cya|see ya|ttyl|ciao|salutations|deuces')


# LISTS OF RESPONSES (20 each)
# (ordered from least aggressive to most aggressive)
# Question responses
qResponses = [ # has 30
    "Good question, but im not sure.",
    "good question man",
    "good question",
    "Yes!",
    "YES",
    "yaaa",
    "good q",
    "yes",
    "yeah for sure",
    "No, i dont think so",
    "Yeah sure",
    "I'm sorry, no",
    "aaaaah im not sure",
    "not sure man",
    "E",
    "ye",
    "nee",
    "bruh",
    "idk man dont ask me",
    "what do you think?",
    "i mean i dont know the answer to that",
    "naaaaah dude",
    "no thank you!",
    "uuuuuuuuuuuuuuuuh i dont know pls dont ask again",
    "nope",
    "bruh",
    "bruh why did you ask me",
    "Couldnt you google that?"
    "bad question",
    "ew why did you ask that"
    ]
# Greeting responses
gResponses = [ #has 30
    "Hey <name>, whats up :)",
    "Hey :)",
    "Hi :)",
    "hi <name> :)",
    "hello:)",
    "Hi <name>! It's so nice to talk to you!",
    "always nice to hear from you <name>, whats up",
    "hey <name>, its nice to hear from you",
    "aaaayyyy how are you doing family",
    "hey <name>, whats up>",
    "aaayyyyy",
    "Hey <name>, wats poppin",
    "whats up dude",
    "hey",
    "ay",
    "aaaay",
    "whats poppin",
    "Yo",
    "yo",
    "E",
    "A",
    "whats up",
    "hi",
    "not really in the mood to talk right now",
    "wat",
    "I don't want to talk to you <name>, I have the cans in.",
    "what",
    "im not your friend anymore <name>",
    "uhhhhh youre gross",
    "you are too stinky to talk to me <name>. Seriously"
    ]
# Statement responses
sResponses = [ # has 30
    "Hell yeah <name>",
    "Okay:)",
    ":)"
    "(:"
    "okay, i like that!",
    "I agree wholeheartedly",
    "Im not sure i can get behind that, but I give you my respect",
    "Yeah. Wanna play bball?",
    "Yeah sure",
    "uh huh",
    "yes",
    "e",
    "E",
    "A",
    "a",
    "okay",
    "cool",
    "sounds good",
    "yup",
    "eep",
    "nah",
    "not a fan of that idea",
    "tbh nah man",
    ".....",
    "Okay but why?",
    "ummmmm no",
    ">:(",
    "okay.................",
    "shut up",
    "."
    ]
# Parting reponses
pResponses = [ # has 30
    "See you later friend! nice talking to you <name>",
    "Bye:)))",
    "bye:)",
    "see you <name>! :)",
    "nice talkin, peace out:)",
    "see you later!",
    "bye <name>",
    "have a good rest of your day <name>, bye",
    "see ya",
    "ciao",
    "bye!",
    "bye",
    "cya",
    "ttyl",
    "salutations",
    "goobye",
    "goodbye",
    "..bye",
    "have a good one",
    "nice talkin",
    "byee",
    "byeee",
    "okay bye",
    "bye",
    "bye.",
    "goodbye.",
    "L",
    "bye >:(",
    ".",
    "good riddance"
    ]


class User:
    def __init__(self, data1):
        self.email = data1['email']
        self.name = data1['name']
        self.history = data1['history']

    def Respond(self, mes):
        # Run Regexs on the string to determine the type of response to give
        # if the string is...
        if qRe.match(mes.lower()) is not None: # a question (has a question flag)
            responseList = qResponses
        elif gRe.match(mes.lower()) is not None: # a greeting
            responseList = gResponses
        elif pRe.match(mes.lower()) is not None: # a goodbye
            responseList = pResponses
        else: # nothing else, so it is a statement
            responseList = sResponses
        # Use sentiment intensity analyzer to get the negative sentiment of the string
        sentiment = SIA.polarity_scores(str(mes))
        negative_sentiment = sentiment['neg']
        a = negative_sentiment * SENTIMENT_WEIGHT # start of aggression variable
        h = self.history
        r3 = random.random() # random float between 0 and 1
        r2 = random.choice([1,0])
        if r2 == 0:
            sign1 = -1
        else:
            sign1 = 1
        r = r3*sign1
        A = a + H_WEIGHT*h + r*RANDOM_WEIGHT
        if A > AGGRESSION_CAP:  # capping the aggression variable 
            aPrime = AGGRESSION_CAP
        else:
            aPrime = int(round(A))
        response1 = responseList[aPrime] # response choice
        response = response1.replace('<name>', self.name) # insert name
        
        return response



print('[Starting...]')
# configure sentiment analysis
#nltk.download('vader_lexicon')
SIA = sia()

#MAIN LOOP
while True:
    
    #check email for unread emails
    print('\n[Looking...]')
    unreadThreads = ezgmail.unread()
    if unreadThreads:  # if there are any unread emails
        ut = len(unreadThreads)
        print(f'\n[There are {ut} unread emails.]')
        # for each unread email
        v = 0
        for v in range(len(unreadThreads)):
            y=v+1
            print(f'\n\nEmail {y}:')
            user_email = str(unreadThreads[v].messages[0].sender)# store email as string

            unreadThreads[v].markAsRead() # mark email as read
            
            if '@pm.sprint.com' in user_email: # if user has a sprint email
                text = unreadThreads[v].messages[0].snippet
                text = re.sub(r'Sent from my mobile.\s_____________________________________________________________\s',
                              '', text)

                    
            else:
                if '@mms.uscc.net' in user_email:   # if the user has a US CELLULAR phone carrier
                    attachmentName = 'text950.txt'
                else:
                    attachmentName = 'text_0.txt'
                
                try:                    # if there is not a file move on to the next email
                    # download the text file
                    unreadThreads[v].messages[0].downloadAttachment(attachmentName, downloadFolder='attachments')
                    print('[Attachment downloaded.]')

                except AttributeError:
                    print(' ! Attachment not found')
                    unreadThreads[v].markAsRead() # mark email as read
                    continue # move on
                
                unreadThreads[v].markAsRead()   # mark email as read
                textFile = open('attachments/' + attachmentName)   # open text file
                text = textFile.read() # turn into string with no newlines
                textFile.close()    # close text file


            print(f'''Message: "{text}"''')
            
            with open('data/data.txt') as json_file: # open user data file
                isExistingUser = False   # is new user variable
                try:
                    user_data = json.load(json_file) # load data
                    print('[User data loaded.]')
                    for v in user_data['users']: # for each user
                        if v['email'] == user_email: # if the email is in the database
                            print(f'[Existing user {user_email}.]')
                            userData = v # individual user dicitonary
                            v['history'] += 1 # add one to history
                            isExistingUser = True     
                except:
                    print('[There is no user data.]')
                    isExistingUser = False
                    user_data = {}
                    user_data['users'] = []

                # if new user make a new user class
                if isExistingUser == False:
                    print(f'[New user {user_email}.]')
                    user_data['users'].append({
                        'email':user_email,
                        'name':'friend',
                        'history':1,
                        })
                    userData = user_data['users'][-1]   # individual user dicitonary
                json_file.close()

            #email time
            user1 = User(userData) # user class
            aResponse = user1.Respond(text) # guh response
            print('[response received.]')
            print(f'''response: "{aResponse}"''')
            ezgmail.send(user_email,'',aResponse)   # send guh response
            print(f'[Email sent to {user_email}.]')
            # save data to txt file in json format
            with open('data/data.txt', 'w') as outfile:
                json.dump(user_data, outfile)
                outfile.close
                
            print('[User database updated.]')
                
            
    else:
        print('[No unread emails.]')
        
    time.sleep(PAUSE_TIME) # pause by the pause time (global variable at top of this script

            # save da data somewhere i can peek at it
                # wat data?
                    # individual user&guh conversation data
                    # aggression level for each message
            


    
