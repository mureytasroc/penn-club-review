import json
from models.scraper import * # Web Scraping utility functions for Online Clubs with Penn.
from models.users import *
import sys

def getClubData():
    clubSoups=get_clubs(soupify(get_clubs_html()))
    clubs = list(map(lambda x: {"name":get_club_name(x), "description":get_club_description(x), "tags":get_club_tags(x), "likes":0}, clubSoups))
    tags = []
    tagColors = []
    colors = ["Aqua","Aquamarine","Bisque","Black","Blue","BlueViolet","Brown","BurlyWood","CadetBlue","Chartreuse","Chocolate","Coral","CornflowerBlue","Cornsilk","Crimson","Cyan","DarkBlue","DarkCyan","DarkGoldenRod","DarkGray","DarkGrey","DarkGreen","DarkKhaki","DarkMagenta","DarkOliveGreen","DarkOrange","DarkOrchid","DarkRed","DarkSalmon","DarkSeaGreen","DarkSlateBlue","DarkSlateGray","DarkSlateGrey","DarkTurquoise","DarkViolet","DeepPink","DeepSkyBlue","DimGray","DimGrey","DodgerBlue","FireBrick","FloralWhite","ForestGreen","Fuchsia","Gainsboro","GhostWhite","Gold","GoldenRod","Gray","Grey","Green","GreenYellow","HoneyDew","HotPink","IndianRed","Indigo","Ivory","Khaki","Lavender","LavenderBlush","LawnGreen","LemonChiffon","LightBlue","LightCoral","LightCyan","LightGoldenRodYellow","LightGray","LightGreen","LightPink","LightSalmon","LightSeaGreen","LightSkyBlue","LightSteelBlue","LightYellow","Lime","LimeGreen","Linen","Magenta","Maroon","MediumAquaMarine","MediumBlue","MediumOrchid","MediumPurple","MediumSeaGreen","MediumSlateBlue","MediumSpringGreen","MediumTurquoise","MediumVioletRed","MidnightBlue","MintCream","MistyRose","Moccasin","NavajoWhite","Navy","OldLace","Olive","OliveDrab","Orange","OrangeRed","Orchid","PaleGoldenRod","PaleGreen","PaleTurquoise","PaleVioletRed","PapayaWhip","PeachPuff","Peru","Pink","Plum","PowderBlue","Purple","RebeccaPurple","Red","RosyBrown","RoyalBlue","SaddleBrown","Salmon","SandyBrown","SeaGreen","SeaShell","Sienna","Silver","SkyBlue","SlateBlue","SlateGray","SlateGrey","Snow","SpringGreen","SteelBlue","Tan","Teal","Thistle","Tomato","Turquoise","Violet","Wheat","Yellow","YellowGreen"];
    count=0
    for c in clubs:
        c["tagColors"]=[]
        for t in c["tags"]:
            if(t in tags):
                c["tagColors"].append(tagColors[tags.index(t)])
            else:
                tags.append(t)
                if(count<len(colors)):
                    tagColors.append(colors[count])
                    c["tagColors"].append(colors[count])
                    count+=1
                else:
                    color = random.choice(colors)
                    tagColors.append(color)
                    c["tagColors"].append(color)
    return (clubs, tags)

def saveTags(tags):
    with open('data/tags.json', 'w') as json_file:
        json.dump(tags, json_file)

def getTags():
    with open('data/tags.json') as json_file:
        return json.load(json_file)

def saveClubs(clubs): #can be easilly/seamlessly updated for a different database system
    with open('data/clubs.json', 'w') as json_file:
        json.dump(clubs, json_file)

def getClubs(): #can be easilly/seamlessly updated for a different database system
    with open('data/clubs.json') as json_file:
        return json.load(json_file)

def getClubByName(name):
    club = None
    index=-1
    for i,c in enumerate(getClubs()):
        if(c["name"]==name):
            club=c
            index=i
    return (club, index)

def addClub(name, description, tags):
    (club, index) = getClubByName(name)
    if not(club == None):
        return 'The club "'+name+'" already exists in our database (add failed).  If you want to update a club, use a put request.'
    club={"name":name, "description":description, "tags": tags}
    clubs=getClubs()
    clubs.append(club)
    saveClubs(clubs)
    return 'The club "'+name+'" was added to our database successfuly.'

def updateClub(name, description, tags):
    (club, index) = getClubByName(name)
    if(club == None):
        return "No club was found with that name (update failed)."
    club={"name":name, "description":description, "tags": tags}
    clubs=getClubs()
    clubs[index]=club
    saveClubs(clubs)
    return 'The club "'+name+'" was updated successfuly.'

def countLikes():
    clubs=getClubs()
    for c in clubs:
        c["likes"]=0
    saveClubs(clubs)
    users=getUsers()
    for u in users:
        for f in u["favclubs"]:
            (club, index) = getClubByName(f)
            club["likes"]+=1
            clubs[index]=club
    saveClubs(clubs)

def addLikes(username, likes):
    clubs=getClubs()
    users=getUsers()
    (user,userInd)=getUserByUsername(username)
    for l in likes:
        if not(l in user["favclubs"]):
            user["favclubs"].append(l)
            (club, index) = getClubByName(l)
            club["likes"]+=1
            clubs[index]=club
    saveClubs(clubs)
    users[userInd]=user
    saveUsers(users)

def setLikes(username, likes):
    clubs=getClubs()
    users=getUsers()
    (user,userInd)=getUserByUsername(username)
    for l in likes:
        if not(l in user["favclubs"]):
            (club, index) = getClubByName(l)
            club["likes"]+=1
            clubs[index]=club
    for f in user["favclubs"]:
        if not(f in likes):
            (club, index) = getClubByName(l)
            club["likes"]-=1
            clubs[index]=club
    saveClubs(clubs)
    user["favclubs"]=likes
    users[userInd]=user
    saveUsers(users)
