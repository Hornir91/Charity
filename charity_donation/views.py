from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.core import serializers
from django.core.exceptions import ObjectDoesNotExist
from django.http import JsonResponse, HttpResponse, Http404
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

    def post(self, request):
        quantity = request.POST.get('bags')
        address = request.POST.get('address')
        phone_number = request.POST.get('phone')
        city = request.POST.get('city')
        zip_code = request.POST.get('postcode')
        pick_up_date = request.POST.get('data')
        pick_up_time = request.POST.get('time')
        pick_up_comment = request.POST.get('more_info')
        user_id = request.user.id
        institution_id = request.POST.get('organization')
        donation = Donation.objects.create(quantity=quantity, address=address, phone_number=phone_number, city=city,
                                           zip_code=zip_code, pick_up_date=pick_up_date, pick_up_time=pick_up_time,
                                           pick_up_comment=pick_up_comment, user_id=user_id,
                                           institution_id=institution_id)
        categories = request.POST.getlist('categories')
        donation.categories.add(*categories)

        return redirect(reverse_lazy('form-confirmation'))


class FormConfirmation(View):

    def get(self, request):
        return render(request, 'form-confirmation.html')


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
        if request.user.is_authenticated:
            return redirect(reverse_lazy('landing-page'))
        else:
            return render(request, 'register.html')

    def post(self, request):
        name = request.POST.get('name')
        surname = request.POST.get('surname')
        email = request.POST.get('email')
        password = request.POST.get('password')
        password2 = request.POST.get('password2')
        o = User.objects.create_user(username=name, email=email, password=password)
        return redirect(reverse_lazy('login'))


class UserProfile(LoginRequiredMixin, View):
    login_url = '/login/#login'

    def get(self, request):
        user = User.objects.get(pk=request.user.id)
        donations = Donation.objects.filter(user_id=request.user.id)
        return render(request, 'user_profile.html', locals())


def third_step_filter(request):
    if request.method == 'GET':
        categories = request.GET.getlist('categoriesChecked')
        if categories:
            final_data = []
            data = Institution.objects.filter(categories__in=categories)
            for obj in data:
                if obj in final_data:
                    continue
                else:
                    final_data.append(obj)
            data_json = serializers.serialize('json', final_data)
            return JsonResponse(data_json, safe=False)
        else:
            return HttpResponse("Coś poszło nie tak :(")


def is_taken_change(request):
    if request.method == "GET":
        donation_change = request.GET.get('checked_status')
        donation_id = request.GET.get('donation_id')
        if donation_change == "false":
            donation = Donation.objects.get(pk=donation_id)
            donation.is_taken = False
            donation.save()
            donation_complete = serializers.serialize('json', [donation])
            return JsonResponse(donation_complete, safe=False)
        elif donation_change == "true":
            donation = Donation.objects.get(pk=donation_id)
            donation.is_taken = True
            donation.save()
            donation_complete = serializers.serialize('json', [donation])
            return JsonResponse(donation_complete, safe=False)
        else:
            return HttpResponse("Coś poszło nie tak :(")

# TODO Edit user info and make a valid form for changing password


class EditUser(LoginRequiredMixin, View):
    login_url = '/login/#login'

    def get(self, request):
        return render(request, "edit_user.html")

    def post(self, request):
        if "edit_user_confirm" in request.POST:
            user = User.objects.get(pk=request.user.id)
            user.name = request.POST.get('name')
            user.surname = request.POST.get('surname')
            user.email = request.POST.get('email')
            user.save()
            return HttpResponse("Pomyślnie zmieniono dane")
        elif "change_password" in request.POST:
            pass
        else:
            raise Http404
