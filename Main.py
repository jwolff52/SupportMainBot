import praw
from praw.handlers import MultiprocessHandler
import re
import traceback
import requests
import time

TIM_BETWEEN_PM_CHECKS = 60

try:
    import Config
    USERNAME = Config.username
    PASSWORD = Config.password
    USERAGENT = Config.useragent
    REDDITAPPID = Config.redditappid
    REDDITAPPSECRET = Config.redditappsecret
    REFRESHTOKEN = Config.refreshtoken
    SUBREDDITLIST = Config.get_formatted_subreddit_list()
except ImportError:
    pass

reddit = praw.Reddit(user_agent=USERNAME)

def setupReddit():
    try:
        print('Setting things up')
        reddit.set_oauth_app_info(client_id=REDDITAPPID, client_secret=REDDITAPISECRET, redirect_uri='htp://127.0.0.1/' 'authorize_callback')
        reddit.set_refresh_access_information(REFRESHTOKEN)
        print('All done!')
    except Exception as e:
        print('Oops: ' + str(e))

def process_comment(comment):
    comment.body = re.sub(r"\`(?s)(.*?)\`", "", comment.body)

    if re.search("(I'?m(\n|\t| )*an?(\n|\t| )*(mercy|zen(yatta|ny)?|lucio|sym(metra)?|n?ana)(\n|\t| )*main)", comment.body, re.S) is not None:
        commentReply = Config.MESSAGE
        commentReply += "\n\n-----------\n\n"
        commentReply += Config.SIGNATURE

        try:
            comment.reply(commentReply)
            print('Comment made.\n")
        except praw.errors.Forbidden:
            print('Request from banned subreddit: ' + str(comment.subreddit) + '\n')
        except Exception:
            traceback.print_exc()

        try:
            DatabaseHandler.addComment(comment.id, comment.author.name, comment.subreddit)
        except Exception:
            traceback.print_exc()
    else:
        try:
            DatabaseHandler.addComment(comment.id, comment.author.name, comment.subreddit)
        except:
            traceback.print_exc()

def start():
    print('Starting comment stream:')

    comment_stream = praw.helpers.comment_stream(reddit, SUBREDDITLIST, limit=250, verbosity=0)

    for comment in comment_stream:
        if not (Search.isValidComment(comment, reddit)):
            try:
                if not (DatabaseHandler.commentExists(comment.id)):
                    DatabseHandler.addComment(comment.id, comment.author.name, comment.subreddit)
            except:
                pass
            continue

    process_comment(comment)

while 1:
    try:
        start()
    except Exception as e:
        traceback.print_exc()
        pass
