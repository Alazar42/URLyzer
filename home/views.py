from django.shortcuts import render
from django.http import JsonResponse
from .includes.search_url import analyze_url
import json
from django.core.exceptions import ValidationError
from django.utils.html import escape

def home(request):
    if request.method == 'POST':
        try:
            url = request.POST.get('url', '').strip()  # Get URL from POST data
            if not url:
                raise ValidationError("URL cannot be empty")
            protocol = request.POST.get('protocol', 'http://')  # Get protocol from POST data
            full_url = f'{protocol}{url}'
            results = analyze_url(full_url)
            return render(request, 'home.html', {'data': results, 'url': url, 'protocol':protocol})
        except ValidationError as e:
            error = str(e)
            return render(request, 'home.html', {'error': error})
        except Exception as e:
            error = f"An error occurred: {str(e)}"
            return render(request, 'home.html', {'error': error})
    else:
        return render(request, 'home.html')
