from django.shortcuts import render
import requests
import json
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import JsonResponse
from .forms import CSSRegistrationForm, JSRegistrationForm
from .models import PageRating
from django.views.decorators.http import require_http_methods
import logging

logger = logging.getLogger(__name__)

def main_page(request):
    return render(request, 'pages/main.html')

def page1(request):
    return render(request, 'pages/page1.html')

def page2(request):
    return render(request, 'pages/page2.html')

def page3(request):
    return render(request, 'pages/page3.html')

def login_page(request):
    return render(request, 'pages/login.html')

@csrf_exempt
def send_feedback(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            message = data.get('message', '')
            
            if not message.strip():
                return JsonResponse({'status': 'error', 'error': 'Empty message'}, status=400)
            
            telegram_message = f"new message from my website:\n\n{message}"
            
            url = f'https://api.telegram.org/bot{settings.TELEGRAM_TOKEN}/sendMessage'
            payload = {
                'chat_id': settings.TELEGRAM_CHAT_ID,
                'text': telegram_message,
                'parse_mode': 'HTML'
            }
            
            response = requests.post(url, json=payload)
            
            if response.status_code == 200:
                return JsonResponse({'status': 'ok'})
            else:
                return JsonResponse({'status': 'error', 'error': 'Telegram API error'}, status=500)
                
        except Exception as e:
            return JsonResponse({'status': 'error', 'error': str(e)}, status=500)
    
    return JsonResponse({'status': 'error', 'error': 'Method not allowed'}, status=405)


def login_css(request):
    if request.method == 'POST':
        form = CSSRegistrationForm(request.POST)
        if form.is_valid():
            # print("AGE FROM FORM:", form.cleaned_data['age'])
            user = form.save()
            # print("AGE SAVED:", user.age)
            messages.success(request, f'Welcome, {user.first_name}! Registration successful!')
            return redirect('registration_success')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = CSSRegistrationForm()
    
    return render(request, 'pages/login_css.html', {'form': form})

def login_js(request):
    if request.method == 'POST':
        form = JSRegistrationForm(request.POST)
        if form.is_valid():
            # print("AGE FROM FORM:", form.cleaned_data['age'])
            user = form.save()
            # print("AGE SAVED:", user.age)
            return JsonResponse({
                'success': True,
                'message': f'Welcome, {user.first_name}! Registration successful!'
            })
        else:
            return JsonResponse({
                'success': False,
                'errors': form.errors
            }, status=400)
    
    return render(request, 'pages/login_js.html')

# lab6 

def registration_success(request):
    return render(request, 'pages/registration_success.html')

def init_ratings():
    for page in ['page1', 'page2', 'page3']:
        PageRating.objects.get_or_create(page_name=page)

def get_ratings(request):
    page_name = request.GET.get('page_name')
    
    if not page_name:
        return JsonResponse({'error': 'page_name required'}, status=400)
    
    try:
        response = requests.get(
            f"{RATINGS_API_URL}/api/get-ratings",
            params={'page_name': page_name},
            timeout=5  # таймаут 5 секунд
        )
        
        if response.status_code == 200:
            return JsonResponse(response.json())
        else:
            logger.error(f"Ratings API error: {response.status_code} - {response.text}")
            return JsonResponse({'error': 'Service unavailable'}, status=502)
            
    except requests.exceptions.ConnectionError:
        logger.error(f"Cannot connect to {RATINGS_API_URL}")
        return JsonResponse({'error': 'Cannot connect to ratings service'}, status=502)
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        return JsonResponse({'error': str(e)}, status=500)

@csrf_exempt
@require_http_methods(["POST"])
def rate_page(request):
    try:
        data = json.loads(request.body)
        
        response = requests.post(
            f"{RATINGS_API_URL}/api/rate",
            json=data,
            headers={"Content-Type": "application/json"},
            timeout=5
        )
        
        return JsonResponse(response.json(), status=response.status_code)
        
    except requests.exceptions.ConnectionError:
        return JsonResponse({'error': 'Cannot connect to ratings service'}, status=502)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

@csrf_exempt
@require_http_methods(["POST"])
def reset_ratings(request):
    try:
        data = json.loads(request.body)
        
        response = requests.post(
            f"{RATINGS_API_URL}/api/reset-ratings",
            json=data,
            headers={"Content-Type": "application/json"},
            timeout=5
        )
        
        return JsonResponse(response.json(), status=response.status_code)
        
    except requests.exceptions.ConnectionError:
        return JsonResponse({'error': 'Cannot connect to ratings service'}, status=502)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

# lab7

RATINGS_API_URL = "http://ratings_api:8002"
