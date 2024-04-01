import os
import re
from dotenv import load_dotenv
from typing import Any, Callable, Dict, List, Union
from langchain.chains import LLMChain, RetrievalQA
from langchain.prompts import PromptTemplate
from langchain_core.language_models.llms import BaseLLM
from pydantic import Field
from langchain.chains.base import Chain
from langchain.prompts.base import StringPromptTemplate
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from time import sleep
from langchain_community.document_loaders import TextLoader
from langchain_community.vectorstores import Chroma
from langchain.agents import AgentExecutor, LLMSingleActionAgent, Tool
from langchain.agents.agent import AgentOutputParser
from langchain.agents.conversational.prompt import FORMAT_INSTRUCTIONS
from langchain.schema import AgentAction, AgentFinish
from langchain_text_splitters import RecursiveCharacterTextSplitter



load_dotenv()
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')