from dotenv import load_dotenv
from fastapi import FastAPI
from langchain.chains.summarize.refine_prompts import prompt_template
from langchain_core.messages import SystemMessage, HumanMessage
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from langserve import add_routes

load_dotenv()

model = ChatOpenAI(model='gpt-4',temperature=0.1)
# temperature: It is the ratio of creativity. If your project should be creativity, you need to increase ration.


system_prompt = "Translate the following into {language}"
prompt = ChatPromptTemplate.from_messages([
    ("system", system_prompt),
    ("human", "Translate the following sentence: {text}")
])

parser = StrOutputParser()

chain = prompt | model | parser

app = FastAPI(
    title="Translator App! ",
    description="Translate the following sentence into specified language",
    version="1.0.0"
)

add_routes(
    app,
    chain,
    path="/chain"
)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
