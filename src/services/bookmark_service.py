from flask import json
from flask.json import jsonify
import validators
from validators.url import url

from src.constants import http_status_codes

from src.models import Bookmark
from src.database import db


class BookmarkService:

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

    def get_all_bookmarks(user_id, page, size):

        bookmarks = Bookmark.query.filter_by(user_id=user_id).paginate(page=page, per_page=size)

        data = []

        for bookmark in bookmarks.items:
            data.append({
                'id': bookmark.id,
                'url': bookmark.url,
                'short_url': bookmark.short_url,
                'visits': bookmark.visits,
                'body': bookmark.body,
                'created_at': bookmark.created_at,
                'updated_at': bookmark.updated_at
            })

        meta={
            "page": bookmarks.page,
            "totalPages": bookmarks.pages,
            "totalElements": bookmarks.total,
            "previousPage": bookmarks.prev_num,
            "nextPage": bookmarks.next_num,
            "hasNext": bookmarks.has_next,
            "hasPrev": bookmarks.has_prev,
            "size": bookmarks.per_page
        }
        return jsonify({
            'data': data,
            'meta': meta
        }), http_status_codes.HTTP_200_OK

    def get_bookmark(user_id, bookmark_id):

        bookmark = Bookmark.query.filter_by(user_id=user_id, id=bookmark_id).first()

        if not bookmark:
            return jsonify({
                'message': 'Item not found'
            }), http_status_codes.HTTP_404_NOT_FOUND

        return jsonify({
            'id': bookmark.id,
            'url': bookmark.url,
            'short_url': bookmark.short_url,
            'visits': bookmark.visits,
            'body': bookmark.body,
            'created_at': bookmark.created_at,
            'updated_at': bookmark.updated_at
        }), http_status_codes.HTTP_200_OK

    def edit_bookmark(data, user_id, bookmark_id):
        bookmark = Bookmark.query.filter_by(user_id=user_id, id=bookmark_id).first()

        if not bookmark:
            return jsonify({
                'message': 'Item not found'
            }), http_status_codes.HTTP_404_NOT_FOUND

        if data['url']:
            if not validators.url(data['url']):
                return jsonify({
                    'error': 'Enter a valid url'
                }), http_status_codes.HTTP_400_BAD_REQUEST

            bookmark.url = data['url']

        if data['body']:
            bookmark.body = data['body']

        db.session.commit()

        return jsonify({}), http_status_codes.HTTP_204_NO_CONTENT

    def delete_bookmark(user_id, bookmark_id):
        bookmark = Bookmark.query.filter_by(user_id=user_id, id=bookmark_id).first()

        if not bookmark:
            return jsonify({
                'message': 'Item not found'
            }), http_status_codes.HTTP_404_NOT_FOUND

        db.session.delete(bookmark)
        db.session.commit()

        return jsonify({}), http_status_codes.HTTP_204_NO_CONTENT

    def get_stats(user_id):
        bookmarks = Bookmark.query.filter_by(user_id=user_id).all()

        data = []

        for bookmark in bookmarks:
            new_link = {
                'visits': bookmark.visits,
                'url': bookmark.url,
                'id': bookmark.id,
                'short_url': bookmark.short_url
            }
            data.append(new_link)

        return jsonify({
            'data': data
        }), http_status_codes.HTTP_200_OK
