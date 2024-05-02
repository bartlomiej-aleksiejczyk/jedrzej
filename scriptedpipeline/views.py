import importlib
from django.shortcuts import render
from django.http import HttpResponse
from .forms import ScriptForm

def script_input(request):
    if request.method == 'POST':
        form = ScriptForm(request.POST)
        if form.is_valid():
            script_module = form.cleaned_data['script']
            module_name, class_name = script_module.rsplit('.', 1)

            try:
                mod = importlib.import_module(module_name)
                script_class = getattr(mod, class_name)
                script_instance = script_class()
                results = script_instance.execute()
                return HttpResponse(f"Script executed. Results: {results}")
            except Exception as e:
                return HttpResponse(f"Error loading or executing script: {e}")
    else:
        form = ScriptForm()
    return render(request, 'pipeline_form.html', {'form': form})