from django.shortcuts import render
from .forms import ScriptForm
from .pipeline import process_script

def script_input(request):
    if request.method == 'POST':
        form = ScriptForm(request.POST)
        if form.is_valid():
            script = form.cleaned_data['script']
            results = process_script(script)
            return render(request, 'result.html', {'results': results})
    else:
        form = ScriptForm()

    return render(request, 'script_form.html', {'form': form})
