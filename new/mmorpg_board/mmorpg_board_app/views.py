# views.py
import random
import string

from django.conf import settings
from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from django.core.mail import send_mail
from django.http import Http404, HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.csrf import csrf_protect

from .forms import CustomUserCreationForm, AdvertisementForm, ResponseForm
from .models import UserProfile, Advertisement, Response, Subscriber
from .forms import SubscribeForm


def generate_verification_code():
    return ''.join(random.choices(string.ascii_letters + string.digits, k=20))


def send_verification_email(email, verification_code):
    subject = 'Verify Your Email'
    message = f'Your verification code is: {verification_code}'
    from_email = 'dorofarseniy@gmail.com'  # Замените на свой email
    recipient_list = [email]
    send_mail(subject, message, from_email, recipient_list)


def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()

            # Генерация и сохранение кода подтверждения
            verification_code = generate_verification_code()
            UserProfile.objects.create(user=user, verification_code=verification_code)

            # Отправка письма с кодом подтверждения
            send_verification_email(user.email, verification_code)

            login(request, user)

            return redirect('verification_sent')
    else:
        form = CustomUserCreationForm()

    return render(request, 'register.html', {'form': form})


@login_required
def verification_sent(request):
    return render(request, 'verification_sent.html')


def create_post(request):
    if request.method == 'POST':
        form = AdvertisementForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('post_created')
    else:
        form = AdvertisementForm()

    return render(request, 'create_post.html', {'form': form})


def post_created(request):
    return render(request, 'post_created.html')


@login_required
def profile_view(request, user_id=None):
    if user_id:
        user_profile = get_object_or_404(UserProfile, user_id=user_id)
        posts = Advertisement.objects.filter(author=user_profile.user)
        return render(request, 'user_profile.html', {'user_profile': user_profile, 'posts': posts})
    else:
        all_posts = Advertisement.objects.all()
        return render(request, 'user_profile.html', {'user': request.user, 'all_posts': all_posts})


def logout_view(request):
    logout(request)
    return redirect('login')


@csrf_protect
def login_view(request, **kwargs):
    return LoginView.as_view(template_name='login.html')(request, **kwargs)


@login_required
def edit_post(request, post_id):
    post = get_object_or_404(Advertisement, id=post_id)

    if post.author != request.user:
        raise Http404("You don't have permission to edit this post.")

    if request.method == 'POST':
        form = AdvertisementForm(request.POST, instance=post)
        if form.is_valid():
            form.save()
            return redirect('profile_view')
    else:
        form = AdvertisementForm(instance=post)

    return render(request, 'edit_post.html', {'form': form, 'post': post, 'user': request.user})


def post_detail(request, post_id):
    post = get_object_or_404(Advertisement, id=post_id)
    response_form = ResponseForm()

    if request.method == 'POST':
        response_form = ResponseForm(request.POST)
        if response_form.is_valid():
            text = response_form.cleaned_data['text']
            Response.objects.create(sender=request.user, receiver=post.author, advertisement=post, text=text)

            # Отправка уведомления по электронной почте
            subject = 'Новый отклик на ваш пост'
            message = f'Пользователь {request.user.username} оставил отклик на ваш пост "{post.title}".'
            from_email = settings.DEFAULT_FROM_EMAIL
            to_email = [post.author.email]
            send_mail(subject, message, from_email, to_email, fail_silently=True)

            return redirect('post_detail', post_id=post_id)

    responses = Response.objects.filter(advertisement=post)

    return render(request, 'post_detail.html', {'post': post, 'response_form': response_form, 'responses': responses})


@login_required
def user_responses(request):
    user_responses = Response.objects.filter(receiver=request.user)

    if request.method == 'GET':
        advertisement_id = request.GET.get('advertisement_id')
        if advertisement_id:
            user_responses = user_responses.filter(advertisement_id=advertisement_id)

    return render(request, 'user_responses.html', {'user_responses': user_responses})


@login_required
def delete_response(request, response_id):
    response = get_object_or_404(Response, id=response_id)

    if request.user == response.receiver:
        response.delete()
        messages.success(request, 'Отклик успешно удален.')
    else:
        messages.error(request, 'У вас нет прав для удаления этого отклика.')

    return redirect('user_responses')


@login_required
def accept_response(request, response_id):
    response = get_object_or_404(Response, id=response_id)

    if request.user == response.receiver:
        response.accepted = True
        response.save()

        subject = 'Ваш отклик принят'
        message = f'Ваш отклик на объявление "{response.advertisement.title}" был принят.'
        from_email = settings.DEFAULT_FROM_EMAIL
        to_email = [response.sender.email]
        send_mail(subject, message, from_email, to_email, fail_silently=True)

        messages.success(request, 'Отклик успешно принят.')
    else:
        messages.error(request, 'У вас нет прав для принятия этого отклика.')

    return redirect('user_responses')


def user_profile(request):
    user_profile = UserProfile.objects.get(user=request.user)
    responses = Response.objects.filter(receiver=request.user)

    unique_advertisements = responses.values_list('advertisement__title', flat=True).distinct()

    selected_advertisement = request.GET.get('advertisement_filter', 'all')

    if selected_advertisement != 'all':
        responses = responses.filter(advertisement__title=selected_advertisement)

    return render(request, 'user_profile.html',
                  {'user_profile': user_profile, 'responses': responses, 'unique_advertisements': unique_advertisements,
                   'selected_advertisement': selected_advertisement})


def subscribe_view(request):
    if request.method == 'POST':
        form = SubscribeForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            Subscriber.objects.create(email=email)

            return HttpResponseRedirect('/subscribe/success/')
    else:
        form = SubscribeForm()

    return render(request, 'subscribe.html', {'form': form})
