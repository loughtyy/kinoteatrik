from .serializers import ArticleSerializer
from rest_framework import viewsets
from .models import Article
class ArticleViewSet(viewsets.ModelViewSet):
 serializer_class = ArticleSerializer
 queryset = Article.objects.all()


