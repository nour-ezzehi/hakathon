from langchain.llms import Ollama
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain.memory import ConversationBufferMemory

# Setup memory
memory = ConversationBufferMemory(memory_key="chat_history", input_key="feeling")

def get_bot_response(feeling: str):
    template = """
    You are a kind and emotionally intelligent companion and motivational.
    Here is the chat history between you and the user:
    {chat_history}

    The user just said: "{feeling}"
    Respond with a brief, motivating reply (max 1 sentences).
    """

    prompt = PromptTemplate(template=template, input_variables=["feeling", "chat_history"])

    llm = Ollama(model="gemma3:latest", temperature=0.7)

    # Attach memory to the chain
    chain = LLMChain(
        llm=llm,
        prompt=prompt,
        memory=memory
    )

    return chain.run(feeling)
