from datetime import datetime
from flask import Blueprint, url_for, request, render_template, g, flash
from werkzeug.utils import redirect
from pybo import db
from ..forms import AnswerForm
from pybo.models import Gomin, Gomin_Answer
from .auth_views import login_required

bp = Blueprint('gomin_answer',__name__,url_prefix='/gomin_answer')

@bp.route('/create/<int:gomin_id>',methods=('POST',))
@login_required
def create(gomin_id):
    form = AnswerForm()
    gomin = Gomin.query.get_or_404(gomin_id)
    if form.validate_on_submit():
        content = request.form['content']
        gomin_answer = Gomin_Answer(content=content, create_date=datetime.now(), user=g.user)
        gomin.gomin_answer_set.append(gomin_answer)
        db.session.commit()
        return redirect(url_for('gomin.detail', gomin_id=gomin_id))
    return render_template('gomin/gomin_detail.html', gomin=gomin, form=form)
    gomin = Gomin.query.get_or_404(gomin_id)
    content = request.form['content']
    gomin_answer = Gomin_Answer(content=content, create_date=datetime.now(), user=g.user)
    gomin.gomin_answer_set.append(gomin_answer)
    db.session.commit()
    return redirect(url_for('gomin.detail',gomin_id=gomin_id))

@bp.route('/modify/<int:answer_id>', methods=('GET','POST'))
@login_required
def modify(answer_id):
    answer = Answer.query.get_or_404(answer_id)
    if g.user != answer.user:
        flash('수정권한이 없습니다')
        return redirect(url_for('question.detail', question_id=answer.question.id))
    if request.method == "POST":
        form = AnswerForm()
        if form.validate_on_submit():
            form.populate_obj(answer)
            answer.modify_date = datetime.now()
            db.session.commit()
            return redirect(url_for('question.detail', question_id=answer.question.id))
    else:
        form = AnswerForm(obj=answer)
        return render_template('answer/answer_form.html', answer=answer, form=form)

@bp.route('/delete/<int:answer_id>')
@login_required
def delete(answer_id):
    answer = Answer.query.get_or_404(answer_id)
    question_id = answer.question.id
    if g.user != answer.user:
        flash('삭제권한이 없습니니다')
    else:
        db.session.delete(answer)
        db.session.commit()
    return redirect(url_for('question.detail', question_id=question_id))