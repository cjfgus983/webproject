from flask import Blueprint, url_for, render_template
from werkzeug.utils import redirect

from pybo.models import Question

import os
from flask import send_from_directory

from datetime import datetime

from flask import Blueprint, render_template, request, url_for, g, flash
from werkzeug.utils import redirect
from sqlalchemy import func

from .. import db
from ..forms import QuestionForm, AnswerForm, memoForm
from ..models import Question, Answer, User, question_voter, memo_Question, Gomin
from ..views.auth_views import login_required


bp = Blueprint('main',__name__,url_prefix='/')
@bp.route('/hello')
def hello_pybo():
    return 'Hello, Pybo!'

@bp.route('/')
def index():
    page = request.args.get('page', type=int, default=1)
    kw = request.args.get('kw', type=str, default='')
    so = request.args.get('so', type=str, default='recent')

    # 정렬
    if so == 'recommend':
        sub_query = db.session.query(question_voter.c.question_id, func.count('*').label('num_voter')) \
            .group_by(question_voter.c.question_id).subquery()
        question_list = Question.query \
            .outerjoin(sub_query, Question.id == sub_query.c.question_id) \
            .order_by(sub_query.c.num_voter.desc(), Question.create_date.desc())
    elif so == 'popular':
        sub_query = db.session.query(Answer.question_id, func.count('*').label('num_answer')) \
            .group_by(Answer.question_id).subquery()
        question_list = Question.query \
            .outerjoin(sub_query, Question.id == sub_query.c.question_id) \
            .order_by(sub_query.c.num_answer.desc(), Question.create_date.desc())
    else:  # recent
        question_list = Question.query.order_by(Question.create_date.desc())

    # 조회
    if kw:
        search = '%%{}%%'.format(kw)
        sub_query = db.session.query(Answer.question_id, Answer.content, User.username) \
            .join(User, Answer.user_id == User.id).subquery()
        question_list = question_list \
            .join(User) \
            .outerjoin(sub_query, sub_query.c.question_id == Question.id) \
            .filter(Question.subject.ilike(search) |  # 질문제목
                    Question.content.ilike(search) |  # 질문내용
                    User.username.ilike(search) |  # 질문작성자
                    sub_query.c.content.ilike(search) |  # 답변내용
                    sub_query.c.username.ilike(search)  # 답변작성자
                    ) \
            .distinct()

    # 페이징
    question_list = question_list.paginate(page, per_page=5)
    #==========================================================메모
    page = request.args.get('page', type=int, default=1)
    form = memoForm()
    memo_list = memo_Question.query.order_by(memo_Question.memo_create_date.desc())
    memo_list = memo_list.paginate(page, per_page=5)
    #===========================================================고민
    page = request.args.get('page', type=int, default=1)
    kw = request.args.get('kw', type=str, default='')
    so = request.args.get('so', type=str, default='recent')

    # 정렬
    if so == 'recommend':
        sub_query = db.session.query(gomin_voter.c.gomin_id, func.count('*').label('num_voter')) \
            .group_by(gomin_voter.c.gomin_id).subquery()
        gomin_list = Gomin.query \
            .outerjoin(sub_query, Gomin.id == sub_query.c.gomin_id) \
            .order_by(sub_query.c.num_voter.desc(), Gomin.create_date.desc())
    elif so == 'popular':
        sub_query = db.session.query(Gomin_Answer.gomin_id, func.count('*').label('num_answer')) \
            .group_by(Gomin_Answer.gomin_id).subquery()
        gomin_list = Gomin.query \
            .outerjoin(sub_query, Gomin.id == sub_query.c.gomin_id) \
            .order_by(sub_query.c.num_answer.desc(), Gomin.create_date.desc())
    else:  # recent
        gomin_list = Gomin.query.order_by(Gomin.create_date.desc())

    # 조회
    if kw:
        search = '%%{}%%'.format(kw)
        sub_query = db.session.query(Gomin_Answer.gomin_id, Gomin_Answer.content, User.username) \
            .join(User, Gomin_Answer.user_id == User.id).subquery()
        gomin_list = gomin_list \
            .join(User) \
            .outerjoin(sub_query, sub_query.c.gomin_id == Gomin.id) \
            .filter(Gomin.subject.ilike(search) |  # 질문제목
                    Gomin.content.ilike(search) |  # 질문내용
                    User.username.ilike(search) |  # 질문작성자
                    sub_query.c.content.ilike(search) |  # 답변내용
                    sub_query.c.username.ilike(search)  # 답변작성자
                    ) \
            .distinct()

    # 페이징
    gomin_list = gomin_list.paginate(page, per_page=5)
    return render_template('mainpage/mainpage.html', question_list=question_list, memo_list=memo_list, gomin_list=gomin_list)



@bp.route('/introduce')
def introduce():
    return render_template('category/introduce.html')

@bp.route('/call')
def call():
    return render_template('category/call.html')

@bp.route('/alert')
def alert():
    return render_template('category/alert.html')

@bp.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),
                               'favicon.ico', mimetype='image/vnd.microsoft.icon')

