from openai import OpenAI

client = OpenAI(api_key="")

response = client.chat.completions.create(
    model="gpt-4-turbo",
    messages=[
        {"role": "system", "content": "You are a helpful AI assistant."},
        {"role": "user", "content": "Explain why proprietary AI models are powerful."}
    ]
)

print(response.choices[0].message.content)
