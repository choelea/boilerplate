from app.core.config import settings
from app.schemas.message_schema import (
    IChatResponse, IUserMessage,
)
import logging
from app.utils.adaptive_cards.cards import create_adaptive_card
from app.utils.callback import (
    CustomAsyncCallbackHandler,
    CustomFinalStreamingStdOutCallbackHandler,
)
from app.utils.tools import (
    GeneralKnowledgeTool,
    ImageSearchTool,
    PokemonSearchTool,
    YoutubeSearchTool,
    GeneralWeatherTool,
)
from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from app.utils.uuid6 import uuid7
from langchain_openai import ChatOpenAI
from langchain.schema import SystemMessage
from langchain.prompts import (
    ChatPromptTemplate,
    HumanMessagePromptTemplate,
    MessagesPlaceholder,
)
from langchain.memory import ConversationBufferMemory
from langchain.chains import LLMChain
from langchain.agents import ZeroShotAgent, AgentExecutor
from app.utils.prompt_zero import zero_agent_prompt
from langchain_core.output_parsers import StrOutputParser

output_parser = StrOutputParser()

router = APIRouter()

llm = ChatOpenAI()


@router.get("/get_answer")
async def get_answer(question: str):
    chain = llm | output_parser
    res = chain.invoke(question)
    return IUserMessage(message=res)
