from app import models

class Queries():
	def get_n_comans(self, post):
		if type(post) is models.Post:
			#returns number of comments on post.
			n_answers = models.Post_Comments.query.filter_by(post_id = post.id).count()
			return n_answers
		elif type(post) is models.Answers:
			#returns number of comments on answer
			n_answers = models.Answer_Comments.query.filter_by(answer_id = post.id).count()
			return n_answers
		else:
			#returns number of answers on post.
			n_answers = models.Answers.query.filter_by(post_id = post.id).count()
			return n_answers