import requests as req
import firebase_admin as admin
from firebase_admin import credentials, firestore
from google.cloud import firestore as fs
import os
from datetime import datetime
from textblob import TextBlob
from flask import Flask, jsonify, make_response
import praw
from praw.models import MoreComments
import statistics

# app = Flask(__name__)

THIS_FOLDER = os.path.dirname(os.path.abspath(__file__))
my_file = os.path.join(THIS_FOLDER, 'gamestock_fbcreds.json')

reddit = praw.Reddit(
        client_id = '7pYQfHV4WpKo7Q',
        client_secret = 'PzrLX-CLm6q03FNWHngi4Y76_Qihgg',
        user_agent = 'gamestock_test',
        # username:'Schnausages',
        # password:'LoonSpidermanToon84'
    )

cred = credentials.Certificate(my_file)
admin.initialize_app(cred)
#db = firestore.client()
db = admin.firestore.client()

# @app.route('/reddit', methods=['Get'])
def get_reddit():
    games_subreddit_list = ['FortNiteBR','CallOfDuty','GrandTheftAutoV','PokemonGo','leagueoflegends']
    for each in games_subreddit_list:
        print(f'TRYING TO FETCH {each} ?!?!??!?!??!?!?!')
        subreddit = reddit.subreddit(each)
        top_posts = subreddit.top(limit=5,time_filter='day')
        for submission in top_posts:
            submission.comments.replace_more(limit=0)
            comments = submission.comments
            comment_list = []
            for comment in comments:
                blob = TextBlob(comment.body)
                if len(blob) < 10: #remove short comments
                    continue
                comment_list.append(blob.sentiment.polarity * 100)
                
        if len(comment_list) > 2:
            scores_avg = statistics.mean(comment_list)
            data = {
                u'game': each,
                u'scores': fs.ArrayUnion([scores_avg]),

                # u'scores': firestore.FieldValue.arrayUnion(scores_avg),
            }
            db.collection(u'games').document(f'{each}').set(data, merge = True)
        else:
            continue
        #TESTING REMOVE
        # db.collection(u'games').document.update({'scores':FieldValue.arrayRemove([-1:-4])})

def testFunction():
    print('!??!?!?! RUNNING TEST FUNCKIOTONT !?!?!??!?')
    db.collection(u'games').document(f'TEST GAME').set({
        u'game':'TEST DUTY 4',
        u'scores':[41,55,32,21,20]
    }, merge = True)
get_reddit()
testFunction()
