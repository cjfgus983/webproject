from datetime import datetime

from flask import Blueprint, render_template, request, url_for, g, flash
from werkzeug.utils import redirect
from sqlalchemy import func

from .. import db
from ..forms import QuestionForm, AnswerForm, memoForm
from ..models import Question, Answer, User, question_voter, memo_Question
from ..views.auth_views import login_required

bp = Blueprint('memo', __name__, url_prefix='/memo')


@bp.route('/memolist/',methods=('GET', 'POST'))
def _list():
    page=request.args.get('page', type=int, default = 1)
    form = memoForm()
    memo_list = memo_Question.query.order_by(memo_Question.memo_create_date.desc())
    memo_list = memo_list.paginate(page,per_page=11)
    return render_template('memo/memo.html',memo_list=memo_list, form=form)

@bp.route('/detail/<int:memo_id>/')
def detail(memo_id):
    memo = memo_Question.query.get_or_404(memo_id)
    return render_template('memo/memo_detail.html',memo=memo)

@bp.route('/create/', methods=('POST','GET'))
@login_required
def create():
    form = memoForm()
    content=request.form['content']
    memo=memo_Question(content=content, memo_create_date=datetime.now(), user=g.user)
    db.session.add(memo)
    db.session.commit()
    return redirect(url_for('memo._list'))



@bp.route('/modify/<int:question_id>', methods=('GET', 'POST'))
@login_required
def modify(question_id):
    question = Question.query.get_or_404(question_id)
    if g.user != question.user:
        flash('수정권한이 없습니다')
        return redirect(url_for('question.detail', question_id=question_id))
    if request.method == 'POST':
        form = QuestionForm()
        if form.validate_on_submit():
            form.populate_obj(question)
            question.modify_date = datetime.now()  # 수정일시 저장
            db.session.commit()
            return redirect(url_for('question.detail', question_id=question_id))
    else:
        form = QuestionForm(obj=question)
    return render_template('question/question_form.html', form=form)


@bp.route('/delete/<int:question_id>')
@login_required
def delete(question_id):
    question = Question.query.get_or_404(question_id)
    if g.user != question.user:
        flash('삭제권한이 없습니다')
        return redirect(url_for('question.detail', question_id=question_id))
    db.session.delete(question)
    db.session.commit()
    return redirect(url_for('question._list'))

import os
from flask import send_from_directory

@bp.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),
                               'favicon.ico', mimetype='image/vnd.microsoft.icon')