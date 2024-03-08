from flask import Blueprint, render_template
from flask_login import login_required, current_user
from website.choices import encoded_choices

views = Blueprint('views', __name__)

@views.route('/')
@login_required
def home():
    return render_template("home.html", user=current_user)


@views.route('/get-started')
@login_required
def get_started():
    return render_template("get_started.html", user=current_user, encoded_choices=encoded_choices)
