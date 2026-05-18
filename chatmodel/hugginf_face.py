# from langchain_huggingface import ChatHuggingFace, HuggingFaceEndpoint

# llm = HuggingFaceEndpoint(
#     repo_id="deepseek-ai/DeepSeek-R1"
# )

# model = ChatHuggingFace(llm=llm)

# response = model.invoke("Who are you")

# print(response.content)

from dotenv import load_dotenv
from langchain_huggingface import ChatHuggingFace, HuggingFaceEndpoint

load_dotenv()

llm = HuggingFaceEndpoint(
    repo_id="deepseek-ai/DeepSeek-R1",
    temperature=0.7,
    max_new_tokens=500
)

model = ChatHuggingFace(llm=llm)

response = model.invoke("Who are you")

print(response.content)