import tkinter as tk
from tkinter import messagebox, filedialog, ttk
from processador import extrair_titulo_e_palavras, baixar_texto_da_url
from motor_benchmark import executar_comparativo, formatar_relatorio

class InterfaceAplicativo:
    def __init__(self, raiz):
        self.raiz = raiz
        self.raiz.title("Estimador F0 - Comparativo de Algoritmos")
        self.raiz.geometry("850x740")
        self.raiz.minsize(780, 620)

        estilo = ttk.Style()
        estilo.theme_use('clam')

        painel_entrada = ttk.LabelFrame(raiz, text=" Fonte do Texto (.txt) ", padding=10)
        painel_entrada.pack(fill="x", padx=15, pady=10)

        ttk.Label(painel_entrada, text="URL do Livro (.txt):").grid(row=0, column=0, sticky="w", pady=5)
        self.entrada_url = ttk.Entry(painel_entrada, width=58)
        self.entrada_url.grid(row=0, column=1, padx=5, pady=5)
        self.entrada_url.insert(0, "https://www.gutenberg.org/cache/epub/79696/pg79696.txt")

        botao_procurar = ttk.Button(painel_entrada, text="Arquivo Local...", command=self.buscar_arquivo)
        botao_procurar.grid(row=0, column=2, padx=5, pady=5)

        painel_titulo = ttk.Frame(raiz, padding=(15, 0))
        painel_titulo.pack(fill="x")
        self.rotulo_titulo_livro = ttk.Label(
            painel_titulo, 
            text="Livro: (Aguardando processamento...)", 
            font=("Segoe UI", 10, "bold"), 
            foreground="#1a5276"
        )
        self.rotulo_titulo_livro.pack(anchor="w")

        painel_parametros = ttk.LabelFrame(raiz, text=" Parametros dos Algoritmos ", padding=10)
        painel_parametros.pack(fill="x", padx=15, pady=10)

        ttk.Label(painel_parametros, text="Epsilon:").grid(row=0, column=0, sticky="w", padx=5)
        self.entrada_epsilon = ttk.Entry(painel_parametros, width=10)
        self.entrada_epsilon.insert(0, "0.15")
        self.entrada_epsilon.grid(row=0, column=1, padx=5)

        ttk.Label(painel_parametros, text="Delta:").grid(row=0, column=2, sticky="w", padx=5)
        self.entrada_delta = ttk.Entry(painel_parametros, width=10)
        self.entrada_delta.insert(0, "0.05")
        self.entrada_delta.grid(row=0, column=3, padx=5)

        ttk.Label(painel_parametros, text="Repeticoes (N):").grid(row=0, column=4, sticky="w", padx=5)
        self.entrada_repeticoes = ttk.Entry(painel_parametros, width=10)
        self.entrada_repeticoes.insert(0, "10")
        self.entrada_repeticoes.grid(row=0, column=5, padx=5)

        self.botao_executar = ttk.Button(raiz, text="Executar Comparativo", command=self.iniciar_processo)
        self.botao_executar.pack(pady=10)

        painel_resultados = ttk.LabelFrame(raiz, text=" Resultados e Metricas ", padding=10)
        painel_resultados.pack(fill="both", expand=True, padx=15, pady=10)

        self.saida_texto = tk.Text(painel_resultados, font=("Consolas", 10), wrap="word")
        barra_rolagem_y = ttk.Scrollbar(painel_resultados, orient="vertical", command=self.saida_texto.yview)
        self.saida_texto.configure(yscrollcommand=barra_rolagem_y.set)

        barra_rolagem_y.pack(side="right", fill="y")
        self.saida_texto.pack(fill="both", expand=True)

    def buscar_arquivo(self):
        caminho_arquivo = filedialog.askopenfilename(filetypes=[("Arquivos de texto", "*.txt"), ("Todos os arquivos", "*.*")])
        if caminho_arquivo:
            self.entrada_url.delete(0, tk.END)
            self.entrada_url.insert(0, caminho_arquivo)

    def escrever_saida(self, linhas):
        self.saida_texto.delete("1.0", tk.END)
        for linha in linhas:
            self.saida_texto.insert(tk.END, linha + "\n")
        self.saida_texto.see(tk.END)

    def iniciar_processo(self):
        fonte = self.entrada_url.get().strip()
        if not fonte:
            messagebox.showerror("Erro", "Por favor, insira uma URL valida ou selecione um arquivo local.")
            return

        try:
            epsilon = float(self.entrada_epsilon.get())
            delta = float(self.entrada_delta.get())
            repeticoes = int(self.entrada_repeticoes.get())
        except ValueError:
            messagebox.showerror("Erro", "Certifique-se de que Epsilon, Delta e Repeticoes sejam numeros validos.")
            return

        self.escrever_saida(["Carregando e processando o texto, aguarde..."])
        self.raiz.update_idletasks()

        try:
            if fonte.startswith("http://") or fonte.startswith("https://"):
                texto_bruto = baixar_texto_da_url(fonte)
                referencia_arquivo = fonte
            else:
                with open(fonte, "r", encoding="utf-8", errors="ignore") as arquivo:
                    texto_bruto = arquivo.read()
                referencia_arquivo = fonte

            titulo_livro, palavras = extrair_titulo_e_palavras(texto_bruto, nome_arquivo_padrao=referencia_arquivo)
            if not palavras:
                messagebox.showwarning("Aviso", "Nenhuma palavra encontrada.")
                return

            self.rotulo_titulo_livro.config(text=f"Livro: {titulo_livro}")

            resultados = executar_comparativo(palavras, epsilon, delta, num_repeticoes=repeticoes)
            linhas_relatorio = formatar_relatorio(titulo_livro, resultados, repeticoes, epsilon, delta)
            
            self.escrever_saida(linhas_relatorio)

        except Exception as erro:
            messagebox.showerror("Erro na Execucao", f"Ocorreu um erro:\n{str(erro)}")

def iniciar_gui():
    janela = tk.Tk()
    app = InterfaceAplicativo(janela)
    janela.mainloop()