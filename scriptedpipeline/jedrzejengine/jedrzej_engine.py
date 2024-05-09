import ast
import importlib
import os

def execute_string(code_string, env_variables):
    try:
        tree = ast.parse(code_string)

        class_def = None
        imports = []
        for node in tree.body:
            if isinstance(node, ast.Import):
                imports.extend(node.names)
            elif isinstance(node, ast.ImportFrom):
                imports.append(node.module)
            elif isinstance(node, ast.ClassDef) and node.name == "MyScript":
                class_def = node

        if class_def is None:
            raise ValueError("No class named MyScript found.")

        local_namespace = {'Script': Script, 'dotenv_values': os.environ}
        local_namespace.update(env_variables)

        for imp in imports:
            module_name = imp.name if isinstance(imp, ast.alias) else imp
            local_namespace[module_name] = importlib.import_module(module_name)

        module = ast.Module(body=[class_def], type_ignores=[])

        exec(compile(module, filename="<ast>", mode="exec"), local_namespace)

        my_script = local_namespace['MyScript'](env_variables)

        for result in my_script.execute():
            print(result)

    except Exception as e:
        print("Error:", e)


class Step:
    def __init__(self, func, condition=lambda x: True, name="Step"):
        self.func = func
        self.condition = condition
        self.name = name


class Script:
    def __init__(self, env):
        self.steps = []
        self.env = env
        self.setup_steps()

    def setup_steps(self):
        # This method should be overridden by subclasses to define steps
        raise NotImplementedError("You must define steps in the setup_steps method.")

    def add_step(self, func, condition=lambda x: True, name="Step"):
        self.steps.append(Step(func, condition, name))

    def execute(self):
        results = []
        for step in self.steps:
            if step.condition(results):
                try:
                    results.append(f"Starting {step.name}")
                    yield results[-1]
                    result = step.func(self.env)
                    results.append(result)
                    yield result
                    results.append(f"Completed {step.name}")
                    yield results[-1]
                except Exception as e:
                    error_msg = f"{step.name} failed with exception: {e}"
                    results.append(error_msg)
                    yield error_msg
                    break

sample_code_to_execute = """
import time 
class MyScript(Script):
    def setup_steps(self):
        self.add_step(self.step1, name="Step 1")
        self.add_step(self.step2, condition=lambda results: "step1 success" in results, name="Step 2")

    def step1(self, env):
        print("Executing Step 1")
        time.sleep(2)  # Simulate a delay of 2 seconds
        print("Using environment variable:", env['ENV_VAR_1'])
        return "step1 success"

    def step2(self, env):
        print("Executing Step 2")
        time.sleep(1)  # Simulate a delay of 1 second
        return "step2 success"
"""