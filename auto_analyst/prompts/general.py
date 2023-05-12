import jinja2

environment = jinja2.Environment()

system_prompt = "You are a helpful assistant that determines whether a question can be answered using a SQL query, aggregation or data plot."

type_examples = [
    {"question": "How many sales were made in August?", "type": "aggregation"},
    {"question": "Relationship between customer age and time spent", "type": "plot"},
    {"question": "Query to get 1000 random customers who live in USA", "type": "query"},
    {"question": "What is the average amount per transaction?", "type": "aggregation"},
    {
        "question": "1, 7, 14, 28 retention for customer who signed up in August",
        "type": "plot",
    },
    {"question": "Plot the timeseries of ad impressions", "type": "plot"},
    {"question": "Query to get last quarters' sales", "type": "query"},
    {
        "question": "Top 10 customers by number of transactions",
        "type": "aggregation",
    },
    {"question": "Histogram of customer age", "type": "plot"},
]

type_messages = (
    [
        {"role": "system", "content": system_prompt},
    ]
    + [
        elem
        for example in type_examples
        for elem in [
            {"role": "user", "content": example["question"]},
            {"role": "assistant", "content": example["type"]},
        ]
    ],
)

def render_type_messages(question):
    return type_messages + [
        {'role':'user','content':question}
    ]