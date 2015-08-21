from flask.ext.wtf import Form
from wtforms import StringField, BooleanField, PasswordField, TextAreaField, HiddenField
from wtforms.fields.html5 import EmailField
from wtforms.validators import DataRequired, Email, Length
from app.models import User

class LoginForm(Form):
    userid = StringField('userid', validators=[DataRequired()])
    password = PasswordField('password', validators=[DataRequired()])
    remember_me = BooleanField('remember_me', default=False)

class CreateAccountForm(Form):
    userid = StringField('userid', validators=[DataRequired()])
    password = PasswordField('password', validators=[DataRequired()])
    emailid = EmailField('emailid', validators=[DataRequired()])
    remember_me = BooleanField('remember_me', default=False)

class CreatePostForm(Form):
    posttext = TextAreaField('posttext', validators=[DataRequired()])

class AnswerPostForm(Form):
    answertext = TextAreaField('answertext', validators=[DataRequired()])

class PostCommentForm(Form):
    postcommenttext = TextAreaField('postcommenttext', validators=[DataRequired()])

class AnswerCommentForm(Form):
    answercommenttext = TextAreaField('answercommenttext', validators=[DataRequired()])

class test(Form):
    post_id = StringField('post_id', validators=[DataRequired()])
    answer_id = StringField('answer_id', validators=[DataRequired()]) 
    answercommenttext = TextAreaField('answercommenttext', validators=[DataRequired()])
    timestamp = StringField('timestamp', validators=[DataRequired()])

class EditForm(Form):
    nickname = StringField('nickname', validators=[DataRequired()])
    about_me = TextAreaField('about_me', validators=[Length(min=0, max=140)])

    def __init__(self, original_nickname, *args, **kwargs):
        Form.__init__(self, *args, **kwargs)
        self.original_nickname = original_nickname

    def validate(self):
        if not Form.validate(self):
            return False
        if self.nickname.data == self.original_nickname:
            return True
        user = User.query.filter_by(nickname=self.nickname.data).first()
        if user != None:
            self.nickname.errors.append('This nickname is already in use. Please choose another one.')
            return False
        return True