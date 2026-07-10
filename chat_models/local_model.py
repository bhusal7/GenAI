# to use model locally bcz Deepseek api isnot for unllimmited so,

from langchain_huggingface import ChatHuggingFace, HuggingFacePipeline

llm = HuggingFacePipeline.from_model_id(
    model_id = "devlocalhost/hi-tinylama-gguf-16bit",
    task="text-generation",
    pipeline_kwargs=dict(
        max_new_tokens=512,
        do_sample=False,
        repetition_penalty=1.03,
    )
)

chat_model = ChatHuggingFace(llm = llm)

response = chat_model.invoke("what is data science?")
print(response.content)