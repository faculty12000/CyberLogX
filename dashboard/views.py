from django.shortcuts import render, redirect, get_object_or_404
from .models import LogFile
import os
from dotenv import load_dotenv
import requests

load_dotenv()
OPENROUTER_API_KEY = os.getenv('OPENROUTER_API_KEY')

def home(request):
    if request.method == 'POST' and request.FILES.get('logfile'):
        LogFile.objects.create(file=request.FILES['logfile'])
        return redirect('home')
    logs = LogFile.objects.order_by('-uploaded_at')
    return render(request, 'dashboard/dashboard.html', {'logs': logs})

def view_log(request, log_id):
    log = get_object_or_404(LogFile, id=log_id)
    log_path = log.file.path
    ai_result = None

    try:
        with open(log_path, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
    except Exception as e:
        content = f"Could not read file: {e}"

    if request.method == 'POST' and 'analyze' in request.POST:
        # Call OpenRouter API
        prompt = f"Analyze this log file for security threats and summarize findings:\n{content[:4000]}"
        headers = {
            "Authorization": f"Bearer {OPENROUTER_API_KEY}",
            "Content-Type": "application/json"
        }
        data = {
            "model": "deepseek/deepseek-chat-v3-0324:free",  # <-- correct model ID for DeepSeek V3
            "messages": [
                {"role": "system", "content": "You are a cybersecurity analyst."},
                {"role": "user", "content": prompt}
            ]
        }
        try:
            response = requests.post(
                "https://openrouter.ai/api/v1/chat/completions",
                headers=headers,
                json=data,
                timeout=60
            )
            if response.status_code == 200:
                ai_result = response.json()['choices'][0]['message']['content']
            else:
                ai_result = f"API Error: {response.status_code} - {response.text}"
        except Exception as e:
            ai_result = f"Request failed: {e}"

    return render(request, 'dashboard/view_log.html', {
        'log': log,
        'content': content,
        'ai_result': ai_result
    })
