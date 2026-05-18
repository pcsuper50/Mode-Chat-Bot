from dotenv import load_dotenv

load_dotenv()

#from langchain.chat_models import init_chat_model
#google_genai:gemini-2.5-flash-lite
from langchain_mistralai import ChatMistralAI
from langchain_core.messages import AIMessage,SystemMessage,HumanMessage

model = ChatMistralAI(model="mistral-small-2506",temperature=0.9)

print("Choose your AI mode")
print("press 1 for angery mode")
print("press 2 for funny mode")
print("press 3 for sad mode")

choice = int(input(" Enter your choice--- "))

if choice==1:
    made = "You are an angry AI agent. You respond aggressively and impatiently"
elif choice==2:
    made = "You are a funny AI agent."
elif choice==3:
    made="You are sad AI agent, reponde like sad"
messages= [

SystemMessage(content=made)

]


print("-___________________Welcome type 0 to exit application________")
while True:
    
    promt = input("You : ")
    messages.append(HumanMessage(content=promt))
    if promt =="0":
        break
    response = model.invoke(messages)
    messages.append(AIMessage(content=response.content))
    print("Bot :" ,response.content)


print(messages)
