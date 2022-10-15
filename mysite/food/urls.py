from . import views
from django.urls import path,reverse_lazy
from django.conf.urls.static import static
from django.conf import settings

app_name = 'food'
urlpatterns = [
    path('', views.index_class_view.as_view(),name='index'),
    path('<int:pk>/', views.FoodDetail.as_view(), name='detail'),
   
    path('add/', views.CreateItem.as_view(), name='create_item'),
    path('update/<int:pk>/', views.UpdateItem.as_view(), name='update_item'),
    path('delete/<int:pk>/', views.ItemDeleteView.as_view(), name='delete_item'),
    path('<int:pk>/comment/', views.CommentCreateView.as_view(), name='comment_create'),
    path('comment/<int:pk>/delete', views.CommentDeleteView.as_view(success_url=reverse_lazy('detail')), name='comment_delete'),
    path('like/<int:pk>/', views.LikeView, name='like_item'),
    path('searched_item/', views.SearchView, name='searched_item'),
]

urlpatterns += [
    # ... the rest of your URLconf goes here ...
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)