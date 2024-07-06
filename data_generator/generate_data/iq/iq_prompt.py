
def iq_prompt(examples, path):
    prompt = "Generate an IQ test question. Requirements:"
    requirements = (
        "1. The test questions are graphical reasoning questions that require you to choose an answer from the options that matches the pattern of the sequence given in the question. One and only one of the answers from the options conforms to this pattern.\n"
        "2. Determine the pattern, sequence, and options clearly.\n"
        "3. The pattern should not be too complicated, and should not use color as a pattern.\n"
        "4. The sequence can include more figures (more than 2) to show the pattern clearly.\n"
        "5. The code must be consistent with the pattern, sequence, and options, especially the quantity.\n"
        "6. The code must control the spacing so that the space is enough between sequences and between options.\n"
        "7. The code can use subplots to make the layout neat.\n"
        "8. The code should not show axes on the figure.\n"
        f"Save the figure to {path}\n"
        "I will give you some examples to refer to. After reading the examples, generate one completely different instance.\n"
        "Be creative of patterns and the Generated instance must be a brand new one.\n"
        'Don not generate any other content except the JSON: {"...": "..."}'
    )

    for i, example in enumerate(examples):
        requirements += f"\nExample {i + 1}: {example}"

    return prompt + requirements
