from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.db.models import Value, CharField
from django.core.paginator import Paginator
from itertools import chain

from . import models
from .forms import TicketForm, ReviewForm, UserFollowsForm
from authentication.models import User


@login_required
def home(request):
    """
    Home page view that displays the latest posts (tickets and reviews) from the user and followed users.
    It also checks if the user has already created a review for any of the tickets.
    """
    # Get the user's tickets and reviews
    user = request.user
    user_tickets = models.Ticket.objects.filter(user=user).annotate(post_type=Value('ticket', CharField()))
    user_reviews = models.Review.objects.filter(user=user).annotate(post_type=Value('review', CharField()))

    # Get the tickets and reviews from followed users
    followed_users = models.UserFollows.objects.filter(user=request.user).values_list('followed_user', flat=True)
    followed_users_tickets = models.Ticket.objects.filter(
        user__in=followed_users).annotate(post_type=Value('ticket', CharField()))
    followed_users_reviews = models.Review.objects.filter(
        user__in=followed_users).annotate(post_type=Value('review', CharField()))

    # Combine the user's posts and followed users' posts
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

    return render(request, 'main/home.html',
                  {'posts': posts, 'user': user, 'review_already_exists': review_already_exists})


@login_required
def create_ticket(request):
    """
    Create a new ticket view. If the request method is POST, it processes the form data and saves the ticket.
    If the request method is GET, it displays an empty form.
    """
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
    """
    Edit an existing ticket view. If the request method is POST, it processes the form data and updates the ticket.
    If the request method is GET, it displays the current ticket data in the form.
    """
    # Get the ticket object or return a 404 error if not found
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
    """
    Delete a ticket view. It retrieves the ticket object and deletes it from the database.
    """
    # Get the ticket object or return a 404 error if not found
    ticket = get_object_or_404(models.Ticket, id=ticket_id)
    ticket.delete()
    return redirect('posts')


@login_required
def create_review_with_ticket(request, ticket_id):
    """
    Create a review for a specific ticket.
    If the request method is POST, it processes the form data and saves the review.
    If the request method is GET, it displays an empty form.
    """
    # Get the ticket object or return a 404 error if not found
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
    """
    Create a review view. If the request method is POST, it processes the form data and saves the review.
    If the request method is GET, it displays an empty form.
    """
    # Create a new ticket and review
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
    """
    Edit an existing review view. If the request method is POST, it processes the form data and updates the review.
    If the request method is GET, it displays the current review data in the form.
    """
    # Get the review object or return a 404 error if not found
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
    """
    Delete a review view. It retrieves the review object and deletes it from the database.
    """
    # Get the review object or return a 404 error if not found
    review = get_object_or_404(models.Review, id=review_id)
    review.delete()
    return redirect('posts')


@login_required
def posts(request):
    """
    Posts view that displays all the tickets and reviews created by the user.
    It combines the tickets and reviews into a single list and sorts them by creation time.
    """
    # Get the user's tickets and reviews
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
    """
    Subscriptions view that allows the user to follow other users.
    It displays a form to enter the username of the user to follow and lists the users that the current user follows.
    """
    # Get the current user's followed users and followers
    form = UserFollowsForm()
    followers = models.UserFollows.objects.filter(followed_user=request.user)
    follows = models.UserFollows.objects.filter(user=request.user)
    error = None

    # Handle the form submission to follow a user
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
    """
    Unfollow a user view. It retrieves the UserFollows object and deletes it from the database.
    """
    # Get the UserFollows object or return a 404 error if not found
    unfollows = get_object_or_404(models.UserFollows, id=follows_id)
    unfollows.delete()
    return redirect('subscriptions')


def pagination(request, posts):
    """
    Helper function to paginate the posts.
    It takes the request and the list of posts, and returns a paginated list of posts.
    """
    # Paginate the posts
    paginator = Paginator(posts, 5)  # Show 5 posts per page
    page_number = request.GET.get('page')
    posts = paginator.get_page(page_number)
    return posts
