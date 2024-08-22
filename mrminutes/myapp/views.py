# views.py

from django.shortcuts import render
from .testscript import process_data
from .main import Summarizer


def process_view(request):
    if request.method == 'POST':
        input_data = int(request.POST.get('input_data'))
        result = process_data(input_data)
        return render(request, 'result.html', {'result': result})
    return render(request, 'input_form.html')

def test_main(request):
    """Test main function"""

    if request.method == 'POST':
        ovr = Summarizer()  # Initialize your class
        txt = ovr.speech_to_text()  # Call the speech_to_text function
        return render(request, 'result.html', {'result': txt})  # Pass result to template

    return render(request, 'input_form.html')  # Render the input form on GET request

def sum_main(request):
    """main function"""
    txt = ""

    if request.method == 'POST':
        ovr = Summarizer()  # Initialize your class