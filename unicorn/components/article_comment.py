from django_unicorn.components import UnicornView
from core.models import Article, ArticleComment
from django.db.models import QuerySet
from django_unicorn import db
class ArticleCommentView(UnicornView):
    comment: str = ""
    article_id: int = None
    comments: QuerySet[ArticleComment] = ArticleComment.objects.none()

    def __init__(self, article_id, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.article_id = article_id

    def get_comments(self):
        self.comments = self.get_article().comments.all()

    def get_article(self):
        return Article.objects.get(id=self.article_id)

    def mount(self):
        self.get_comments()
        return super().mount()
        
    def save(self):
        if not self.request.user.is_authenticated:
            error_message = "Kindly Login to comment."
        elif len(self.comment) >=1 :
            ArticleComment.objects.create(
                author=self.request.user,
                content=self.comment,
                article = self.get_article()
            )
            self.error_message = ""
            self.comment = ""
        else:
            self.error_message = "A comment must be at least one character long."
        
