class PipelineStep:
    def execute(self, data):
        raise NotImplementedError("Each step must define an execute method.")

class PrintStep(PipelineStep):
    def __init__(self, message):
        self.message = message

    def execute(self, data):
        print(self.message)  
        return data + self.message + "\n"

class ModifyStep(PipelineStep):
    def __init__(self, append_text):
        self.append_text = append_text

    def execute(self, data):
        return data + self.append_text + "\n"

step_classes = {
    'PrintStep': PrintStep,
    'ModifyStep': ModifyStep,
}

def process_script(script):
    steps = parse_script(script)
    data = "" 
    for step in steps:
        step_type, args = step.split(':', 1)
        step_class = step_classes.get(step_type.strip())
        if step_class:
            step_instance = step_class(args.strip())
            data = step_instance.execute(data)
    return data

def parse_script(script):
    return script.strip().split('\n')
