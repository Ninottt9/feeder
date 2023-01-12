import functools

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash

from feeder.db import get_db

bp = Blueprint('main', __name__)


@bp.route('main')
def main():
    return render_template('index.html')