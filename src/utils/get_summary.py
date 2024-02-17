from openai import OpenAI
client = OpenAI(api_key="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")

def get_summary(transcript):
    completion = client.chat.completions.create(
    model="gpt-3.5-turbo-0125",
    messages=[
        {"role": "system", "content": "Summarize in 50 words."},
        {"role": "user", "content": f"{transcript}"}
    ]
    )

    return completion.choices[0].message.content

