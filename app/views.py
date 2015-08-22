from flask import render_template, flash, redirect, url_for, request, g, session
from app import app, models, db
from app import queries as q
from flask.ext.login import login_user, logout_user, current_user, login_required
from .forms import LoginForm, CreateAccountForm, CreatePostForm, AnswerPostForm, PostCommentForm, AnswerCommentForm, test
from datetime import datetime
from forms import LoginForm, EditForm
from .oauth import OAuthSignIn

@app.route('/')
@app.route('/index')
@login_required
def index():
    user = current_user
    posts = models.Post.query.all()
    index_posts = get_index_posts(posts)
    #answers = models.Answers.query.all()
    #post_comments = models.Post_Comments.query.all()
    #answer_comments = models.Answer_Comments.query.all()
    return render_template('index.html',title='Home',user=user,posts=index_posts)

def get_index_posts(posts):
    index_posts = []
    for p in posts:
        post_text = p.posttext
        user_name = p.ref_user_post.nickname
        top_answer = models.Answers.query.filter_by(post_id = p.id).first()
        n_comments = q.Queries().get_n_comans(p)
        n_answers = q.Queries().get_n_comans(p)
        user_avatar = p.ref_user_post.avatar(25)
        post_id = p.id

        date = p.timestamp
        post = {'Post Id' : post_id,
                'Post Text':post_text,
                'User Name':user_name,
                'Top Answer':top_answer,
                'NComments':n_comments,
                'NAnswers': n_answers,
                'Date':date,
                'User Avatar': user_avatar}

        index_posts.append(post)
    return index_posts

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    error = None
    if form.validate_on_submit():
        if request.method == 'POST':
    	   user = models.User.query.filter_by(userid=form.userid.data).first()
    	if user is not None and user.password == form.password.data:
        	login_user(user)
        	return redirect(url_for('index'))
    else:
    	error='Your userid/password is incorrect.'
    return render_template('login.html', 
                           title='Sign In',
                           form=form)

@app.route('/logout')
@login_required
def logout():
	logout_user()
	flash('Goodbye!')
	return redirect(url_for('login'))

@app.route('/account', methods=['GET', 'POST'])
def create_account():
    form = CreateAccountForm()
    if request.method =='POST'and form.validate_on_submit():
        userid = form.userid.data
    	password = form.password.data
    	emailid = form.emailid.data
    	nickname = form.emailid.data
        #Added following social_id column for facebook and twitter login.
        #social_id = form.userid.data
    	#newuser = models.User(userid, password, emailid, nickname, social_id)
        newuser = models.User(userid, password, emailid, nickname)
    	db.session.add(newuser)
        db.session.commit()
        flash('Account Created for %s' % (userid))
        return redirect(url_for('login'))

    return render_template('account.html', 
                           title='Create an Account',
                           form=form)

@app.route('/user/<userid>')
@login_required
def user(userid):
    user = models.User.query.filter_by(userid=userid).first()
    if user == None:
        flash('User %s not found.' % userid)
        return redirect(url_for('index'))
    posts = [
        {'author': user, 'body': 'Test post #1'},
        {'author': user, 'body': 'Test post #2'}
    ]
    return render_template('user.html',
                           user=user,
                           posts=posts)
@app.before_request
def before_request():
    g.user = current_user
    if g.user.is_authenticated():
        g.user.last_seen = datetime.utcnow()
        db.session.add(g.user)
        db.session.commit()

@app.route('/edit', methods=['GET', 'POST'])
@login_required
def edit():
    form = EditForm(g.user.nickname)
    if form.validate_on_submit():
        g.user.nickname = form.nickname.data
        g.user.about_me = form.about_me.data
        db.session.add(g.user)
        db.session.commit()
        flash('Your changes have been saved.')
        return redirect(url_for('edit'))
    else:
        form.nickname.data = g.user.nickname
        form.about_me.data = g.user.about_me
    return render_template('edit.html', form=form)


@app.route('/create_post', methods=['GET', 'POST'])
@login_required
def create_post():
    form = CreatePostForm()
    if request.method =='POST'and form.validate_on_submit():
        posttext = form.posttext.data
        timestamp = datetime.utcnow()
        user = current_user
        newpost = models.Post(user, posttext, timestamp)
        db.session.add(newpost)
        db.session.commit()
        flash('New post by %s' % (user.userid))
        return redirect(url_for('index'))
    return render_template('create_post.html',title='Create a new post.',form=form)

@app.route('/session_creater/<post_type>&<pid>')
@login_required
def session_creater(post_type, pid):
    if(int(post_type) == 0):
        #answer_post
        session['post_id']=pid
        return redirect(url_for('answer_post'))
    elif(int(post_type) == 1):
        #comment_on_post
        session['post_id']=pid
        return redirect(url_for('comment_on_post'))
    #else:
        #comment_on_answer
        #session['answer_id']=pid
        #flash('answer_id %s' % (session['answer_id']))
        #return redirect(url_for('comment_on_answer'))
    elif(int(post_type) == 2):
        #comment_on_answer
        session['answer_id']=pid
        #flash('answer_id %s' % (session['answer_id']))
        return redirect(url_for('comment_on_answer'))
    else:
        session['post_id'] = pid
        return redirect(url_for('show_all_answers'))

@app.route('/show_all_answers')
@login_required
def show_all_answers():
    user_name = current_user
    post_id = session['post_id']
    posttext = models.Post.query.filter_by(id=int(post_id)).first()
    all_answers = models.Answers.query.filter_by(id=int(post_id)).all()
    show_all_answers = []
    for a in all_answers:
        comment_cnt = models.Answer_Comments.query.filter_by(id=a.id).count()
        answertext = a.answertext
        date = a.timestamp
        user_name = a.ref_user_answer.nickname
        user_avatar = a.ref_user_answer.avatar(25)
        answer = {'Comment Count' : comment_cnt,
                'Answer Text':answertext,
                'User Name':user_name,
                'Date':date,
                'User Avatar': user_avatar}

        show_all_answers.append(answer)
    return render_template('show_all_answers.html',title='All Answers on post.',answers=show_all_answers,postid=post_id,posttext=posttext)

@app.route('/answer_post/', methods=['GET', 'POST'])
@login_required
def answer_post():
    form = AnswerPostForm()    
    post_id = session['post_id']
    user = current_user
    post = models.Post.query.filter_by(id=int(post_id)).first()
    if request.method =='POST':
        if form.validate_on_submit():
            answertext = form.answertext.data
            timestamp = datetime.utcnow()
            newanswer = models.Answers(user, post, answertext, timestamp)
            db.session.add(newanswer)
            db.session.commit()
            flash('New answer by %s' % (user.userid))
            return redirect(url_for('index'))
    return render_template('answer_post.html',title='Answer a post.',form=form)
    
@app.route('/post_comment/', methods=['GET', 'POST'])
@login_required
def comment_on_post():
    form = PostCommentForm()
    post_id = session['post_id']
    user = current_user
    post = models.Post.query.filter_by(id=int(post_id)).first()
    if request.method =='POST':
        if form.validate_on_submit():
            postcommenttext = form.postcommenttext.data
            timestamp = datetime.utcnow()
            postcomment = models.Post_Comments(user, post, postcommenttext, timestamp)
            db.session.add(postcomment)
            db.session.commit()
            flash('New answer by %s' % (user.userid))
            return redirect(url_for('index'))
    return render_template('comment_on_post.html',title='Answer a post.',form=form)

@app.route('/comment_on_answer/', methods=['GET', 'POST'])
@login_required
def comment_on_answer():
    form = AnswerCommentForm()
    post_id = session['post_id']
    answer_id = session['answer_id']
    user = current_user
    if request.method =='POST':
        if form.validate_on_submit():
            answer = models.Answers.query.filter_by(id=int(answer_id)).first()
            answercommenttext = form.answercommenttext.data
            timestamp = datetime.utcnow()            
            answercomment = models.Answer_Comments(user, answer, answercommenttext, timestamp)
            db.session.add(answercomment)
            db.session.commit()
            flash('New comment on answer by %s' % (user.userid))
            return redirect(url_for('index'))
    return render_template('comment_on_answer.html',title='Comment on Answer.',form=form)