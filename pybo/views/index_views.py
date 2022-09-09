from datetime import datetime

from flask import Blueprint, render_template, request, url_for, g, flash
from werkzeug.utils import redirect
from sqlalchemy import func

from .. import db
from ..forms import QuestionForm, AnswerForm
from ..models import Question, Answer, User, question_voter
from ..views.auth_views import login_required

bp = Blueprint('index', __name__, url_prefix='/index')

@bp.route('/index/')
def _mainpage():
    return render_template('mainpage/mainpage.html')