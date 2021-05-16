from flask import Flask, request, escape, jsonify
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)
env_config = os.getenv("APP_SETTINGS", "config.DevelopmentConfig")
app.config.from_object(env_config)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

from models import Quote


@app.route('/add-quote', methods=['POST'])
def add_quote():
    text = escape(request.get_json(force = True)["text"])
    author = escape(request.get_json(force = True)["author"])
    try:
        new_quote = Quote(
            text=text,
            author=author
        )
        db.session.add(new_quote)
        db.session.commit()
        return "success", 200
    except Exception as e:
        print(e)
        return "error", 400

@app.route('/list-quotes', methods=["GET"])
def list_quotes():
    try:
        quotes = Quote.query.all()
        jsonified = jsonify(quotes=[e.serialize() for e in quotes])
        print(jsonified)
        return jsonified, 200
    except Exception as e:
        print(e)
        return "error", 400


if __name__ == '__main__':
    app.run()
