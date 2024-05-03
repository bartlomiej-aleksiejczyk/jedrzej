import ast
from types import SimpleNamespace
from dotenv import dotenv_values

def execute_string(code_string, env_variables):
    """
    Execute the given Python code string.
    """
    try:
        tree = ast.parse(code_string)
        class_def = None
        for node in tree.body:
            if isinstance(node, ast.ClassDef):
                if node.name == "MyScript":
                    class_def = node
                    break
        if class_def is None:
            raise ValueError("No class named MyScript found.")

        # Create a local namespace for execution
        local_namespace = {}
        # Populate the local namespace with required objects
        local_namespace['Script'] = Script
        local_namespace['dotenv_values'] = dotenv_values
        # Add environmental variables to the local namespace
        local_namespace.update(env_variables)

        # Create a new Module AST node with an empty type_ignores list
        module = ast.Module(body=[class_def], type_ignores=[])

        # Execute the module within the local namespace
        exec(compile(module, filename="<ast>", mode="exec"), local_namespace)

        # Instantiate the class and execute it
        my_script = local_namespace['MyScript'](env_variables)
        results = my_script.execute()
        for result in results:
            print(result)
    except Exception as e:
        print("Error:", e)

# Example usage
env_variables = {
    'ENV_VAR_1': 'value1',
    'ENV_VAR_2': 'value2',
    'EXAMPLE_VAR': 'Bajo',
    'global_var': 123
}

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
                    print(f"Starting {step.name}")
                    result = step.func(self.env)
                    results.append(result)
                    print(f"Completed {step.name}")
                except Exception as e:
                    results.append(f"{step.name} failed with exception: {e}")
                    print(f"{step.name} failed with exception: {e}")
                    break
        return results

# Example usage
code_to_execute = """
class MyScript(Script):
    def setup_steps(self):
        self.add_step(self.step1, name="Step 1")
        self.add_step(self.step2, condition=lambda results: "step1 success" in results, name="Step 2")

    def step1(self, env):
        print("Executing Step 1")
        print("Using environment variable:", env['EXAMPLE_VAR'])
        return "step1 success"

    def step2(self, env):
        print("Executing Step 2")
        return "step2 success"
"""

execute_string(code_to_execute, env_variables)
