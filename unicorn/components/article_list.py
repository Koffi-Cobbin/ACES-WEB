from django_unicorn.components import UnicornView
from django.db.models import Q


from core.models import Article, ArticleCategory


class ArticleListView(UnicornView):
    article_categories = ArticleCategory.objects.all()
    search_query = ''
    selected_category = None
    articles = None

    def mount(self, *args, **kwargs):
        self.get_articles()

    def get_articles(self):
        articles = Article.objects.filter(is_draft=False)
        if self.search_query:
            articles = articles.filter(Q(title__icontains=self.search_query)|Q(content__icontains=self.search_query)) 
        if self.selected_category:
            articles = articles.filter(categories=self.selected_category)
        self.articles = articles


    
    def updated_selected_category(self, *args, **kwargs):
        self.get_articles()
    
    def set_selected_category_with_pk(self, pk):
        
        self.selected_category = ArticleCategory.objects.get(pk=pk)

    def updated_search_query(self, *args, **kwargs):
        self.get_articles()
