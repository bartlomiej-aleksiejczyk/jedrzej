class Step:
    def __init__(self, func, condition=lambda x: True):
        self.func = func
        self.condition = condition

class Script:
    def __init__(self):
        self.steps = []
        self.setup_steps()

    def setup_steps(self):
        # This method should be overridden by subclasses to define steps
        raise NotImplementedError("You must define steps in the setup_steps method.")

    def add_step(self, func, condition=lambda x: True):
        self.steps.append(Step(func, condition))

    def execute(self):
        results = []
        for step in self.steps:
            if step.condition(results):
                try:
                    result = step.func()
                    results.append(result)
                except Exception as e:
                    results.append(f"Step failed with exception: {e}")
                    break
        return results
