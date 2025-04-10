from langchain_ollama import OllamaLLM
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain.memory import ConversationBufferMemory
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import OpenAIEmbeddings
from langchain.text_splitter import CharacterTextSplitter

# Create crisis resources knowledge base
def create_crisis_resources_db():
    # Sample data - you would expand this with real resources
    crisis_resources = [
        "National Suicide Prevention Lifeline: 1-800-273-8255 - Available 24/7",
        "Crisis Text Line: Text HOME to 741741 - Available 24/7",
        "Dr. Sarah Johnson - Emergency Psychiatrist: 555-123-4567",
        "Dr. Michael Chen - Crisis Counselor: 555-987-6543",
        "Central Hospital Emergency Mental Health Unit: 555-333-2222"
    ]
    
    # Process documents
    text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
    docs = text_splitter.create_documents(crisis_resources)
    
    # Create vectorstore
    embeddings = OpenAIEmbeddings()
    db = Chroma.from_documents(docs, embeddings)
    return db

# Check if message contains crisis indicators
def detect_crisis(message):
    crisis_keywords = ["suicide", "kill myself", "end my life", "don't want to live", 
                     "better off dead", "no reason to live", "can't go on"]
    
    message_lower = message.lower()
    for keyword in crisis_keywords:
        if keyword in message_lower:
            return True
    return False




def get_bot_response(feeling: str, is_crisis: bool = False):
    # Setup memory
    memory = ConversationBufferMemory(memory_key="chat_history", input_key="feeling")
    
    if is_crisis:
        # Use crisis-specific template
        template = """
        You are a compassionate and supportive mental health companion.
        The user has expressed concerning thoughts that may indicate they're in crisis.
        
        The user said: "{feeling}"
        
        Respond with empathy while encouraging them to seek professional help.
        Keep your response brief but warm and supportive.
        """
        
        prompt = PromptTemplate(template=template, input_variables=["feeling"])
        llm = llm = OllamaLLM(model="gemma3:latest", temperature=0.7)
    
        # No memory for crisis responses
        chain = (
            {"feeling": lambda x: x}
            | prompt
            | llm
            | StrOutputParser()
        )
    else:
        # Regular conversation flow (your existing code)
        template = """
        You are a kind and emotionally intelligent companion and motivational.
        Here is the chat history between you and the user:
        {chat_history}
        
        The user just said: "{feeling}"
        Respond with a brief, motivating reply (max 1 sentences).
        """
        
        prompt = PromptTemplate(template=template, input_variables=["feeling", "chat_history"])
        
        # Attach memory to the chain
        chain = (
            {"feeling": lambda x: x, "chat_history": lambda _: memory.load_memory_variables({})["chat_history"]}
            | prompt
            | llm
            | StrOutputParser()
        )
    
    # Process the feeling
    result = chain.invoke(feeling)
    
    # Only save to memory for non-crisis messages
    if not is_crisis:
        memory.save_context({"feeling": feeling}, {"output": result})
    
    return result
 