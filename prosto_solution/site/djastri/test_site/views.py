import json

from django.shortcuts import render
from django.views import View
from django.views.generic import TemplateView
from django.http import JsonResponse, HttpResponse, HttpRequest
from django.conf import settings
import stripe

from test_site.models import Item, Order, OrderItem

def error404Json(request, message) -> JsonResponse:
    respons = JsonResponse({"status": "Error"})
    response.status_code = 404
    response.content = json.dumps({"status": "Error", "message": message})
    return responses

def error404Http(message) -> HttpResponse:
    response = HttpResponse()
    response.status_code = 404
    response.content = "Error404: " +message
    return response


def check_and_create_order(request: HttpRequest) -> dict:
    uuid_c = request.COOKIES.get("orduuid", None)
    order, created = Order.objects.get_or_create(uuid=uuid_c)
    if created:
        order.save()
    if order.in_work:
        order = Order.objects.create()
        order.save()

    return {"orduuid": order.uuid}


class MakeOrderView(View):
    def get(self, request) -> JsonResponse:
        response = JsonResponse({"status": "OK"})
        uuid_order = request.COOKIES.get("orduuid", None)
        if not uuid_order:
            response = error404Json(response, "Order not found")
            return response
        
        order = Order.objects.get(uuid=uuid_order)
        if not order.in_work:
            order.in_work = True
            order.save()
        
        #check order items not empty
        if not order.orderitem_set.all():
            response = error404Json(response, "Order items not found")
            return response
        
        #line_items extend in orderitems from order
        line_items = []
        for order_item in order.orderitem_set.all():
            line_items.append({
                "price": order_item.item.stripe_price_id,
                "quantity": order_item.quantity
            })
        
        #create stripe checkout session
        stripe.api_key = settings.STRIPE_SECRET_KEY
        try:
            checkout_session = stripe.checkout.Session.create(
                line_items = line_items,
                mode = "payment",
                return_url = "http://127.0.0.1:8000/",
                success_url = "http://127.0.0.1:8000/",
                coupon = order.discounts.stripe_coupon_id if order.discounts else None,
                tax_rates = [order.tax.stripe_tax_rate_id] if order.tax else None,
            )
        except Exception as e:
            response.status_code = 500
            response.content = json.dumps({"status": "ServerError", "message": str(e)})
            return response

        order.stripe_checkout_session_id = checkout_session["id"]
        order.save()
        response.content = json.dumps({"status": "OK", "session_id": checkout_session['id']})
        response.set_cookie("orduuid_check", uuid_order)
        return response


class AddItemView(View):
    def post(self, request, id: int) -> JsonResponse:
        response = JsonResponse({"status": "OK"})
        uuid_order = check_and_create_order(request).get("orduuid")
        order = Order.objects.get(uuid=uuid_order)
        item_object = None
        try:
            item_object = Item.objects.get(id=id)
        except Item.DoesNotExist:
            response = error404Json(response, "Item not found")
            return response

        order_item, created = OrderItem.objects.get_or_create(order=order, item=item_object)
        if not created:
            order_item.quantity += 1
        order_item.save()
        response.set_cookie("orduuid", uuid_order)
        response.content = json.dumps({"status": "OK"})
        return response


class ItemOrderView(View):
    def get(self, request, id: int) -> JsonResponse:
        response = JsonResponse({"status": "OK"})
        #make new order and add item
        order = Order.objects.create()
        order.in_work = True
        order.save()
        try:
            item_object = Item.objects.get(id=id)
        except Item.DoesNotExist:
            response = error404Json(response, "Item not found")
            return response

        order_item = OrderItem.objects.create(order=order, item=item_object)
     
        order_item.save()
        #line_items extend in orderitems from order
        line_items = []
        line_items.append({
            "price": item_object.stripe_price_id,
            "quantity": order_item.quantity
        })
        stripe.api_key = settings.SECRET_KEY_STRIPE
        checkout_session = stripe.checkout.Session.create(
            line_items=line_items,
            mode='payment',
            return_url = "http://127.0.0.1:8000/",
            success_url = "http://127.0.0.1:8000/",
            coupon = order.discounts.stripe_coupon_id if order.discounts else None,
            tax_rates = [order.tax.stripe_tax_rate_id] if order.tax else None,
        )
        response.content = json.dumps({"status": "OK", "session_id": checkout_session['id']})
        return response
        


class ItemView(TemplateView):
    template_name = "item.html"

    def get(self, request, id: int) -> HttpResponse:
        context = self.get_context_data(id)
        if context.get("error"):
            return context.get("error")
        return render(request, self.template_name, context) 


    def get_context_data(self, id: int, **kwargs):
        context = super().get_context_data(**kwargs)
        item_object = None
        try:
            item_object = Item.objects.get(id=id)
        except Item.DoesNotExist:
            context['error'] = error404Http("Item not found")

        context["item"] = item_object
        return context