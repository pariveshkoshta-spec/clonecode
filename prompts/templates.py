CLONE_DETECTION_PROMPT = """
Determine if the following two code snippets are semantic clones (meaning they perform the exact same core function or logic, even if implemented using different algorithms, variable names, or programming languages). 

Code Snippet 1:
{code1}

Code Snippet 2:
{code2}

Think step-by-step internally if you must, but your FINAL output must be ONLY the number "1" if they are clones, or ONLY the number "0" if they are NOT clones. Do not include any explanations in your output.
"""
