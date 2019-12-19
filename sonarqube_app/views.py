from django.shortcuts import render
from .forms import SonarForm


def sonar(request):
    form = SonarForm()
    return render(request, 'sonar_page.html', {'title': 'Sonar', 'form': form})
