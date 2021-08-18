from flask import Blueprint, request
from flask_jwt_extended.view_decorators import jwt_required

from src.services import BookmarkService

from flask_jwt_extended import get_jwt_identity


bookmarks = Blueprint("bookmarks", __name__, url_prefix="/api/v1/bookmarks")

@bookmarks.route('/', methods=['GET', 'POST'])
@jwt_required()
def handle_bookmarks():
    user_id = get_jwt_identity()
    data = request.json

    page = request.args.get('page', 1, type=int)
    size = request.args.get('size', 5, type=int)

    if request.method == 'POST':
        return BookmarkService.create_bookmark(data, user_id)
    else:
        return BookmarkService.get_all_bookmarks(user_id, page, size)
