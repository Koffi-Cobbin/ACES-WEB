from django.db.models.query import QuerySet
from django_unicorn.components import UnicornView, QuerySetType
from django.db.models import Q


from core.models import Article, ArticleCategory


class ArticleListView(UnicornView):
    article_categories: QuerySetType[ArticleCategory] = ArticleCategory.objects.none()
    search_query = ''
    selected_category = None
    articles: QuerySetType[Article] = Article.objects.none()

    def mount(self, *args, **kwargs):
        self.get_articles()

    def get_articles(self):
        articles = Article.objects.filter(is_draft=False)
        if self.search_query:
            articles = articles.filter(Q(title__contains=self.search_query)|Q(content__icontains=self.search_query))
        if self.selected_category:
            articles = articles.filter(categories=self.selected_category)
        self.articles = articles
        return self.articles

    def set_selected_category_with_pk(self, pk):
        
        self.selected_category = ArticleCategory.objects.get(pk=pk)
        self.get_articles()

    def updated_search_query(self, *args, **kwargs):
        self.get_articles()
