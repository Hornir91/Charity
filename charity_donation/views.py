from django.shortcuts import render
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
