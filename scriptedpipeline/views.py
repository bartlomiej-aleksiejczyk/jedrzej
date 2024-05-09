from django.shortcuts import render
from django.http import HttpResponse
from .forms import ScriptForm
from .jedrzejengine import execute_string


def script_input(request):
    if request.method == 'POST':
        form = ScriptForm(request.POST)
        if form.is_valid():
            code_string = form.cleaned_data['script']
            # env_variables = dotenv_values()
            env_variables = {
                'ENV_VAR_1': 'value1',
                'ENV_VAR_2': 'value2',
                'global_var': 123
            }
            try:
                results = []
                for result in execute_string(code_string, env_variables):
                    results.append(result)

                return HttpResponse(f"Script executed. Results: {'<br>'.join(results)}")
            except Exception as e:
                return HttpResponse(f"Error executing script: {e}")
    else:
        form = ScriptForm()

    return render(request, 'pipeline_form.html', {'form': form})
