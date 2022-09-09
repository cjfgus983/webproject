from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, PasswordField
from wtforms.fields import EmailField
# wtforms.fields.html5 말고 wtforms.fields 로
from wtforms.validators import DataRequired, Length, EqualTo, Email

class QuestionForm(FlaskForm):
    subject = StringField('제목',validators=[DataRequired('제목을 입력해주세요')])
    content = TextAreaField('내용',validators=[DataRequired('내용을 입력해주세요')])

class AnswerForm(FlaskForm):
    content = TextAreaField('내용',validators=[DataRequired('내용을 입력해주세요')])

class UserCreateForm(FlaskForm):
    username = StringField('사용자이름', validators=[DataRequired(), Length(min=3,max=25)])
    password1= PasswordField('비밀번호', validators=[DataRequired(), EqualTo('password2','비밀번호가 일치하지 않습니다')])
    password2 = PasswordField('비밀번호확인', validators=[DataRequired()])
    email = EmailField('이메일', [DataRequired(),Email()])
    mbti = StringField('엠비티아이', validators=[DataRequired(), Length(min=3, max=25)])

class UserLoginForm(FlaskForm):
    username = StringField('사용자이름', validators=[DataRequired(), Length(min=3, max=25)])
    password = PasswordField('비밀번호', validators=[DataRequired()])

class CommentForm(FlaskForm):
    content = TextAreaField('내용', validators=[DataRequired()])

class memoForm(FlaskForm):
    content = TextAreaField('내용', validators=[DataRequired('내용을 입력해주세요')])

class GominForm(FlaskForm):
    subject = StringField('제목',validators=[DataRequired('제목을 입력해주세요')])
    content = TextAreaField('내용',validators=[DataRequired('내용을 입력해주세요')])

class Gomin_AnswerForm(FlaskForm):
    content = TextAreaField('내용',validators=[DataRequired('내용을 입력해주세요')])