from flask import Flask, url_for, request
from github import Github

app = Flask(__name__)

CLIENT_ID = "ef2350442ef233ab666c"
CLIENT_SECRET = "680a3834b54e58171157d73b2a752f1053254a59"
REDIRECT_URI = "http://localhost:5000/build"


@app.route('/')
def homepage():
    text = '<a href="%s">Authenticate with github</a>'
    return text % make_authorization_url()

def make_authorization_url():
    # Generate a random string for the state parameter
    # Save it for use later to prevent xsrf attacks
    from uuid import uuid4
    state = str(uuid4())
    save_created_state(state)
    params = {"client_id": CLIENT_ID,
              "response_type": "code",
              "state": state,
              "redirect_uri": REDIRECT_URI,
              "duration": "temporary",
              "scope": "identity"}
    import urllib
    url = "https://github.com/login/oauth/authorize?" + urllib.urlencode(params)
    return url

# Left as an exercise to the reader.
# You may want to store valid states in a database or memcache,
# or perhaps cryptographically sign them and verify upon retrieval.
def save_created_state(state):
    pass
def is_valid_state(state):
    return True



'''
@app.route('/')
def api_root():
    return 'Welcome'
'''
    
@app.route('/build')
def api_list():
    out = ""
   
    g = Github( request.args.get('code') )
    
    for repo in g.get_user().get_repos():
        out += repo.name + "\n"
    return 'List of ' + url_for('api_list') + "\n\n" + out


@app.route('/build/<repo>')
def api_build(repo):
    return 'You are reading ' + repo

if __name__ == '__main__':
    app.run(debug=True, port=5000)
