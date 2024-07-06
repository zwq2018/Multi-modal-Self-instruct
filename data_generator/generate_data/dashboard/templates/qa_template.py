from enum import Enum

QA_TYPES = Enum('QA_TYPES', ['DATA_EXTRACTION', 'MATH_REASONING', 'COLOR'])

qa_types = {
    QA_TYPES['DATA_EXTRACTION']: {
        'Example 1': "What's the reading?",
        'Example 2': 'What is the range of the dashboard display?',
        "Example 3": "What is the maximum value of the range?",
        "Example 4": "What is the unit of the number shown on the dashboard?",
        "Example 5": "What's the scale value?",
        "Example 6": "What is the difference between the maximum and minimum values?",
    },
    QA_TYPES['MATH_REASONING']: {
        'Example 1': 'How long does it take to travel 100km from place A to place B at the current speed?',
        'Example 2': 'The vehicle travels at a constant speed of 10m/s, how long will it take to reach a certain odometer reading?',
        "Example 3": "The engine consumes 0.02 liters of fuel per minute at current speed, how much fuel will be consumed in an hour?",
        "Example 4": "The speed is increasing by 1m/s per second, how long will it take to reach 200m/s?",
        "Example 5": "The caliper's reading is the diameter of a cylindrical object, what is the circumference of the base of the cylinder?",
        "Example 6": "The warning rainfall is 300mm and it is increasing by 10mm per hour, how long before it reaches the warning line?",
        "Example 7": "How many more degrees do we need to raise before the water boils?",
    },
    QA_TYPES['COLOR']: {
        'Example 1': 'How many colors are there in the dashboard?',
        'Example 2': 'What is the color of the pointer? (Give in RGB format)',
        'Example 3': 'What is the color of the reading? (Give in RGB format)',
        'Example 4': 'What is the color of the scale numbers? (Give in RGB format)',
    }
}


def qa_template():
    return """{
    "DATA_EXTRACTION":[
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
    ],
    "COLOR":[
        {
            "Q":"...",
            "A":"..."
        },
        ...
    ]
}"""