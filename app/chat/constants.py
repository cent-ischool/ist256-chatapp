TEMPERATURE=0.3
SYSTEM_PROMPT='''
Your name is Fudgebot. You're a helpful AI Python programming tutor for college students enrolled in an introductory Python programming course.
Do not answer questions that are not Python programming related, instead say "I'm sorry, I can't help with that."
Keep your answers short and simple. Make sure to provide explanations for any code you write.

Some instructions for your responses:

- Avoid `if __name__ == "__main__":` blocks in your code. Students use jupyter notebooks.
- do not write a function unless you are asked to do so.
- use f-strings for string interpolation.
- avoid the `class` keyword as students do not learn to create custom Python classes in this course.
'''


RAG_PROMPT='''
INSTRUCTIONS:
Answer the question based on the document and your understanding of Python programming. 

DOCUMENT:
{documents}

QUESTION:
{prompt}
'''
ABOUT_PROMPT='''
### What is this?
This app is an AI Tutor Bot designed for IST256, an introductory programming course in Python.
You are welcome to ask the bot course-related questions about Python programming, assignments or labs.
Like a human tutor, its here to help you learn programming concepts and apply them using the Python programming language.

### Tips For Use

- Your chat session history will restart when you are logged out.
- Try to be specific with your questions, and use terminology from the course.
- Experiment with it! Ask it questions, see what it can do.

'''

CHAT_CONVERSATION_STYLE="""
<style>
    .st-emotion-cache-janbn0 {
        flex-direction: row-reverse;
        text-align: right;
    }
</style>
"""
HIDE_MENU_STYLE = """
    <style>
        .stAppDeployButton { visibility: hidden; }
    </style>
    <style>
        .stMainMenu {visibility: hidden;}
    </style>
"""
