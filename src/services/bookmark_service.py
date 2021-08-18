from flask.json import jsonify
import validators

from src.constants import http_status_codes

from src.models import Bookmark
from src.database import db


class BookmarkService():

    def create_bookmark(data, user_id):

        body_param = data['body']
        url_param = data['url']

        if not validators.url(url_param):
            return jsonify({
                'error': 'Enter a valid url'
            }), http_status_codes.HTTP_400_BAD_REQUEST

        if Bookmark.query.filter_by(url=url_param).first():
            return jsonify({
                'error': 'URL already exists!'
            }), http_status_codes.HTTP_409_CONFLICT

        bookmark = Bookmark(body=body_param, url=url_param, user_id=user_id)

        db.session.add(bookmark)
        db.session.commit()

        return jsonify({
            'id': bookmark.id,
            'url': bookmark.url,
            'short_url': bookmark.short_url,
            'visits': bookmark.visits,
            'body': bookmark.body,
            'created_at': bookmark.created_at,
            'updated_at': bookmark.updated_at
            }), http_status_codes.HTTP_201_CREATED

    def get_all_bookmarks(user_id):

        bookmarks = Bookmark.query.filter_by(user_id=user_id)

        data = []

        for bookmark in bookmarks:
            data.append({
                'id': bookmark.id,
                'url': bookmark.url,
                'short_url': bookmark.short_url,
                'visits': bookmark.visits,
                'body': bookmark.body,
                'created_at': bookmark.created_at,
                'updated_at': bookmark.updated_at
            })
        return jsonify({
            'data': data
        }), http_status_codes.HTTP_200_OK