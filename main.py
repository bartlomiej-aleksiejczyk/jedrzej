def execute_string(code_string):
    """
    Execute the given Python code string.
    """
    try:
        exec(code_string, globals())
        my_script = MyScript()
        results = my_script.execute()
        for result in results:
            print(result)
    except Exception as e:
        print("Error:", e)


class Step:
    def __init__(self, func, condition=lambda x: True, name="Step"):
        self.func = func
        self.condition = condition
        self.name = name


class Script:
    def __init__(self):
        self.steps = []
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
                    result = step.func()
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

    def step1(self):
        print("Executing Step 1")
        return "step1 success"

    def step2(self):
        print("Executing Step 2")
        return "step2 success"
"""

execute_string(code_to_execute)
