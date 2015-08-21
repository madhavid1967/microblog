from app import db
from hashlib import md5

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nickname = db.Column(db.String(64), index=True, unique=False)
    userid = db.Column(db.String(64), index=True, unique=True)
    password = db.Column(db.String(64), index=True, unique=False)
    emailid = db.Column(db.String(120), index=True, unique=True)
    posts = db.relationship('Post', backref='author', lazy='dynamic')
    answers = db.relationship('Answers', backref='author_answer', lazy='dynamic')
    post_comments_userid = db.relationship('Post_Comments', backref='post_comment_userid', lazy='dynamic')
    answer_comments_userid = db.relationship('Answers_Comments', backref='answer_comment_userid', lazy='dynamic')
    about_me = db.Column(db.String(140))
    last_seen = db.Column(db.DateTime)
    #Added following social_id column for facebook and twitter login.
    #social_id = db.Column(db.String(64),  unique=False)

    #Added following social_id parameter for facebook and twitter login.
    def __init__(self, userid, password, emailid, nickname):
    	self.userid = userid
    	self.password = password
    	self.emailid = emailid
    	self.nickname = nickname
        #Added following social_id column for facebook and twitter login.
        #self.social_id = social_id

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return unicode(self.id)

    def __repr__(self):
        return '<User %r>' % (self.userid)


    def avatar(self, size):
        return 'http://www.gravatar.com/avatar/%s?d=mm&s=%d' % (md5(self.emailid.encode('utf-8')).hexdigest(), size)
        
class Post(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    posttext = db.Column(db.String(140))
    timestamp = db.Column(db.DateTime)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    answers = db.relationship('Post_Comments', backref='post_comments', lazy='dynamic')

    def __init__(self, userid, posttext, timestamp):
    	self.author = userid
    	self.posttext = posttext
    	self.timestamp = timestamp

    def __repr__(self):
        return '<Post %r>' % (self.body)

class Answers(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    answertext = db.Column(db.String(140))
    timestamp = db.Column(db.DateTime)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'), nullable=False)
    answer_comments = db.relationship('Answers_Comments', backref='answer_comments', lazy='dynamic')

    def __init__(self, userid, post_id, answertext, timestamp):
        self.user_id = userid
        self.answertext = answertext
        self.timestamp = timestamp
        self.post_id = post_id

    def __repr__(self):
        return '<Answers %r>' % (self.body)

class Post_Comments(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    postcommenttext = db.Column(db.String(140))
    timestamp = db.Column(db.DateTime)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'), nullable=False)

    def __init__(self, userid, post_id, commentext, timestamp):
        self.user_id = userid
        self.commentext = commentext
        self.timestamp = timestamp
        self.post_id = post_id

    def __repr__(self):
        return '<Post_Comments %r>' % (self.body)

class Answer_Comments(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    answercommenttext = db.Column(db.String(140))
    timestamp = db.Column(db.DateTime)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'), nullable=False)
    answer_id = db.Column(db.Integer, db.ForeignKey('answer.id'), nullable=False)

    def __init__(self, userid, post_id, answer_id, answercommenttext, timestamp):
        self.user_id = userid
        self.answercommenttext = answercommenttext
        self.timestamp = timestamp
        self.post_id = post_id
        self.user_id = user_id
        self.answer_id = answer_id

    def __repr__(self):
        return '<Answers_Comments %r>' % (self.body)