from enum import Enum

ALGORITHM_QA_TYPES = Enum('ALGORITHM_QA_TYPES', ['STRUCTURAL'])

algorithm_qa_types = {
    ALGORITHM_QA_TYPES['STRUCTURAL']: {
        'Example 1': "How many types of symbols are there in the flowchart?",
        'Example 2': 'How many oval symbols are there in the flowchart?',
        "Example 3": "How many rectangular symbols are there in the flowchart?",
        "Example 4": "What is the color of the diamond symbol?",
        "Example 5": "What is the color of the parallelogram symbol?",
    }
}

DAILY_QA_TYPES = Enum('DAILY_QA_TYPES', ['STRUCTURAL', 'REASONING'])

daily_qa_types = {
    DAILY_QA_TYPES['STRUCTURAL']: {
        'Example 1': "How many types of symbols are there in the flowchart?",
        'Example 2': 'How many oval symbols are there in the flowchart?',
        "Example 3": "How many rectangular symbols are there in the flowchart?",
        "Example 4": "What is the color of the diamond symbol?",
        "Example 5": "What is the color of the parallelogram symbol?",
    },
    DAILY_QA_TYPES['REASONING']: {
        "Example 1": """
            What's the next step of “Put the cake in the oven”?
            A. Open the oven door.
            B. Close the oven door.
            C. Wait for the cake to bake.
            D. Take out the cake and enjoy.
        """,
        "Example 2": """
            What is the previous step of “dump all the parts on the ground”?
            A. Open the bike package.
            B. Put the parts together according to the pictures in the instructions.
            C. Check if all the screws are tightened.
            D. Get on the bike and enjoy the ride.
        """,
    }
}

def algorithm_qa_template():
    return """{
    "STRUCTURAL":[
        {
            "Q":"...",
            "A":"..."
        },
        ...
    ]
}"""


def daily_qa_template():
    return """{
    "STRUCTURAL":[
        {
            "Q":"...",
            "A":"..."
        },
        ...
    ],
    "REASONING":[
        {
            "Q":"...",
            "A":"..."
        },
        ...
    ]
}"""
