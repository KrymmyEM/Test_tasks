from django.urls import path
from test_site import views

urlpattern_site = [
    path("buy/<int:id>/", views.BuyView.as_view()),
    path("item/<int:id>/", views.ItemView.as_view()),
]