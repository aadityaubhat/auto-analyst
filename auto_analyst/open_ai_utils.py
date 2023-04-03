import openai
from config import OPENAI_API_KEY
from prompts import (
    render_agg_plot_prompt,
    render_analytical_prompt,
    render_data_prompt,
)


openai.api_key = OPENAI_API_KEY


def get_chat_reply(system_prompt, prompt):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": prompt},
            ],
        temperature=0.1,
        )
    
    return response['choices'][0]['message']['content'].strip().lower()

