from langchain_perplexity import ChatPerplexity
from dotenv import load_dotenv
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
import os
os.environ["LANGCHAIN_PROJECT"] = "sequential-LLM-chain"

load_dotenv()

prompt1 = PromptTemplate(
    template='Generate a detailed report on {topic}',
    input_variables=['topic']
)

prompt2 = PromptTemplate(
    template='Generate a 5 pointer summary from the following text \n {text}',
    input_variables=['text']
)

model = ChatPerplexity(model='sonar', temperature=0.7)
model2 = ChatPerplexity(model='sonar-pro', temperature=0.7)

parser = StrOutputParser()

chain = prompt1 | model | parser | prompt2 | model2 | parser

config = {
    'run_name':'sequential_chain',
    'tags': ['sequential-chain', 'llm-application'],
    'metadata': {'perplexity': 'sonar-pro', 'type': 'sequential-chain', 'author': 'waseem_akram'}
}
result = chain.invoke({'topic': 'Unemployment reasons in Pakistan?'},config=config)

print(result)
