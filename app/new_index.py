<!-- extend base layout -->
{% extends "base.html" %}

{% block content %}
    <h1>Hi, {{ user.userid }}!</h1>
    {# Following for loop prints posts.# }
    {% for post in posts %}
    <div id="posts">
    	<p>
      		Post:{{ post.author.userid }} says: <b>{{ post.posttext }}</b>
    	</p>
    </div>
    	{# Following for loop prints comments on the posts.# }
    	{% for post_comment in post_comments %}
    	<div id="post_comments">
    		{% if post.id == post_comments.post_comments.id %}<p>Answer:{{ post_comment.postcommenttext }}</p>{% endif %}
    	</div>
    	{% endfor %}

    	{# Following for loop prints answer for the post.# }
    	{% for answer in answers %}
    	<div id="post_answers">
    		{% if post.id == answer.answer.id %}<p>Answer:{{ answer.answertext }}</p>{% endif %}
    	</div>
    	{% endfor %}
    {% endfor %}
{% endblock %}