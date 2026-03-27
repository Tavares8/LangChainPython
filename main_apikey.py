from openai import OpenAI, RateLimitError, OpenAIError
from dotenv import load_dotenv
import os

load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")

numero_dias = 7
numero_criancas = 2
atividade = "música"

prompt = f"Crie um roteiro de viagem de {numero_dias}, para uma familia com {numero_criancas} crianças, que gosta de {atividade}."

cliente = OpenAI(api_key=api_key)

try:
    resposta = cliente.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {
                "role": "system", 
                "content": "Você é um assistente de viagem especializado em criar roteiros personalizados para famílias."
            },
            {
                "role": "user", 
                "content": prompt
            }
        ]
    )
    print(resposta.choices[0].message.content)
except RateLimitError as e:
    print("\n❌ Erro: Você excedeu sua cota ou está sem saldo na OpenAI. Verifique seus detalhes de faturamento.")
except OpenAIError as e:
    print(f"\n❌ Ocorreu um erro ao comunicar com a API da OpenAI: {e}")