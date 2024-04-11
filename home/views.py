from django.shortcuts import render
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from .includes.search_url import analyze_url
import json
from django.core.exceptions import ValidationError
from django.utils.html import escape

@login_required
def home(request):
    if request.method == 'POST':
        try:
            url = request.POST['url'].strip()  # Get URL from POST data
            if not url:
                raise ValidationError("URL cannot be empty")
            protocol = request.POST['protocol']  # Get protocol from POST data
            full_url = f'{protocol}{url}'
            results = analyze_url(full_url)
            if results is not None:    
                data_found = True
            return render(request, 'index.html', {'data': results, 'url': url, 'protocol':protocol, 'data_found':data_found})
        except ValidationError as e:
            error = str(e)
            data_found = False
            return render(request, 'index.html', {'error': error, 'data_found':data_found})
        except Exception as e:
            error = f"An error occurred: {str(e)}"
            data_found = False
            return render(request, 'index.html', {'error': error, 'data_found':data_found})
    else:
        return render(request, 'index.html')
