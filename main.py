from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser, JsonOutputParser
from pydantic import Field, BaseModel
from dotenv import load_dotenv
from langchain.globals import set_debug
import os

set_debug(True)

load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")

class Destino(BaseModel):
    cidade: str = Field("A cidade sugerida para visitar")
    motivo: str = Field("O motivo pelo qual a cidade é uma boa escolha para visitar")

class Restaurantes(BaseModel):
    cidade: str = Field("A cidade sugerida para visitar")
    restaurantes: str = Field("Restaurantes recomendados na cidade sugerida")
    
parseador_destino = JsonOutputParser(pydantic_object=Destino)
parseador_restaurantes = JsonOutputParser(pydantic_object=Restaurantes)

prompt_cidade = PromptTemplate(
    template="""
    Sugira uma cidade dado o meu interesse por {interesse}.
    {formato_de_saida}
    """,
    input_variables=["interesse"],
    partial_variables={"formato_de_saida": parseador_destino.get_format_instructions()}
) 

prompt_restaurantes = PromptTemplate(
    template="""
    Sugira restaurantes na cidade de {cidade}.
    {formato_de_saida}
    """,
    partial_variables={"formato_de_saida": parseador_restaurantes.get_format_instructions()}
) 

prompt_cultural = PromptTemplate(
    template="""
    Sugira atrações culturais na cidade de {cidade}.
    """
)

modelo = ChatOpenAI(model="gpt-3.5-turbo", 
                    temperature=0.5, 
                    openai_api_key=api_key
) # posso usar qquer llm aqui, mas vou usar o chatgpt


cadeia1 = prompt_cidade | modelo | parseador_destino
cadeia2 = prompt_restaurantes | modelo | parseador_restaurantes
cadeia3 = prompt_cultural | modelo | StrOutputParser()

cadeia = cadeia1 | cadeia2 | cadeia3

resposta = cadeia.invoke(
    {
        "interesse": "praia"
    }
) 
print(resposta)