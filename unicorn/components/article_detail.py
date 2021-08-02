from django_unicorn.components import UnicornView

from core.models import Article, ArticleComment, ArticleVote
from django.shortcuts import get_object_or_404
from django_unicorn.db import DbModel
from django.contrib.auth import get_user_model

User = get_user_model()

class ArticleDetailView(UnicornView):
    comment_message = None
    vote = None
    article = None
    comment = None

    class Meta:
        db_models = [DbModel("article", ArticleComment), DbModel('vote', ArticleVote), DbModel('article.author', User)]

    def __init__(self, article_id, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        self.article = get_object_or_404(Article, is_draft=False, pk=int(article_id))
        if self.request.user.is_authenticated:
            vote = self.article.votes.filter(author=self.request.user)
            if vote.exists():
                self.vote = vote.first()
            else:
                self.vote = ArticleVote(article=self.article, author=self.request.user)
            self.comment = ArticleComment(article=self.article, author=self.request.user)

    

    def save(self):
        assert self.comment
        assert self.comment.content
        self.comment.save()
        self.comment = ArticleComment(article=self.article, author=self.request.user )
    
    def cast_vote(self, vote):
        vote = int(vote)
        assert vote in [1, -1]
        assert self.vote
        if int(vote) == 1:
            self.vote.vote = 1
        elif int(vote) == -1:
            self.vote.vote = -1
        self.vote.save()

    
    