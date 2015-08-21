from app import db
from hashlib import md5

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nickname = db.Column(db.String(64), index=True, unique=False)
    userid = db.Column(db.String(64), index=True, unique=True)
    password = db.Column(db.String(64), index=True, unique=False)
    emailid = db.Column(db.String(120), index=True, unique=True)
    posts = db.relationship('Post', backref='ref_user_post', lazy='dynamic')
    answers = db.relationship('Answers', backref='ref_user_answer', lazy='dynamic')
    postcomments = db.relationship('Post_Comments', backref='ref_user_comment', lazy='dynamic')
    answercomments = db.relationship('Answer_Comments', backref='ref_user_answercomment', lazy='dynamic')
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
    answers = db.relationship('Answers', backref='ref_post_answer', lazy='dynamic')
    comments = db.relationship('Post_Comments', backref='ref_post_comment', lazy='dynamic')
    #post_anscomments = db.relationship('Post_Comments', backref='ref_post_anscomment', lazy='dynamic')

    def __init__(self, user, posttext, timestamp):
    	self.ref_user_post = user
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
    anscomments = db.relationship('Answer_Comments', backref='ref_ans_anscomment', lazy='dynamic')

    def __init__(self, user, post, answertext, timestamp):
        self.ref_user_answer = user
        self.ref_post_answer = post
        self.answertext = answertext
        self.timestamp = timestamp    
        
    def __repr__(self):
        return '<Answers %r>' % (self.body)

class Post_Comments(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    postcommenttext = db.Column(db.String(140))
    timestamp = db.Column(db.DateTime)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'), nullable=False)

    def __init__(self, user, post, postcommenttext, timestamp):
        self.ref_user_comment = user
        self.postcommenttext = postcommenttext
        self.timestamp = timestamp
        self.ref_post_comment = post

    def __repr__(self):
        return '<Post_Comments %r>' % (self.body)          

class Answer_Comments(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    answercommenttext = db.Column(db.String(140))
    timestamp = db.Column(db.DateTime)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    #post_id = db.Column(db.Integer, db.ForeignKey('post.id'), nullable=False)
    answer_id = db.Column(db.Integer, db.ForeignKey('answers.id'), nullable=False)

    def __init__(self, user, answer, answercommenttext, timestamp):
        self.ref_user_answercomment = user
        self.ref_ans_anscomment = answer
        self.answercommenttext = answercommenttext
        self.timestamp = timestamp
        #self.ref_post_anscomment = post
        
    def __repr__(self):
        return '<Answer_Comments %r>' % (self.body)