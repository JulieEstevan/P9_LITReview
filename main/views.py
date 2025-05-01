from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.conf import settings

from . import forms, models
from .forms import TicketForm, ReviewForm, UserFollowsForm
from authentication.models import User

@login_required
def home(request):
    print(request.user.subscriptions.exists())
    return render(request, 'main/home.html')

@login_required
def posts(request):
    return render(request, 'main/posts.html')

@login_required
def subscriptions(request):
    return render(request, 'main/subscriptions.html')

@login_required
def create_ticket(request):
    if request.method == 'POST':
        form = TicketForm(request.POST, request.FILES)
        if form.is_valid():
            ticket = form.save(commit=False)
            ticket.user = request.user
            ticket.save()
            return redirect('posts')
    else:
        form = TicketForm()
    return render(request, 'main/create_ticket.html', {'form': form})

@login_required
def create_review(request):
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        ticket_form = TicketForm(request.POST, request.FILES)
        if ticket_form.is_valid():
            ticket = ticket_form.save(commit=False)
            ticket.user = request.user
            ticket.save()
        if form.is_valid():
            review = form.save(commit=False)
            review.user = request.user
            review.save()
            return redirect('posts')
    else:
        form = ReviewForm()
        ticket_form = TicketForm()
    return render(request, 'main/create_review.html', {'form': form, 'ticket_form': ticket_form})

@login_required
def subscriptions(request):
    form = UserFollowsForm()
    followers = models.UserFollows.objects.filter(followed_user=request.user)
    follows = models.UserFollows.objects.filter(user=request.user)
    error = None
    if request.method == 'POST':
        form = UserFollowsForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            if username != request.user.username:
                try:
                    followed_user = User.objects.get(username=username)
                    if not models.UserFollows.objects.filter(user=request.user, followed_user=followed_user).exists():
                        models.UserFollows.objects.create(user=request.user, followed_user=followed_user)
                        return redirect('subscriptions')
                    else:
                        error = 'Vous suivez déjà cet utilisateur.'
                except User.DoesNotExist:
                    error = 'Cet utilisateur n\'existe pas.'
            else:
                error = 'Vous ne pouvez pas vous suivre vous-même.'
    else:
        form = UserFollowsForm()
    context = {
        'form': form,
        'followers': followers,
        'follows': follows,
        'error': error,
    }
    return render(request, 'main/subscriptions.html', context)

@login_required
def unfollows(request, follows_id):
    unfollows = models.UserFollows.objects.get(id=follows_id)
    unfollows.delete()
    return redirect('subscriptions')