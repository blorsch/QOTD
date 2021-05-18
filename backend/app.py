from flask import Flask, request, escape, jsonify, make_response, current_app
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql.expression import func
import os
from flask_cors import CORS
from functools import wraps, update_wrapper
from datetime import datetime, timedelta
import jwt

app = Flask(__name__)
env_config = os.getenv("APP_SETTINGS", "config.DevelopmentConfig")
app.config.from_object(env_config)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
CORS(app)
app.config['CORS_HEADERS'] = 'Access-Control-Allow-Origin'

from models import Quote, User

def crossdomain(origin=None, methods=None, headers=None, max_age=21600,
                attach_to_all=True, automatic_options=True):
    """Decorator function that allows crossdomain requests.
      Courtesy of
      https://blog.skyred.fi/articles/better-crossdomain-snippet-for-flask.html
    """
    if methods is not None:
        methods = ', '.join(sorted(x.upper() for x in methods))
    # use str instead of basestring if using Python 3.x
    if headers is not None and not isinstance(headers, str):
        headers = ', '.join(x.upper() for x in headers)
    # use str instead of basestring if using Python 3.x
    if not isinstance(origin, str):
        origin = ', '.join(origin)
    if isinstance(max_age, timedelta):
        max_age = max_age.total_seconds()

    def get_methods():
        """ Determines which methods are allowed
        """
        if methods is not None:
            return methods

        options_resp = current_app.make_default_options_response()
        return options_resp.headers['allow']

    def decorator(f):
        """The decorator function
        """
        def wrapped_function(*args, **kwargs):
            """Caries out the actual cross domain code
            """
            if automatic_options and request.method == 'OPTIONS':
                resp = current_app.make_default_options_response()
            else:
                resp = make_response(f(*args, **kwargs))
            if not attach_to_all and request.method != 'OPTIONS':
                return resp

            h = resp.headers
            h['Access-Control-Allow-Origin'] = origin
            h['Access-Control-Allow-Methods'] = get_methods()
            h['Access-Control-Max-Age'] = str(max_age)
            h['Access-Control-Allow-Credentials'] = 'true'
            h['Access-Control-Allow-Headers'] = \
                "Origin, X-Requested-With, Content-Type, Accept, Authorization"
            if headers is not None:
                h['Access-Control-Allow-Headers'] = headers
            return resp

        f.provide_automatic_options = False
        return update_wrapper(wrapped_function, f)
    return decorator

# https://stackabuse.com/single-page-apps-with-vue-js-and-flask-jwt-authentication/

@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    user = User(**data)
    db.session.add(user)
    db.session.commit()
    return jsonify(user.serialize()), 201


@app.route('/login', methods=['POST'])
def login():
    print("here")
    data = request.get_json()
    user = User.authenticate(**data)

    if not user:
        return jsonify({'message': 'Invalid credentials', 'authenticated': False}), 401

    token = jwt.encode({
        'sub': user.email,
        'iat':datetime.utcnow(),
        'exp': datetime.utcnow() + timedelta(minutes=60)},
        os.environ['FLASK_SECRET_KEY'])
    return jsonify({'token': token})


def token_required(f):
    @wraps(f)
    def _verify(*args, **kwargs):
        auth_headers = request.headers.get('Authorization', '').split()

        invalid_msg = {
            'message': 'Invalid token. Registeration and / or authentication required',
            'authenticated': False
        }
        expired_msg = {
            'message': 'Expired token. Reauthentication required.',
            'authenticated': False
        }

        if len(auth_headers) != 2:
            return jsonify(invalid_msg), 401

        try:
            token = auth_headers[1]
            data = jwt.decode(token, os.environ['FLASK_SECRET_KEY'], algorithms=["HS256"])
            user = User.query.filter_by(email=data['sub']).first()
            if not user:
                raise RuntimeError('User not found')
            return f(user, *args, **kwargs)
        except jwt.ExpiredSignatureError:
            return jsonify(expired_msg), 401 # 401 is Unauthorized HTTP status code
        except (jwt.InvalidTokenError, Exception) as e:
            print(f"Error {e}")
            return jsonify(invalid_msg), 401
    return _verify

# start unique code

@app.route('/add-quote', methods=['POST'])
@token_required
def add_quote(*args):
    print(*args)
    text = escape(request.get_json(force = True)["text"])
    author = escape(request.get_json(force = True)["author"])
    try:
        new_quote = Quote(
            text=text,
            author=author
        )
        db.session.add(new_quote)
        db.session.commit()
        return "success", 201
    except Exception as e:
        print(e)
        return "error", 400

@app.route('/delete-quote/<id>', methods=['POST'])
#@token_required - messing with arguments
def delete_quote(id):
    #id = kwargs["id"]
    try:
        to_delete = Quote.query.filter_by(id=escape(id)).first()
        print(to_delete)
        db.session.delete(to_delete)
        db.session.commit()
        return "success", 200
    except Exception as e:
        print(e)
        return "error", 400

@app.route('/list-quotes', methods=["GET"])
@token_required
def list_quotes(*args):
    print(*args)
    try:
        quotes = Quote.query.all()
        jsonified = jsonify(quotes=[e.serialize() for e in quotes])
        return jsonified, 200
    except Exception as e:
        print(e)
        return "error", 400

@app.route('/random-quote', methods=["GET"])
def random_quote():
    try:
        quote = Quote.query.order_by(func.random()).limit(1).all()
        print(quote)
        jsonified = jsonify(quotes=[e.serialize() for e in quote])
        return jsonified, 200
    except Exception as e:
        print(e)
        return "error", 400

if __name__ == '__main__':
    app.run()
