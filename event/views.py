from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import LeadForm
from .tasks import send_email

def home(request):
    form = LeadForm()
    return render(request, 'home.html', {'form': form})

def confirmation(request):
    if request.session.get('confirmed'):
        name = request.session.get('name')
        email = request.session.get('email')
        
        context = {
            'name': name,
            'email': email,
        }
        send_email.delay(name, email)    
        return render(request, 'confirmation.html', context)
    else:
        return redirect('home')

def register(request):
    if request.method == 'GET':
        return redirect('home')
    
    form = LeadForm(request.POST)
    if form.is_valid():
        lead = form.save()
        messages.success(request, 'Cadastro realizado com sucesso')
        request.session['confirmed'] = True
        request.session['name'] = lead.name
        request.session['email'] = lead.email
        return redirect('confirmation')
    else:
        messages.error(request, 'Dados inválidos')

    return render(request, 'home.html', {'form': form})