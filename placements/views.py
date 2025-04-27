from django.shortcuts import render, redirect
from .models import Job, Application
from .forms import UserRegistrationForm, ApplicationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .models import Profile
from .models import Notification
from django.http import HttpResponseRedirect
from django.urls import reverse

def home(request):
    return render(request, 'placements/home.html')

def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.set_password(user.password)
            user.save()
            return redirect('login')
    else:
        form = UserRegistrationForm()
    return render(request, 'placements/register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user:
            login(request, user)
            return redirect('dashboard_student')
    return render(request, 'placements/login.html')

@login_required
def dashboard_student(request):
    jobs = Job.objects.all()
    return render(request, 'placements/dashboard_student.html', {'jobs': jobs})

@login_required
def job_detail(request, job_id):
    job = Job.objects.get(id=job_id)
    return render(request, 'placements/job_detail.html', {'job': job})

@login_required
def apply_job(request, job_id):
    job = Job.objects.get(id=job_id)
    if request.method == 'POST':
        Application.objects.create(user=request.user, job=job)
        return redirect('dashboard_student')
    return render(request, 'placements/apply_job.html', {'job': job})
@login_required
def profile_settings(request):
    profile = request.user.profile  # get profile
    if request.method == 'POST':
        if 'profile_image' in request.FILES:
            profile.profile_image = request.FILES['profile_image']
        if 'resume' in request.FILES:
            profile.resume = request.FILES['resume']
        profile.save()
        return redirect('profile_settings')
    return render(request, 'placements/profile_settings.html', {'profile': profile})


@login_required
def notifications(request):
    notifications = Notification.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'placements/notifications.html', {'notifications': notifications})
def logout_view(request):
    logout(request)
    return redirect('home')
@login_required
def mark_notification_read(request, notification_id):
    notification = Notification.objects.get(id=notification_id)
    notification.is_read = True
    notification.save()
    return HttpResponseRedirect(reverse('notifications'))
@login_required
def update_application_status(request, application_id, status):
    application = JobApplication.objects.get(id=application_id)
    application.status = status
    application.save()
    return redirect('dashboard_student')
