from graph import Graph
from entities import Prisioneiro, Minotauro
import random

def ler_entrada(filePath="entradas/input.txt"):
    try:
        with open(filePath, 'r', encoding='utf-8') as file:
            lines = file.readlines()
            
        lines = [line.strip() for line in lines if line.strip()]
        
        n = int(lines[0])
        m = int(lines[1])
        
        edges = []
        for i in range(2, 2 + m):
            u, v, w = map(int, lines[i].split())
            edges.append((u, v, w))
        
        entrada = int(lines[2 + m])
        saida = int(lines[3 + m])
        pos_minotauro = int(lines[4 + m])
        percepcao = int(lines[5 + m])
        tempo_max = int(lines[6 + m])
        
        g = Graph.from_txt_format(n, edges, entrada, saida)
        
        p = Prisioneiro(entrada)
        m = Minotauro(pos_minotauro, percepcao, g)
        
        dados = {
            'tempo_maximo': tempo_max
        }
        
        return g, p, m, dados
        
    except FileNotFoundError:
        print(f"Erro: O arquivo '{filePath}' não foi encontrado.")
        return None, None, None, None
    except (ValueError, IndexError) as e:
        print(f"Erro: Formato do arquivo inválido. {e}")
        return None, None, None, None

def simular_batalha():
    return random.random() < 0.01  

def gerar_relatorio(prisioneiro, minotauro: Minotauro, tempo_restante, resultado):
    relatorio = []
    relatorio.append("=== RELATÓRIO DA SIMULAÇÃO ===\n")
    
 
    if resultado == "escapou":
        relatorio.append("O prisioneiro conseguiu escapar!")
    elif resultado == "morreu_batalha":
        relatorio.append("O prisioneiro morreu em batalha com o minotauro.")
    elif resultado == "morreu_fome":
        relatorio.append("O prisioneiro morreu de fome.")
    elif resultado == "venceu_batalha":
        relatorio.append("O prisioneiro venceu o minotauro em batalha!")
    
    relatorio.append(f"Tempo restante: {tempo_restante} rodadas\n")
    
 
    relatorio.append("Trajetória do prisioneiro:")
    relatorio.append(" -> ".join(map(str, prisioneiro.trajetoria)))
    relatorio.append("")
    
    if minotauro.findMoment is not None:
        relatorio.append(f"Minotauro detectou o prisioneiro na rodada {minotauro.findMoment}")
        relatorio.append("Trajetória do minotauro durante perseguição:")
        relatorio.append(" -> ".join(map(str, minotauro.chasePath)))
    else:
        relatorio.append("Minotauro não detectou o prisioneiro")
    
    relatorio.append("")
    relatorio.append("Estatísticas:")
    relatorio.append(f"   - Vértices visitados pelo prisioneiro: {len(prisioneiro.visitados)}")
    relatorio.append(f"   - Arestas percorridas pelo prisioneiro: {len(prisioneiro.arestas)}")
    relatorio.append(f"   - Total de movimentos do prisioneiro: {len(prisioneiro.trajetoria) - 1}")
    
    return "\n".join(relatorio)

def simular_labirinto():
    g, p, m, dados = ler_entrada()
    
    if g is None or p is None or m is None or dados is None:
        print("Erro: Não foi possível carregar os dados de entrada.")
        return None

    tempo_max = dados['tempo_maximo']
    
    tempo = tempo_max
    rodada = 0
    resultado = None
    
    print("Iniciando simulação do Labirinto de Creta...")
    print(f"Prisioneiro inicia na posição {g.getEntry()}")
    print(f"Minotauro inicia na posição {m.startPosition}")
    print(f"Saída do labirinto: posição {g.getExit()}")
    print(f"Tempo máximo: {tempo_max} rodadas")
    print(f"Percepção do minotauro: {m.perception}")
    print("-" * 50)
    
    while tempo > 0 and p.vivo and not p.escapou:
        rodada += 1
        print(f"\nRodada {rodada} (Tempo restante: {tempo})")
        
        print(f"Prisioneiro está na posição {p.pos}")
        
        prox = p.escolher_proximo_movimento(g)
        if prox is not None:
            p.mover_para(prox)
            print(f"Prisioneiro moveu para {p.pos}")

        if prox is None:
            print("Prisioneiro está preso e não pode se mover.")

        if p.pos == g.getExit():
            p.escapou = True
            resultado = "escapou"
            break
        
        print(f"Minotauro está na posição {m.actualPosition}")
        
        m.move(p.pos)
        
        if m.inChase and m.findMoment is None: 
            print(f"Minotauro perseguiu até {m.actualPosition}")
            m.findMoment = rodada
        else: 
            print(f"Minotauro moveu para {m.actualPosition}")
     
        if p.pos == m.actualPosition:
            print("BATALHA! Prisioneiro e minotauro se encontraram!")
            if simular_batalha():
                print("Milagre! O prisioneiro venceu a batalha!")
                resultado = "venceu_batalha"
                
            else:
                print("O prisioneiro foi derrotado pelo minotauro.")
                p.vivo = False
                resultado = "morreu_batalha"
                break
        
        tempo -= 1
    
    if tempo <= 0 and not p.escapou and p.vivo:
        resultado = "morreu_fome"
        print("\nO prisioneiro morreu de fome.")

    if resultado is None:
        resultado = "indefinido"

    relatorio = gerar_relatorio(p, m, tempo, resultado)
    print("\n" + relatorio)
    
    with open("relatorio.txt", "w") as f:
        f.write(relatorio)
    
    print("\nRelatório salvo em 'relatorio.txt'")
    return resultado

if __name__ == "__main__":
    simular_labirinto()
  