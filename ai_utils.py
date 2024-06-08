import ollama

def interpret_rule(rule_text, context):
    response = ollama.query(model='ollama-base', input=rule_text, context=context)
    return response
