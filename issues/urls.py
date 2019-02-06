from django.urls import path

from . import views

urlpatterns = [
    path('homepage/', views.homepage, name='homepage'),
    path('repositories/', views.RepositoryListView.as_view(), name='repositories'),
    path('repositories/import', views.sync_repositories, name='repositories_import'),
    path('repositories/<slug:pk>', views.RepositoryView.as_view(), name='repositories_issues'),
    path('repositories/issues/<slug:pk>', views.sync_issues, name='issues_update'),
]

