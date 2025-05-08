"""
URL configuration for LITReview project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

import authentication.views
import main.views

urlpatterns = [
    # Admin URL
    # This URL is used to access the Django admin interface.
    path('admin/', admin.site.urls),
    # Authentication URLs
    # These URLs are used for user authentication, including login, logout, and signup.
    # The login URL uses a custom template and redirects authenticated users to the home page.
    path('', LoginView.as_view(
        template_name='authentication/login.html',
        redirect_authenticated_user=True,
    ), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('signup/', authentication.views.signup_page, name='signup'),

    # Main URLs
    # These URLs are used for the main functionality of the application,
    # including viewing and managing tickets and reviews.
    path('home/', main.views.home, name='home'),
    path('posts/', main.views.posts, name='posts'),
    path('subscriptions/', main.views.subscriptions, name='subscriptions'),
    path('unfollows/<int:follows_id>', main.views.unfollows, name='unfollows'),
    path('create_ticket/', main.views.create_ticket, name='create_ticket'),
    path('edit_ticket/<int:ticket_id>', main.views.edit_ticket, name='edit_ticket'),
    path('delete_ticket/<int:ticket_id>', main.views.delete_ticket, name='delete_ticket'),
    path('create_review/', main.views.create_review, name='create_review'),
    path('create_review/<int:ticket_id>', main.views.create_review_with_ticket, name='create_review_with_ticket'),
    path('edit_review/<int:review_id>', main.views.edit_review, name='edit_review'),
    path('delete_review/<int:review_id>', main.views.delete_review, name='delete_review'),
]

# Serve static and media files in development
if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
