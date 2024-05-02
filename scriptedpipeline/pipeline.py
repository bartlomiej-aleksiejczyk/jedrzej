def process_script(script):
    steps = parse_script(script)
    results = []
    for step in steps:
        result = execute_step(step)
        results.append(result)
    return results

def parse_script(script):
    # This function needs to parse the script into executable steps
    # For now, we'll mock this as a simple split by new lines
    return script.strip().split('\n')

def execute_step(step):
    # Execute a step. You might use exec, but be careful with security issues!
    # Here, we'll just mock the execution.
    # In production, you would use a safe environment for this, like a sandbox.
    local_scope = {}
    exec(step, {'__builtins__': {}}, local_scope)
    return local_scope.get('result', None)
