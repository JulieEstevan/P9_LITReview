from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.db.models import Value, CharField
from django.core.paginator import Paginator
from itertools import chain

from . import models
from .forms import TicketForm, ReviewForm, UserFollowsForm
from authentication.models import User


@login_required
def home(request):
    user = request.user
    user_tickets = models.Ticket.objects.filter(user=user).annotate(post_type=Value('ticket', CharField()))
    user_reviews = models.Review.objects.filter(user=user).annotate(post_type=Value('review', CharField()))

    followed_users = models.UserFollows.objects.filter(user=request.user).values_list('followed_user', flat=True)
    followed_users_tickets = models.Ticket.objects.filter(user__in=followed_users).annotate(post_type=Value('ticket', CharField()))
    followed_users_reviews = models.Review.objects.filter(user__in=followed_users).annotate(post_type=Value('review', CharField()))

    tickets = chain(user_tickets, followed_users_tickets)
    reviews = chain(user_reviews, followed_users_reviews)
    posts = sorted(chain(tickets, reviews), key=lambda post: post.time_created, reverse=True)

    # Check if the user has already created a review for any of the tickets
    review_already_exists = False
    for post in posts:
        if isinstance(post, models.Ticket):
            if models.Review.objects.filter(ticket=post, user=user).exists():
                review_already_exists = True
                break
    
    # Paginate the posts
    posts = pagination(request, posts)

    return render(request, 'main/home.html', {'posts': posts, 'user': user, 'review_already_exists': review_already_exists})

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
def edit_ticket(request, ticket_id):
    ticket = get_object_or_404(models.Ticket, id=ticket_id)
    if request.method == 'POST':
        form = TicketForm(request.POST, request.FILES, instance=ticket)
        if form.is_valid():
            ticket = form.save(commit=False)
            ticket.user = request.user
            ticket.save()
            return redirect('posts')
    else:
        form = TicketForm(instance=ticket)
    return render(request, 'main/edit_ticket.html', {'form': form, 'ticket': ticket})

@login_required
def delete_ticket(request, ticket_id):
    ticket = get_object_or_404(models.Ticket, id=ticket_id)
    ticket.delete()
    return redirect('posts')

@login_required
def create_review_with_ticket(request, ticket_id):
    ticket = get_object_or_404(models.Ticket, id=ticket_id)
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.user = request.user
            review.ticket = ticket
            review.save()
            return redirect('posts')
    else:
        form = ReviewForm()
    return render(request, 'main/create_review_with_ticket.html', {'form': form, 'ticket': ticket})

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
            review.ticket = ticket
            review.save()
            return redirect('posts')
    else:
        form = ReviewForm()
        ticket_form = TicketForm()
    return render(request, 'main/create_review.html', {'form': form, 'ticket_form': ticket_form})

@login_required
def edit_review(request, review_id):
    review = get_object_or_404(models.Review, id=review_id)
    if request.method == 'POST':
        form = ReviewForm(request.POST, instance=review)
        if form.is_valid():
            form.save()
            return redirect('posts')
    else:
        form = ReviewForm(instance=review)
    return render(request, 'main/edit_review.html', {'form': form})

@login_required
def delete_review(request, review_id):
    review = get_object_or_404(models.Review, id=review_id)
    review.delete()
    return redirect('posts')

@login_required
def posts(request):
    user_tickets = models.Ticket.objects.filter(user=request.user)
    user_tickets = user_tickets.annotate(post_type=Value('ticket', CharField()))
    user_reviews = models.Review.objects.filter(user=request.user)
    user_reviews = user_reviews.annotate(post_type=Value('review', CharField()))
    
    posts = sorted(chain(user_tickets, user_reviews), key=lambda post: post.time_created, reverse=True)

    # Paginate the posts
    posts = pagination(request, posts)

    return render(request, 'main/posts.html', {'posts': posts})

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
    unfollows = get_object_or_404(models.UserFollows, id=follows_id)
    unfollows.delete()
    return redirect('subscriptions')

def pagination(request, posts):
    paginator = Paginator(posts, 5)  # Show 5 posts per page
    page_number = request.GET.get('page')
    posts = paginator.get_page(page_number)
    return posts