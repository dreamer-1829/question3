from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.utils.timezone import now
from .models import WeightEntry
from .forms import WeightForm, DateRangeForm
from django import forms



# SIGNUP
def signup_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'weight_loss/signup.html', {'form': form})


# LOGIN
def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')
    else:
        form = AuthenticationForm()

    return render(request, 'weight_loss/login.html', {'form': form})


# LOGOUT
def logout_view(request):
    logout(request)
    return redirect('login')


# ADD WEIGHT
@login_required
def add_weight(request):
    today = now().date()

    if WeightEntry.objects.filter(user=request.user, date=today).exists():
        return render(request, 'weight_loss/add_weight.html',
                      {'error': "You already added your weight today!"})

    if request.method == 'POST':
        form = WeightForm(request.POST)
        if form.is_valid():
            weight_obj = form.save(commit=False)
            weight_obj.user = request.user
            weight_obj.save()
            return redirect('list_weights')
    else:
        form = WeightForm()

    return render(request, 'weight_loss/add_weight.html', {'form': form})


# LIST WEIGHTS
@login_required
def list_weights(request):
    entries = WeightEntry.objects.filter(user=request.user).order_by('-date')
    paginator = Paginator(entries, 5)

    page = request.GET.get('page')
    page_obj = paginator.get_page(page)

    return render(request, 'weight_loss/list_weights.html',
                  {'page_obj': page_obj})


# EDIT WEIGHT
@login_required
def edit_weight(request, id):
    entry = get_object_or_404(WeightEntry, id=id, user=request.user)

    if request.method == 'POST':
        form = WeightForm(request.POST, instance=entry)
        if form.is_valid():
            form.save()
            return redirect('list_weights')
    else:
        form = WeightForm(instance=entry)

    return render(request, 'weight_loss/edit_weight.html', {'form': form})


# DELETE WEIGHT
@login_required
def delete_weight(request, id):
    entry = get_object_or_404(WeightEntry, id=id, user=request.user)
    entry.delete()
    return redirect('list_weights')


# WEIGHT LOSS BETWEEN DATES
@login_required
def weight_loss_between_dates(request):
    result = None
    entries = None

    if request.method == 'POST':
        form = DateRangeForm(request.POST)
        if form.is_valid():
            start = form.cleaned_data['start_date']
            end = form.cleaned_data['end_date']

            entries = WeightEntry.objects.filter(
                user=request.user, date__range=[start, end]
            ).order_by('date')

            if entries.exists():
                first = entries.first().weight
                last = entries.last().weight
                result = first - last
    else:
        form = DateRangeForm()

    return render(request, 'weight_loss/weight_loss_between_dates.html',
                  {'form': form, 'result': result, 'entries': entries})


# HOME PAGE
def home(request):
    return render(request, 'weight_loss/home.html')
