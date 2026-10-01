import time
import statistics
from algoritmos import (
    calcular_limiar, 
    algoritmo_1_estimador_f0, 
    algoritmo_2_relaxado, 
    contar_distintos_exato
)

def executar_comparativo(fluxo: list, epsilon: float, delta: float, num_repeticoes: int = 10):
    m = len(fluxo)
    
    tempo_inicio_exato = time.perf_counter()
    f0_exato = contar_distintos_exato(fluxo)
    tempo_exato = time.perf_counter() - tempo_inicio_exato

    tempos_alg1 = []
    estimativas_alg1 = []
    falhas_alg1 = 0

    for _ in range(num_repeticoes):
        inicio = time.perf_counter()
        resultado = algoritmo_1_estimador_f0(fluxo, epsilon, delta)
        fim = time.perf_counter()
        tempos_alg1.append(fim - inicio)
        if resultado is None:
            falhas_alg1 += 1
        else:
            estimativas_alg1.append(resultado)

    tempos_alg2 = []
    estimativas_alg2 = []

    for _ in range(num_repeticoes):
        inicio = time.perf_counter()
        resultado = algoritmo_2_relaxado(fluxo, epsilon, delta)
        fim = time.perf_counter()
        tempos_alg2.append(fim - inicio)
        estimativas_alg2.append(resultado)

    limiar = calcular_limiar(m, epsilon, delta)

    def calcular_estatisticas(tempos, estimativas):
        tempo_total = sum(tempos)
        tempo_medio = statistics.mean(tempos) if tempos else 0
        desvio_tempo = statistics.stdev(tempos) if len(tempos) > 1 else 0.0
        
        if estimativas:
            estimativa_media = statistics.mean(estimativas)
            desvio_estimativa = statistics.stdev(estimativas) if len(estimativas) > 1 else 0.0
            erro_absoluto = abs(estimativa_media - f0_exato)
            porcentagem_erro_relativo = (erro_absoluto / f0_exato) * 100 if f0_exato > 0 else 0.0
        else:
            estimativa_media, desvio_estimativa, erro_absoluto, porcentagem_erro_relativo = 0, 0, 0, 0

        return {
            "tempo_total": tempo_total,
            "tempo_medio": tempo_medio,
            "desvio_tempo": desvio_tempo,
            "estimativa_media": estimativa_media,
            "desvio_estimativa": desvio_estimativa,
            "porcentagem_erro_relativo": porcentagem_erro_relativo
        }

    estatisticas1 = calcular_estatisticas(tempos_alg1, estimativas_alg1)
    estatisticas2 = calcular_estatisticas(tempos_alg2, estimativas_alg2)

    return {
        "m": m,
        "f0_exato": f0_exato,
        "tempo_exato": tempo_exato,
        "limiar": limiar,
        "alg1": {**estatisticas1, "falhas": falhas_alg1},
        "alg2": estatisticas2
    }

def formatar_relatorio(titulo_livro: str, resultados: dict, num_repeticoes: int, epsilon: float, delta: float) -> list:
    alg1 = resultados["alg1"]
    alg2 = resultados["alg2"]
    
    relatorio = []
    relatorio.append("=" * 75)
    relatorio.append("           RELATORIO COMPARATIVO - ESTIMATIVA DE PALAVRAS DISTINTAS")
    relatorio.append("=" * 75)
    relatorio.append(f"NOME DO LIVRO                  : {titulo_livro}")
    relatorio.append("-" * 75)
    relatorio.append(f"Total de Palavras Lidas (m)    : {resultados['m']:,}")
    relatorio.append(f"Palavras Distintas Reais (F0)  : {resultados['f0_exato']:,}")
    relatorio.append(f"Parametros de Tolerancia       : epsilon = {epsilon}, delta = {delta}")
    relatorio.append(f"Limiar de Memoria (thresh)     : {resultados['limiar']:,} palavras")
    relatorio.append(f"Repeticoes para Medias (N)     : {num_repeticoes}")
    relatorio.append("-" * 75)
    relatorio.append(f"Tempo da Contagem Exata        : {resultados['tempo_exato']*1000:.3f} ms")
    relatorio.append("-" * 75)
    
    relatorio.append("\n[ ALGORITMO 1: Estimador F0 (Com deteccao de falha) ]")
    relatorio.append(f"  * Tempo Medio por Execucao   : {alg1['tempo_medio']*1000:.3f} ms")
    relatorio.append(f"  * Palavras Distintas (Est.)  : {alg1['estimativa_media']:.2f}")
    relatorio.append(f"  * Desvio Padrao da Estimativa: {alg1['desvio_estimativa']:.2f}")
    relatorio.append(f"  * Erro Relativo Medio        : {alg1['porcentagem_erro_relativo']:.2f}%")
    relatorio.append(f"  * Falhas Ocorridas           : {alg1['falhas']} de {num_repeticoes}")

    relatorio.append("\n[ ALGORITMO 2: Estimador Relaxado (Sem aborto) ]")
    relatorio.append(f"  * Tempo Medio por Execucao   : {alg2['tempo_medio']*1000:.3f} ms")
    relatorio.append(f"  * Palavras Distintas (Est.)  : {alg2['estimativa_media']:.2f}")
    relatorio.append(f"  * Desvio Padrao da Estimativa: {alg2['desvio_estimativa']:.2f}")
    relatorio.append(f"  * Erro Relativo Medio        : {alg2['porcentagem_erro_relativo']:.2f}%")
    relatorio.append("=" * 75)
    
    return relatorio