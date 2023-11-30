from django.urls import path
from test_site import views

urlpattern_site = [
    path("buy/<int:id>/", views.ItemOrderView.as_view()),
    path("add/<int:id>/", views.AddItemView.as_view()),
    path("item/<int:id>/", views.ItemView.as_view()),
]