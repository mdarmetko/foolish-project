from articles import views
from django.urls import path

app_name = 'articles'
urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('articles/<str:headline>', views.ArticleView.as_view(), name='article'),
    path('comments', views.CommentView.as_view())
]
