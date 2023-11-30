from django.shortcuts import render
from django.views import View
from django.views.generic import TemplateView
from django.http import JsonResponse, HttpResponse


class BuyView(View):
    def get(self, request, id: int) -> JsonResponse:
        ...

class ItemView(TemplateView):
    template_name = "item.html"
    def get_context_data(self, id: int, **kwargs):
        context = super().get_context_data(**kwargs)
        context["message"] = id
        return context