from timeit import default_timer

from django.contrib.auth.models import Group
from django.http import HttpRequest
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.shortcuts import redirect
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import View
from django.views import generic

from .forms import GroupForm
from .models import Order
from .models import Product


class ShopIndexView(View):
    def get(self, request: HttpRequest) -> HttpResponse:
        products = [
            ('Laptop', 1999),
            ('Desktop', 2999),
            ('Smartphone', 999),
        ]
        print(products)
        context = {
            "time_running": default_timer(),
            "products": products,
        }
        
        return render(request, 'shopapp/shop-index.html', context=context)


class GroupsListView(View):
    def get(self, request: HttpRequest) -> HttpResponse:
        context = {
            "form": GroupForm(),
            "groups": Group.objects.prefetch_related('permissions').all(),
        }
        return render(request, 'shopapp/groups-list.html', context=context)
    
    def post(self, request: HttpRequest):
        form = GroupForm(request.POST)
        if form.is_valid():
            form.save()
        return redirect(request.path)


class ProductDetailView(generic.DetailView):
    template_name = 'shopapp/products-details.html'
    model = Product
    context_object_name = 'product'


class ProductListView(generic.ListView):
    template_name = 'shopapp/products-list.html'
    # model = Product
    context_object_name = 'products'
    queryset = Product.objects.filter(archived=False)


class OrdersListView(generic.ListView):
    queryset = (
        Order.objects.select_related("user").prefetch_related("products")
    )


class OrdersDetailView(generic.DetailView):
    queryset = (
        Order.objects.select_related("user").prefetch_related("products")
    )


class ProductCreateView(generic.CreateView):
    model = Product
    fields = ('name', 'price', 'description', 'discount')
    success_url = reverse_lazy('shopapp:products_list')


class OrderCreateView(generic.CreateView):
    model = Order
    fields = ('delivery_address', 'promocode', 'user', 'products')
    success_url = reverse_lazy('shopapp:orders_list')


class ProductUpdateView(generic.UpdateView):
    model = Product
    fields = ('name', 'price', 'description', 'discount')
    template_name_suffix = "_update_form"
    
    def get_success_url(self, **kwargs):
        return reverse_lazy("shopapp:products_details", kwargs={
            'pk': self.object.pk
        })


class OrderUpdateView(generic.UpdateView):
    model = Order
    fields = ('delivery_address', 'promocode', 'user', 'products')
    template_name_suffix = "_update_form"
    
    def get_success_url(self, **kwargs):
        return reverse_lazy("shopapp:orders_details", kwargs={
            'pk': self.object.pk
        })


class ProductDeleteView(generic.DeleteView):
    model = Product
    success_url = reverse_lazy('shopapp:products_list')
    
    def form_valid(self, form):
        success_url = self.get_success_url()
        # self.object.delete()
        self.object.archived = True
        self.object.save()
        return HttpResponseRedirect(success_url)


class OrderDeleteView(generic.DeleteView):
    model = Order
    success_url = reverse_lazy('shopapp:orders_list')
    
    # def form_valid(self, form):
    #     success_url = self.get_success_url()
    #     # self.object.delete()
    #     self.object.archived = True
    #     self.object.save()
    #     return HttpResponseRedirect(success_url)
