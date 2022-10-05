from app import app, helpers, response
from flask import request, render_template, make_response
from functools import wraps
from app.controller import users

#middleware
def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        # jwt is passed in the request header
        if 'x-access-token' in request.headers:
            token = request.headers['x-access-token']
        
        validation = helpers.validateToken(token)
        if validation['status'] != '200' :
            return response.resp(validation['status'], 'Something wrong')
        
        return  f(validation['user_id'], *args, **kwargs)
  
    return decorated

# REGISTER
@app.route('/register', methods=['POST'])
def register():
    return users.register()

#LOGIN
@app.route('/login', methods=['POST'])
def login():
    return users.login()