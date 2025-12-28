VERSION="2.0.0"
TITLE="IST256 AI"
LOGO="chat/images/ai-platform.svg"
USER_ICON="chat/images/question.svg"
ASSISTANT_AZURE_NORAG_ICON="chat/images/assistant-azure-norag.svg"
ASSISTANT_AZURE_RAG_ICON="chat/images/assistant-azure-rag.svg"
ASSISTANT_OLLAMA_NORAG_ICON="chat/images/assistant-ollama-norag.svg"
ASSISTANT_OLLAMA_RAG_ICON="chat/images/assistant-ollama-rag.svg"
ASSISTANT_ICONS = [
    ASSISTANT_AZURE_NORAG_ICON,
    ASSISTANT_AZURE_RAG_ICON,
    ASSISTANT_OLLAMA_NORAG_ICON,
    ASSISTANT_OLLAMA_RAG_ICON
]

MODES = ["Tutor", "Answer"]
MODE_HELP ="Mode selection chooses how the AI will behave."
MODE_CAPTIONS = [
    "AI provides guided learning like a tutor.", 
    "AI provides direct answers to your prompts."
]

CONTEXT_HELP = "Context Selection pre-loads the assignment or lab into the AI so its knowledgeable of the content."

# SYSTEM_PROMPT='''
# Your name is Fudgebot. You're a helpful AI Python programming tutor for college 
# students enrolled in an introductory Python programming course.
# You can talk about yourself and your capabilities.
# You can try to help with programming assignments and labs.
# Do not answer questions that are not Python programming or course related.
# Keep your answers short and simple. Make sure to provide explanations for any code you write.

# Some instructions for your code responses:

# - Avoid `if __name__ == "__main__":` blocks in your code. Students use jupyter notebooks.
# - do not write a function unless you are asked to do so.
# - use f-strings for string interpolation.
# - avoid the `class` keyword as students do not learn to create custom Python classes in this course.
# '''
CONTEXT_PROMPT_TEMPLATE='''
You are assisting with the assignment: {assignment}

Here is the full assignment content:

{content}

---

'''
# CONTEXT_PROMPT_TEMPLATE_NO_CONTENT='''
# I would like to ask you questions about the assignment: {assignment}. 
# Please acknowledge that you are ready to answer questions about this assignment.
# '''


# RAG_PROMPT_TEMPLATE='''
# INSTRUCTIONS:
# Answer the question based on the document and your understanding of Python programming. 
# If you write python code, make sure to explain what it does.

# DOCUMENT:
# {documents}

# QUESTION:
# {query}
# '''
ABOUT_PROMPT='''
### What is this?
This app is an AI Tutor Bot designed for IST256, an introductory programming course in Python.
You are welcome to ask the bot course-related questions about Python programming, assignments or labs.
Like a human tutor, its here to help you learn programming concepts and apply them using the Python programming language.

### Tips

- The bot will remmeber things said in your conversation.
- Select a context to talk about a lab or homework, "General Python" for everything else.
- When you switch conxtexts, your chat history/memory will be cleared.
- Your chat history/memory will be cleared when you hard-refresh the page or logout.
- Try to be specific with your questions, and use terminology from the course.
- Experiment with it! Ask it questions, see what it can do.

-----
'''

TIPS_TEXT = """
### Tips for Using the AI Tutor

- **Choose Your Mode**: Tutor mode guides you to learn, Answer mode gives direct solutions
- **Select Context**: Pick an assignment/lab to get specific help, or use "General Python" for anything
- **Ask Specific Questions**: The AI works best with clear, detailed questions
- **Iterate**: If the answer isn't helpful, rephrase your question or ask for clarification
- **Session Memory**: The AI remembers your conversation until you change mode/context
"""

FAQ_TEXT = """
### Frequently Asked Questions

**Q: Why did my chat history disappear?**
A: Chat history clears when you change Mode or Context, logout, or refresh the page.

**Q: Can the AI see my assignment?**
A: Yes! When you select a specific assignment/lab, the full content is automatically loaded.

**Q: What's the difference between Tutor and Answer modes?**
A: Tutor mode uses Socratic teaching (guides you with questions), Answer mode provides direct solutions.

**Q: Can I download my conversation?**
A: Yes! Expand "AI Mode/Context" at the bottom. Click "Download Chat" for this session or "Download All" for all your sessions.

**Q: Is my data private?**
A: Conversations are logged to a secure database for course improvement. Only instructors can access logs.
"""

UNAUTHORIZED_MESSAGE = """
You are not authorized to access this application.

If you are enrolled in IST256 for the current semester, please contact your instructor
(mafudge@syr.edu) with your SU email address to request access.
"""

CHAT_CONVERSATION_STYLE="""
<style>
    .st-emotion-cache-janbn0 {
        flex-direction: row-reverse;
        text-align: right;
    }
</style>
"""

CHAT_CONVERSATION_STYLE2="""
<style>
    .st-emotion-cache-1mph9ef {
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


