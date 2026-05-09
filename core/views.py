import json
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render
from patients.models import Patient
from .ai_assistant import ask_gemini

@login_required
def dashboard(request):
    context = {
        'total_patients': Patient.objects.filter(is_active=True).count(),
        'recent_patients': Patient.objects.filter(is_active=True).order_by('-created_at')[:5],
    }
    return render(request, 'core/dashboard.html', context)


@login_required
def ai_chat(request):
    """Vue AJAX pour le chat IA."""
    if request.method == 'POST':
        data     = json.loads(request.body)
        messages = data.get('messages', [])

        system_prompt = """Tu es un assistant médical intelligent intégré dans le système 
de gestion de la Clinique Al Shifa. Tu aides le personnel médical et administratif.
Tu peux répondre aux questions sur :
- Les procédures médicales courantes
- La gestion administrative de la clinique
- Les médicaments et interactions courantes
- Les conseils pour utiliser le système (patients, RDV, consultations, facturation)
Réponds toujours en français, de façon concise et professionnelle.
⚠️ Rappelle toujours que tu n'es pas un médecin et que les décisions médicales
doivent être prises par des professionnels de santé qualifiés."""

        reply = ask_gemini(messages, system_prompt)
        return JsonResponse({'reply': reply})

    return JsonResponse({'error': 'Méthode non autorisée'}, status=405)