# myapp/pipeline.py

class PipelineStep:
    def execute(self, data):
        raise NotImplementedError("Each step must define an execute method.")

class PrintStep(PipelineStep):
    def __init__(self, message):
        self.message = message

    def execute(self, data):
        print(self.message)  # Or accumulate messages in a list to show in the web
        return data + self.message + "\n"

class ModifyStep(PipelineStep):
    def __init__(self, append_text):
        self.append_text = append_text

    def execute(self, data):
        return data + self.append_text + "\n"

# Map of allowed steps and their corresponding classes
step_classes = {
    'PrintStep': PrintStep,
    'ModifyStep': ModifyStep,
}

def process_script(script):
    steps = parse_script(script)
    data = ""  # Initial data passed through the pipeline
    for step in steps:
        step_type, args = step.split(':', 1)
        step_class = step_classes.get(step_type.strip())
        if step_class:
            step_instance = step_class(args.strip())
            data = step_instance.execute(data)
    return data

def parse_script(script):
    # Each step is on a new line
    return script.strip().split('\n')
