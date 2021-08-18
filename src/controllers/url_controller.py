from flask import Blueprint, redirect

from src.services import UrlService


url = Blueprint("url", __name__, url_prefix="")

@url.get('/<short_url>')
def redirect_to_url(short_url):
    print(short_url)
    bookmark = UrlService.get_bookmark(short_url)

    return redirect(bookmark.url)