from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from .forms import EmployeeRegisterForm, EmployeeLoginForm
from .models import AuthCode, Attendance
from django.utils import timezone
from .models import TimeLog

def register(request):
    if request.method == 'POST':
        form = EmployeeRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = EmployeeRegisterForm()
    return render(request, 'attendance/register.html', {'form': form})

def employee_login(request):
    if request.method == 'POST':
        form = EmployeeLoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            auth_code = form.cleaned_data.get('auth_code')

            user = authenticate(request, username=username, password=password)
            if user is not None:
                code_obj = AuthCode.objects.filter(user=user, code=auth_code, is_active=True).first()
                if code_obj:
                    login(request, user)
                    return redirect('time_in')
                else:
                    # Invalid auth code
                    form.add_error('auth_code', 'Invalid authentication code')
    else:
        form = EmployeeLoginForm()
    return render(request, 'attendance/login.html', {'form': form})


def time_in(request):
    if request.method == "POST":
        # Create a new TimeLog entry for the user
        TimeLog.objects.create(user=request.user, time_in=timezone.now())
        return redirect('time_log')  # Redirect to the time log page

    return render(request, 'attendance/time_in.html')

def time_out(request):
    if request.method == "POST":
        # Get the latest time log entry for the user
        time_log = TimeLog.objects.filter(user=request.user, time_out=None).last()
        if time_log:
            time_log.time_out = timezone.now()
            time_log.save()
        return redirect('time_log')  # Redirect to the time log page

    return render(request, 'attendance/time_out.html')

def time_log(request):
    # Get all time logs for the user
    time_logs = TimeLog.objects.filter(user=request.user).order_by('-time_in')
    return render(request, 'attendance/time_log.html', {'time_logs': time_logs})

