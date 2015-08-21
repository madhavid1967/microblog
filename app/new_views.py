@app.route('/answer_comment/<post_id>', methods=['GET', 'POST'])
@login_required
def answer_comment(post_id):
    form = AnswerCommentForm()
    if request.method =='POST':
        if form.validate_on_submit():
            post_id = post_id
            answertext = form.answertext.data
            timestamp = datetime.utcnow()
            newanswer = models.Answers(current_user.id, post_id, answertext, timestamp)
            db.session.add(newanswer)
            db.session.commit()
            flash('New answer by %s' % (current_user.userid))
            return redirect(url_for('index'))
    else:
        form.post_id.data = post_id
    return render_template('answer_comment.html',title='Answer a post.',form=form)

@app.route('/post_comment/<post_id>', methods=['GET', 'POST'])
@login_required
def post_comment(post_id):
    form = PostCommentForm()
    if request.method =='POST':
        if form.validate_on_submit():
            post_id = post_id
            postcommenttext = form.postcommenttext.data
            timestamp = datetime.utcnow()
            newanswer = models.Answers(current_user.id, post_id, postcommenttext, timestamp)
            db.session.add(newanswer)
            db.session.commit()
            flash('New answer by %s' % (current_user.userid))
            return redirect(url_for('index'))
    else:
        form.post_id.data = post_id
    return render_template('answer_comment.html',title='Answer a post.',form=form)