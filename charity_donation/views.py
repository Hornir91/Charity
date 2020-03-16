from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import View

from charity_donation.models import Donation, Institution, Category


class LandingPage(View):

    def get(self, request):
        bags = Donation.objects.all()
        bags_count = 0
        for bag in bags:
            bags_count += int(bag.quantity)
        charities = Institution.objects.all()
        char_cnt = charities.count()

        return render(request, 'index.html', {'bags_count': bags_count, 'charities': charities, 'char_cnt': char_cnt})


class AddDonation(LoginRequiredMixin, View):
    login_url = '/login/#login'

    def get(self, request):
        categories = Category.objects.all()
        institutions = Institution.objects.all()
        return render(request, 'form.html', {'categories': categories, 'institutions': institutions})


class Login(View):

    def get(self, request):
        return render(request, 'login.html')

    def post(self, request):
        email = request.POST.get('email')
        password = request.POST.get('password')
        usr = User.objects.get(email=email)
        user = authenticate(username=usr.username, password=password)
        if user is not None:
            login(request, user)
            return redirect(reverse_lazy('landing-page'))
        else:
            return redirect(reverse_lazy('register'))


class Logout(View):

    def get(self, request):
        logout(request)
        return redirect(reverse_lazy('landing-page'))


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


class UserProfile(View):

    def get(self, request):
        user = User.objects.get(pk=request.user.id)
        return render(request, 'user_profile.html', locals())
