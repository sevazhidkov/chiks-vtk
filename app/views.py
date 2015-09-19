import random

import pymongo
from bson.objectid import ObjectId

from flask import render_template, request, redirect, url_for

from . import app
from .db import db
from .rating import rating


@app.route('/')
def index():
    # Создаем пару девушек для голосования
    first_girl = random.choice(list(db.girls.find()))
    second_girl = random.choice(list(db.girls.find({
        '_id': {'$ne': first_girl['_id']}
    })))

    # Генерируем рейтинг девушек
    girls_rating = db.girls.find(limit=10).sort([
        ('rating', pymongo.DESCENDING),
    ])
    return render_template('index.html', girls=girls_rating, pair=[
        first_girl, second_girl
    ])


@app.route('/vote')
def vote():
    print(request.args['winner'])
    winner_id = ObjectId(request.args['winner'])
    loser_id = ObjectId(request.args['loser'])
    winner_girl = list(db.girls.find({'_id': winner_id}))[0]
    loser_girl = list(db.girls.find({'_id': loser_id}))[0]

    # С помощью формулы рейтинга Эло, обновляем рейтинги девушек
    db.girls.update_one({'_id': winner_girl['_id']}, {
        '$set': {
            'rating': rating(winner_girl['rating'], 1, loser_girl['rating']),
            'checks': winner_girl['checks'] + 1
        }
    })
    db.girls.update_one({'_id': loser_girl['_id']}, {
        '$set': {
            'rating': rating(loser_girl['rating'], 0, winner_girl['rating']),
            'checks': loser_girl['checks'] + 1
        }
    })

    return redirect(url_for('index'))
