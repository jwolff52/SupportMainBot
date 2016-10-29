import praw
from praw.handlers import MultiprocessHandler
from datetime import datetime
from datetime import timedelta
import re
import traceback
import requests
import time

import DatabaseHandler
import Search

try:
    import Config
    USERNAME = Config.USERNAME
    PASSWORD = Config.PASSWORD
    USERAGENT = Config.USERAGENT
    REDDITAPPID = Config.REDDITAPPID
    REDDITAPPSECRET = Config.REDDITAPPSECRET
    REFRESHTOKEN = Config.REFRESHTOKEN
    SUBREDDITLIST = Config.getSubList()
except ImportError:
    pass

reddit = praw.Reddit(user_agent=USERAGENT)

def setupReddit():
    try:
        print('Setting things up')
        reddit.set_oauth_app_info(client_id=REDDITAPPID, client_secret=REDDITAPPSECRET, redirect_uri='http://127.0.0.1/' 'authorize_callback')
        reddit.refresh_access_information(REFRESHTOKEN)
        print('All done!')
    except Exception as e:
        print('Oops: ' + str(e))
	traceback.print_exc()

def process_comment(comment):
    comment.body = re.sub(r"\`(?s)(.*?)\`", "", comment.body)

    if re.search("((mercy|zen(yatta|ny)?|lucio|sym(metra)?|n?ana)(\n|\t|\^| )*main(\n|\t|\^| )*btw)", comment.body, re.I) is not None:
        commentReply = Config.MESSAGE
        commentReply += "\n\n-----------\n\n"
        commentReply += Config.SIGNATURE

        try:
            comment.reply(commentReply)
            print('Comment made.\n')
        except praw.errors.Forbidden:
            print('Request from banned subreddit: ' + str(comment.subreddit) + '\n')
        except Exception:
            traceback.print_exc()

        try:
            DatabaseHandler.addComment(comment.id, comment.author.name, comment.subreddit, True)
        except Exception:
            traceback.print_exc()
    else:
        try:
            DatabaseHandler.addComment(comment.id, comment.author.name, comment.subreddit, False)
        except:
            traceback.print_exc()

def start():
    print('Starting comment stream:')

    comment_stream = praw.helpers.comment_stream(reddit, 'weebobot+overwatch', limit=250)
    for comment in comment_stream:
        if not (Search.isValidComment(comment, reddit)):
            try:
                if not (DatabaseHandler.commentExists(comment.id)):
                    DatabaseHandler.addComment(comment.id, comment.author.name, comment.subreddit, False)
            except:
                pass
            continue

        print('New Comment in: /r/{0} by /u/{1}: {2}'.format(comment.subreddit, comment.author.name, comment.body[:50]))
        process_comment(comment)

setupReddit()

while 1:
    try:
        start()
    except Exception as e:
        traceback.print_exc()
        pass
    print('Looping')
