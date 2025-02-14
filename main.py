from typing import Optional, Union

from fastapi import FastAPI, Form, Query, Request
from fastapi.responses import HTMLResponse
import markdown2
from pydantic import BaseModel

# views.py (exemplo básico - atualizado para Perplexity)

from service_rag import rag_function_perplexity # Importe a função RAG da Perplexity AI
from fastapi.templating import Jinja2Templates

templates = Jinja2Templates(directory="templates")

class Item(BaseModel):
    user_query: str


app = FastAPI()


@app.get("/items", response_class=HTMLResponse)
async def minha_view_rag_perplexity(request: Request):
    return templates.TemplateResponse("template_da_sua_view.html", {'request': request})

@app.post("/items", response_class=HTMLResponse)
async def minha_view_rag_perplexity(request: Request, user_query: str = Form(...)):
    """
    View para processar perguntas do usuário usando RAG com Perplexity API.

    - item_id: Identificador do item (pode ser usado para identificar um contexto específico, se necessário).
    - user_query (opcional): A pergunta do usuário, passada como query parameter.
    """
    resposta_rag = "" # Inicializa a resposta RAG como vazia

    if user_query: # Verifica se o user_query foi fornecido
        documentos_fonte = [
            "Python é uma linguagem de programação de alto nível, interpretada, de propósito geral e muito popular.",
            "Uma das características do Python é a sua legibilidade, o que significa que o código Python é fácil de ler e entender.",
            "Tipos de dados básicos em Python incluem inteiros (int), números de ponto flutuante (float), strings (str) e booleanos (bool).",
            "Listas em Python são coleções ordenadas e mutáveis de itens, escritas com colchetes [].",
            "Tuplas são coleções ordenadas e imutáveis de itens, escritas com parênteses ().",
            "Dicionários em Python são coleções não ordenadas, mutáveis e indexadas de itens, escritos com chaves {}.",
            "Estruturas de controle de fluxo em Python incluem 'if', 'elif', 'else' para decisões e 'for' e 'while' para loops.",
            "Funções em Python são blocos de código reutilizáveis definidos com a palavra-chave 'def'.",
            "Módulos em Python são arquivos contendo definições e declarações Python. Você pode importar módulos para reutilizar código.",
            "O tratamento de exceções em Python é feito com blocos 'try', 'except', 'finally' para lidar com erros de forma elegante.",
            "Python suporta programação orientada a objetos (POO) com classes e objetos.",
            "Virtual environments em Python são usados para criar ambientes isolados para projetos, gerenciando dependências separadamente.",
            "Pip é o gerenciador de pacotes padrão para Python, usado para instalar e gerenciar bibliotecas e dependências.",
            "F-strings em Python (a partir da versão 3.6) são uma forma concisa e legível de formatar strings, usando f'...'."
        ]
        perplexity_api_key = "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" # **Configure sua chave API aqui (ou melhor, em variáveis de ambiente)**

        resposta_rag = rag_function_perplexity(user_query, documentos_fonte, perplexity_api_key) # Chama a função RAG da Perplexity
        resposta_rag_html = markdown2.markdown(resposta_rag)

    return templates.TemplateResponse("template_da_sua_view.html", {'pergunta': user_query, 'resposta_rag': resposta_rag_html, 'request': request})