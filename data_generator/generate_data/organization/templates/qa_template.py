from enum import Enum

QA_TYPES = Enum("QA_TYPES", ["STRUCTURAL", "MATH_REASONING"])

qa_types = {
    QA_TYPES["STRUCTURAL"]: {
        "Example 1": "What is the type of this figure? Choose your answer from organization chart, pie chart, line chart, gantt chart.",
        "Example 2": "What's the color of xxx?",
    },
    QA_TYPES["MATH_REASONING"]: {
        "Example 1": "How many people does xxx department / node have?",
        "Example 2": "Does xxx node exist in this figure?",
        "Example 3": "How many nodes are there?",
    },
}


def qa_template():
    return """{
    "STRUCTURAL":[
        {
            "Q":"...",
            "A":"..."
        },
        ...
    ],
    "MATH_REASONING":[
        {
            "Q":"...",
            "A":"..."
        },
        ...
    ]
}"""
