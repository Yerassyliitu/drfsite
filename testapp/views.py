from django.db.models import Count, Sum, Q
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.views.generic import DeleteView
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Restaurant, Order, RestaurantImage

from django.contrib.auth.views import LoginView, LogoutView
from .forms import MyAuthenticationForm, RestaurantForm, RestaurantImageForm


class MyLoginView(LoginView):
    template_name = 'testapp/login.html'
    form_class = MyAuthenticationForm


class MyLogoutView(LogoutView):
    http_method_names = ['get']

    def get(self, request, *args, **kwargs):
        super().get(request, *args, **kwargs)
        return redirect('login')

class RestaurantCreateView(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'testapp/add_partner.html'

    def get(self, request):
        form = RestaurantForm()
        images = RestaurantImage.objects.filter(post__isnull=True)
        return Response({'form': form, 'image_form': RestaurantImageForm(), 'images': images})

    def post(self, request):
        form = RestaurantForm(request.POST, request.FILES)
        image_form = RestaurantImageForm(request.POST, request.FILES)
        if form.is_valid():
            restaurant = form.save()
            return Response({'success': True, 'restaurant_id': restaurant.id})
        else:
            # В случае ошибки валидации формы используйте render
            images = RestaurantImage.objects.filter(post__isnull=True)
            return render(request, self.template_name,
                          {'form': form, 'image_form': image_form, 'images': images, 'success': False})


class ImageCreateView(APIView):
    def post(self, request):
        form = RestaurantImageForm(request.POST, request.FILES)
        if form.is_valid():
            image = form.save()
            if image:
                return redirect('restaurant_create')



class RestaurantListView(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'testapp/all_partners.html'

    def get(self, request):
        queryset = Restaurant.objects.all()
        total_restaurants = queryset.count()
        # Обработка поиска
        search_query = request.GET.get('search_query')
        if search_query:
            queryset = queryset.filter(
                Q(title__icontains=search_query) |
                Q(description__icontains=search_query) |
                Q(food_type__icontains=search_query) |
                Q(phone_number__icontains=search_query) |
                Q(location__icontains=search_query)
            )

        # Обработка сортировки
        sort_by_orders = request.GET.get('sort_orders')
        sort_by_amount = request.GET.get('sort_amount')

        if sort_by_orders:
            queryset = queryset.annotate(num_orders=Count('orders')).order_by(
                'num_orders' if sort_by_orders == 'asc' else '-num_orders')
        elif sort_by_amount:
            queryset = queryset.annotate(total_amount=Sum('orders__sum_of_credit__sum')).order_by(
                'total_amount' if sort_by_amount == 'asc' else '-total_amount')

        return Response({'restaurants': queryset, 'total_restaurants': total_restaurants})


class RestaurantEditView(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'testapp/add_partner.html'

    def get(self, request, pk):
        restaurant = get_object_or_404(Restaurant, pk=pk)
        form = RestaurantForm(instance=restaurant)
        return Response({'restaurant': restaurant, 'form': form})

    def post(self, request, pk):
        restaurant = get_object_or_404(Restaurant, pk=pk)
        form = RestaurantForm(request.POST, request.FILES, instance=restaurant)
        if form.is_valid():
            restaurant = form.save()
            return redirect('restaurant_list')
        else:
            return render(request, self.template_name, {'form': form, 'success': False})



class RestaurantDeleteView(DeleteView):
    model = Restaurant
    success_url = reverse_lazy('restaurant_list')  # Укажите ваш путь, куда перенаправлять после удаления
    template_name = 'testapp/all_partners.html'  # Создайте этот шаблон в соответствии с вашими нуждами

    def delete(self, request, *args, **kwargs):
        # Ваш код обработки удаления
        return super().delete(request, *args, **kwargs)


class OrderListView(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'testapp/all_orders.html'

    def get(self, request, status):
        queryset = Order.objects.filter(status=status)
        total_orders = queryset.count()
        if total_orders > 0:
            # найти средний чек всех ордеров
            average = Order.objects.aggregate(average=Sum('sum_of_credit__sum') / total_orders)['average']
        else:
            average = 0
        search_query = request.GET.get('search_query')
        if search_query:
            queryset = queryset.filter(
                Q(user__username__icontains=search_query) |
                Q(restaurant__title__icontains=search_query) |
                Q(sum_of_credit__sum__icontains=search_query) |
                Q(period_of_credit__months__icontains=search_query) |
                Q(status__icontains=search_query)
            )

        # Обработка сортировки
        sort_by_orders = request.GET.get('sort_sum')

        if sort_by_orders:
            queryset = queryset.annotate(total_amount=Sum('sum_of_credit__sum')).order_by(
                'total_amount' if sort_by_orders == 'asc' else '-total_amount')


        return Response({'orders': queryset, 'total_orders': total_orders, 'average': average, 'status': status})


class OrderDeleteView(DeleteView):
    model = Order
    success_url = reverse_lazy('order_list')  # Укажите ваш путь, куда перенаправлять после удаления
    template_name = 'testapp/all_orders.html'  # Создайте этот шаблон в соответствии с вашими нуждами

    def delete(self, request, *args, **kwargs):
        # Ваш код обработки удаления
        return super().delete(request, *args, **kwargs)