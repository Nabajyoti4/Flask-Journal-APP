from apifairy import authenticate, body, other_responses, response

from . import users_api_blueprint
from project.user_api.schema import new_user_schema, user_schema, token_schema
from project.models import User
from project import db as database, basic_auth, ma


@users_api_blueprint.route('/', methods=['POST'])
@body(new_user_schema)
@response(user_schema, 201)
def register(kwargs):
    """Create a new user"""
    new_user = User(**kwargs)
    database.session.add(new_user)
    database.session.commit()
    return new_user


@users_api_blueprint.route('/get-auth-token', methods=['POST'])
@authenticate(basic_auth)
@response(token_schema)
@other_responses({401: 'Invalid username or password'})
def get_auth_token():
    """Get authentication token"""
    user = basic_auth.current_user()
    token = user.generate_auth_token()
    database.session.add(user)
    database.session.commit()
    return dict(token=token)