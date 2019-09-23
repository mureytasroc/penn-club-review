from flask import Flask, request, render_template, Markup, jsonify, send_from_directory, url_for, make_response
import sys
from models.clubs import *
from urllib.parse import unquote
import chardet
from urllib.parse import unquote
import ast




app = Flask(__name__)

#---vvv
#(clubs, tags) = getClubData()
#saveClubs(clubs)
#saveTags(tags)
#---the club data will be rescraped every time the server starts up if the above lines are uncommented
#---this could be changed to refresh at certain intervals

countLikes()

@app.route('/static/<path:path>')
def send_js(path):
    return send_from_directory('static', path)

@app.route('/')
def main():
    return render_template('index.html')

@app.route('/clubs')
def clubsPage():
    username="jen"#change this
    userCode=username#change this
    (user,i)=getUserByUsername("jen")
    likedClubs=user["favclubs"]
    clubs=getClubs()
    tags=getTags()
    def trimDescription(club):
        desc = club["description"]
        if(len(desc)>125):
            desc=str(desc[0:120])+str("...")
        club["description"]=desc
        return club
    clubs=list(map(trimDescription,clubs))
    return render_template('clubs.html', clubs=clubs, tags=json.dumps(tags), tagsAr=tags, userCode=userCode, likedClubs=json.dumps(likedClubs))

@app.route('/account')
def accountPage():
    return render_template('edituser.html')

@app.route('/reviews/<cname>')
def reviewsPage(cname):
    (club,i)=getClubByName(cname.replace("_"," "))
    return render_template('reviews.html', club=club)

@app.route('/review/<cname>')
def reviewPage(cname):
    (club,i)=getClubByName(cname.replace("_"," "))
    return render_template('review.html', club=club)

@app.route('/api')
def api():
    return "Welcome to the Penn Club Review API!."

@app.route('/api/clubs', methods=['GET', 'POST', 'PUT'])
def api_clubs():
    if(request.method == 'GET'):
        return jsonify(getClubs())
    elif(request.method == 'POST'):
        return addClub(request.form['name'], request.form['description'], json.loads(request.form['tags']))
    else: #put
        return updateClub(request.form['name'], request.form['description'], json.loads(request.form['tags']))

@app.route('/api/user/<username>')
def api_getUserPublic(username):
    userPub = getUserByUsernamePublic(username)
    if(userPub == None):
        return "Requested user does not exist in our database"
    return jsonify(userPub)

@app.route('/api/favorite', methods=['POST', 'PUT'])
def apifav():
    rawdata=request.data
    enc = chardet.detect(rawdata)
    dataurl = str(rawdata.decode(enc['encoding']))
    datastring = unquote(dataurl).replace("data=","").replace('"',"'") #sorry for this heavy-handed workaround... ajax is annoying
    data=ast.literal_eval(datastring)
    if(request.method == 'POST'):
        username=data['username']
        addLikes(username, data["likes"])
        return json.dumps({'success':True}), 200, {'ContentType':'application/json'}
    if(request.method == 'PUT'):
        username=data['username']
        setLikes(username, data["likes"])
        return json.dumps({'success':True}), 200, {'ContentType':'application/json'}
