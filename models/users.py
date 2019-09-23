import json
from models.clubs import *
import sys

def saveUsers(users): #can be easilly/seamlessly updated for a different database system
    with open('data/users.json', 'w') as json_file:
        json.dump(users, json_file)

def getUsers(): #can be easilly/seamlessly updated for a different database system
    with open('data/users.json') as json_file:
        return json.load(json_file)

def getUserByUsername(username):
    user = None
    index=-1
    users=getUsers()
    for i,u in enumerate(users):
        if(u["username"]==username):
            user=u
            index=i
    return (user, index)

def getUserByUsernamePublic(username):
    (user, index) = getUserByUsername(username)
    if(user == None):
        return (None, -1)
    return {"username":username,"name":user["name"],"year":user["year"], "school":user["school"],"favtags":user["favtags"], "favclubs":user["favclubs"]}
    #the above return ensures that only public-safe user data is returned
    #(excluding passwords, activity history, or anything else in our user database that might be sensitive info)
