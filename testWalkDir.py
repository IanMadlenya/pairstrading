from processFuncs import *
import sys
import os
directory=r'/home/webmaster/Documents/Source/Python/mongoDB/stockData/import'

#Check for new update files:
#look in update directory
#   if files exists
#       check csv structure
#       compare to expected structure
#        if ok
#            begin import
#            if import ok
#                delete .d files that need to be recalculated
#Recalculation will happen automatically

if __name__ == '__main__':
    walktree(directory, importFile)
    
    if False:
        from pymongo import MongoClient
        client = MongoClient()
        db = client.test_database
        #Date format 12-Jun-2013
        import datetime
        post = {"author": "Mike","text": "My first blog post!","tags": ["mongodb", "python", "pymongo"],"date": datetime.datetime.utcnow()}
        posts = db.posts
        post_id = posts.insert(post)
        db.collection_names()
