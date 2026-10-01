# Estimador de Elementos Distintos ($F_0$) - Implementação CVM

Este repositório contém uma implementação modular em Python baseada no artigo científico *"Distinct Elements in Streams: An Algorithm for the (Text) Book"* (Chakraborty, Vinodchandran e Meel), projetada para estimar a quantidade de elementos distintos ($F_0$) em fluxos de dados massivos utilizando espaço sublinear de memória.

## 📂 Estrutura do Projeto

O código foi desenvolvido de forma modular para separar responsabilidades e garantir uma arquitetura limpa:

* **`algoritmos.py`**: Contém a implementação matemática do cálculo de limiar (`thresh`) e dos dois algoritmos de estimativa (o Algoritmo 1 com detecção de falha e o Algoritmo 2 relaxado).
* **`processador.py`**: Responsável pelo download de textos via HTTP/HTTPS (como e-books do Projeto Gutenberg) ou leitura de arquivos locais, além de realizar a limpeza e tokenização do texto.
* **`motor_benchmark.py`**: Gerencia a execução das múltiplas repetições, computa o tempo de execução, desvios padrão, erros relativos e formata o relatório de desempenho.
* **`interface_grafica.py`**: Fornece uma interface gráfica intuitiva construída com `Tkinter` para configurar parâmetros e visualizar os resultados.
* **`main.py`**: O script principal que gerencia a inicialização, detectando o ambiente para abrir a interface gráfica ou rodar via linha de comando (CLI).

---

## ⚙️ Como os Algoritmos Funcionam

O sistema utiliza amostragem baseada em probabilidade para processar fluxos de dados sem precisar armazenar todos os elementos na memória RAM:

1. **Limiar de Memória (`thresh`):** O sistema calcula um limite máximo de itens que podem ser armazenados simultaneamente com base no tamanho do fluxo ($m$) e nos parâmetros de tolerância ($\epsilon$ e delta).
2. **Amostragem Probabilística:** Conforme as palavras do livro são lidas, o algoritmo mantém uma amostra usando uma taxa de probabilidade $p$. Quando o limite de memória é atingido, um sorteio descarta cerca de metade dos elementos, dobrando a taxa de amostragem.
3. **Diferença entre Algoritmo 1 e Algoritmo 2:** O Algoritmo 1 possui um mecanismo de segurança estrutural (correspondente à linha 8 do artigo) que aborta a execução caso o sorteio falhe em liberar espaço na memória. O Algoritmo 2 é a versão relaxada que omite essa verificação de falha. Na prática, como a probabilidade de falha é extremamente baixa, ambos entregam resultados altamente precisos.

---

## 🚀 Como Executar

Certifique-se de ter o Python instalado em sua máquina. O projeto utiliza apenas bibliotecas nativas do Python (`math`, `random`, `time`, `statistics`, `urllib`, `tkinter`, etc.).

Para iniciar a aplicação com a interface gráfica, execute no terminal:

```bash
python main.py
