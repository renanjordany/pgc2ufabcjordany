import os
import re
import urllib.request

def extrair_titulo_e_palavras(texto_bruto: str, nome_arquivo_padrao: str = "") -> tuple:
    linhas = texto_bruto.splitlines()
    titulo_livro = "Titulo Nao Identificado"

    for linha in linhas:
        linha_limpa = linha.strip()
        if linha_limpa:
            titulo_livro = linha_limpa.lstrip('\ufeff')
            break

    if titulo_livro == "Titulo Nao Identificado" and nome_arquivo_padrao:
        titulo_livro = os.path.basename(nome_arquivo_padrao)

    palavras = re.findall(r'\b\w+\b', texto_bruto.lower())
    return titulo_livro, palavras

def baixar_texto_da_url(url: str) -> str:
    requisicao = urllib.request.Request(
        url, 
        headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
    )
    with urllib.request.urlopen(requisicao) as resposta:
        conteudo = resposta.read().decode('utf-8', errors='ignore')
    return conteudo