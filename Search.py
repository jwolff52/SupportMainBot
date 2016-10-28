import DatabaseHandler
import Config

def isValidComment(comment, reddit):
    try:
        if (DatabseHandler.commentExists(comment.id):
            return False

        try:
            if (comment.author.name == Config.USERNAME):
                DatabaseHandler.addComment(comment.id, comment.author.name, comment.subreddit, False)
                return False
        except:
            pass

        return True

    except:
        traceback.print_exc()
        return False
