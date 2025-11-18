import os
from groq import Groq
from dotenv import load_dotenv
load_dotenv()

groq_client = Groq()

def talk(query):
    prompt = f"""You are a helpful and friendly chatbot designed for small talk.
Answer the user **only in plain text**, do not include HTML, Markdown, or code blocks.

User question: {query}
"""

    completion = groq_client.chat.completions.create(
        model=os.environ['GROQ_MODEL'],
        messages=[  # type: ignore
            {
                'role': 'user',
                'content': prompt
            }
        ]
    )

    # The text answer
    return completion.choices[0].message.content.strip()


if __name__ == '__main__':
    print(talk('How are you today?'))

