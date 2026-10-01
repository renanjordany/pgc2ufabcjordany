import sys

try:
    import tkinter as tk
    from interface_grafica import iniciar_gui
    TEM_TKINTER = True
except ImportError:
    TEM_TKINTER = False

from processador import baixar_texto_da_url, extrair_titulo_e_palavras
from motor_benchmark import executar_comparativo, formatar_relatorio

def executar_cli():
    print("Modo CLI ativado.")
    url_padrao = "https://www.gutenberg.org/cache/epub/79696/pg79696.txt"
    print(f"Baixando livro de exemplo ({url_padrao})...")
    
    texto = baixar_texto_da_url(url_padrao)
    titulo_livro, palavras = extrair_titulo_e_palavras(texto, nome_arquivo_padrao=url_padrao)
    
    print(f"Livro Identificado: {titulo_livro}")
    print(f"Total de palavras processadas (m): {len(palavras)}")
    
    resultados = executar_comparativo(palavras, epsilon=0.15, delta=0.05, num_repeticoes=10)
    relatorio = formatar_relatorio(titulo_livro, resultados, num_repeticoes=10, epsilon=0.15, delta=0.05)
    
    for linha in relatorio:
        print(linha)

if __name__ == "__main__":
    if TEM_TKINTER and len(sys.argv) == 1:
        iniciar_gui()
    else:
        executar_cli()
