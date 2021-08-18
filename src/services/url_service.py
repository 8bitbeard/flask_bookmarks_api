from flask.json import jsonify
import validators
from validators.url import url

from src.constants import http_status_codes

from src.models import Bookmark
from src.database import db


class UrlService():

    def get_bookmark(short_url):
        bookmark = Bookmark.query.filter_by(short_url=short_url).first_or_404()

        if bookmark:
            bookmark.visits = bookmark.visits + 1
            db.session.commit()

            return bookmark