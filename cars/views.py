from django.shortcuts import render, redirect
from cars.models import Car, CarIntentory
from cars.forms import CarModelForm
from django.views import View
from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from babel.numbers import format_currency
    
class CarsListView(ListView):
    model = Car
    template_name = 'cars.html'
    context_object_name = 'cars'

    #Se vc precisa filtrar algo usa esse metodo, porem se nao usar ele entende como um Car.objects.all()
    def get_queryset(self):
        cars = super().get_queryset().order_by('model')
        search = self.request.GET.get('search')
        if search:
            cars = cars.filter(model__icontains=search)
        return cars
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        inventory = CarIntentory.objects.first()

        context['cars_count'] = inventory.cars_count if inventory else 0
        context['cars_value'] = format_currency(inventory.cars_value, 'BRL', locale='pt_BR') if inventory else "R$ 0,00"
        
        return context

#usando o CreateView, no template .html usa-se o padrao form. para acessar as informacoes do formulario
@method_decorator(login_required(login_url='login'), name='dispatch')
class NewCarCreateView(CreateView):
    model = Car
    form_class = CarModelForm
    template_name = 'new_car.html'
    success_url = '/cars/'

class CarDetailView(DetailView):
    model = Car
    template_name = 'car_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        car = self.get_object()
        context['formatted_value'] = format_currency(car.value, 'BRL', locale='pt_BR')
        return context

@method_decorator(login_required(login_url='login'), name='dispatch')
class CarUpdateView(UpdateView):
    model = Car
    form_class = CarModelForm
    template_name = 'car_update.html'
    #success_url = '/cars/'

    def get_success_url(self):
        return reverse('car_detail', kwargs={'pk': self.object.pk})
    
@method_decorator(login_required(login_url='login'), name='dispatch')
class CarDeleteView(DeleteView):
    model = Car
    template_name = 'car_delete.html'
    success_url = '/cars/'