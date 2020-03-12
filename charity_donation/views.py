from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import View

from charity_donation.models import Donation, Institution


class LandingPage(View):

    def get(self, request):
        bags = Donation.objects.all()
        bags_count = 0
        for bag in bags:
            bags_count += int(bag.quantity)
        charities = Institution.objects.all()
        char_cnt = charities.count()

        return render(request, 'index.html', {'bags_count': bags_count, 'charities': charities, 'char_cnt': char_cnt})


class AddDonation(View):

    def get(self, request):
        return render(request, 'form.html')


class Login(View):

    def get(self, request):
        return render(request, 'login.html')


class Register(View):

    def get(self, request):
        return render(request, 'register.html')

    def post(self, request):
        name = request.POST.get('name')
        surname = request.POST.get('surname')
        email = request.POST.get('email')
        password = request.POST.get('password')
        password2 = request.POST.get('password2')
        o = User.objects.create_user(username=name, email=email, password=password)
        return redirect(reverse_lazy('login'))
