from datetime import datetime

from flask import Blueprint, render_template, request, url_for, g, flash
from werkzeug.utils import redirect
from sqlalchemy import func

from .. import db
from ..forms import QuestionForm, AnswerForm, GominForm, Gomin_AnswerForm
from ..models import Question, Answer, User, question_voter, Gomin, Gomin_Answer
from ..views.auth_views import login_required

bp = Blueprint('gomin', __name__, url_prefix='/gomin')


@bp.route('/gominlist/')
def _list():
    # 입력 파라미터
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
    gomin_list = gomin_list.paginate(page, per_page=10)
    return render_template('gomin/gomin_list.html', gomin_list=gomin_list, page=page, kw=kw, so=so)



@bp.route('/detail/<int:gomin_id>/')
def detail(gomin_id):
    form = Gomin_AnswerForm()
    gomin = Gomin.query.get_or_404(gomin_id)
    return render_template('gomin/gomin_detail.html', gomin=gomin, form=form)


@bp.route('/create/', methods=('GET', 'POST'))
@login_required
def create():
    form = GominForm()
    if request.method == 'POST' and form.validate_on_submit():
        gomin = Gomin(subject=form.subject.data, content=form.content.data,
                            create_date=datetime.now(), user=g.user)
        db.session.add(gomin)
        db.session.commit()
        return redirect(url_for('gomin._list'))#제출하면 redirect로 question리스트로 리턴하도록함
    return render_template('gomin/gomin_form.html', form=form)


@bp.route('/modify/<int:gomin_id>', methods=('GET', 'POST'))
@login_required
def modify(gomin_id):
    gomin = Gomin.query.get_or_404(gomin_id)
    if g.user != gomin.user:
        flash('수정권한이 없습니다')
        return redirect(url_for('gomin.detail', gomin_id=gomin_id))
    if request.method == 'POST':
        form = GominForm()
        if form.validate_on_submit():
            form.populate_obj(gomin)
            gomin.modify_date = datetime.now()  # 수정일시 저장
            db.session.commit()
            return redirect(url_for('gomin.detail', gomin_id=gomin_id))
    else:
        form = GominForm(obj=gomin)
    return render_template('gomin/gomin_form.html', form=form)


@bp.route('/delete/<int:gomin_id>')
@login_required
def delete(gomin_id):
    gomin = Gomin.query.get_or_404(gomin_id)
    if g.user != gomin.user:
        flash('삭제권한이 없습니다')
        return redirect(url_for('gomin.detail', gomin_id=gomin_id))
    db.session.delete(gomin)
    db.session.commit()
    return redirect(url_for('gomin._list'))

import os
from flask import send_from_directory
