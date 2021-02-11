import requests as req
import firebase_admin
from firebase_admin import credentials, firestore
import os
from datetime import datetime
from textblob import TextBlob

THIS_FOLDER = os.path.dirname(os.path.abspath(__file__))
my_file = os.path.join(THIS_FOLDER, 'gamestock_fbcreds.json')

def get_reddit():
    cred = credentials.Certificate(my_file)
    firebase_admin.initialize_app(cred)
    db = firestore.client()
    auth = req.auth.HTTPBasicAuth('7pYQfHV4WpKo7Q','PzrLX-CLm6q03FNWHngi4Y76_Qihgg')
    data = {
        'grant_type':'password',
        'username':'Schnausages',
        'password':'LoonSpidermanToon84'
    }
    headers = {'User-Agent':'gamestock_test/0.0.1'}
    res = req.post('https://www.reddit.com/api/v1/access_token', auth = auth,
    data=data, headers = headers)
    TOKEN = res.json()['access_token']
    headers = {**headers, **{'Authorization': f"bearer {TOKEN}"}}
    games_subreddit_list = ['FortNiteBR','CallOfDuty','GrandTheftAutoV']
    for eachGame in games_subreddit_list:
        #response = req.get("https://oauth.reddit.com/r/python/hot",
        response = req.get(f'https://oauth.reddit.com/r/{eachGame}/hot',
        
        params={'limit':'5'},headers=headers)
        response_json = response.json()
        #return response_json
        score_list = []
        for each in response_json['data']['children']:
            text_body = each['data']['selftext']
            text_blob = TextBlob(text_body)
            post_score = text_blob.sentiment.subjectivity * 100
            score_list.append(post_score)
        data ={
            u'game':f'{eachGame}',
            u'scores':score_list
        }
        db.collection(u'games').document().set(data)
    # return {'SCORE LIST': score_list}