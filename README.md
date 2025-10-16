# Labirinto de Creta - Simulador

Simulação da travessia do labirinto de Creta, onde um prisioneiro tenta escapar enquanto é caçado pelo Minotauro.

## 🚀 Como Executar (FÁCIL!)

### Opção 1: Execução Automática (Recomendada)
**Windows:**
- Clique duas vezes no arquivo `executar.bat`

**Linux/Mac:**
- Abra o terminal na pasta do projeto
- Execute: `chmod +x executar.sh && ./executar.sh`

### Opção 2: Execução Manual
1. **Pré-requisitos:**
   - Python 3.6 ou superior instalado
   - Nenhuma biblioteca adicional necessária!

2. **Instruções:**
   ```bash
   cd src
   python main.py
   ```

### Arquivo de Entrada
O programa lê os dados do arquivo `entradas/input.txt` no formato:
- Linha 1: número de vértices
- Linha 2: número de arestas  
- Próximas linhas: arestas no formato `u v peso`
- Linha n+3: vértice de entrada
- Linha n+4: vértice de saída
- Linha n+5: posição inicial do minotauro
- Linha n+6: parâmetro de percepção
- Linha n+7: tempo máximo de duração do alimento

### Saída
O programa gera:
- Logs detalhados da simulação no console
- Arquivo `relatorio.txt` com resumo completo da simulação

## Estrutura do Projeto
- `main.py`: Função principal e lógica da simulação
- `graph.py`: Implementação do grafo e algoritmo de Dijkstra
- `entities.py`: Classes Prisioneiro e Minotauro
- `entradas/input.txt`: Arquivo de entrada com dados do labirinto

## Algoritmos Utilizados
- **Dijkstra**: Para cálculo de caminhos mínimos (O((V+E)log V))
- **Estruturas de dados**: Sets, heaps e dicionários para eficiência
## Vídeos e Equipe

- Integrantes da equipe: <NOME 1> (<MATRÍCULA>), <NOME 2> (<MATRÍCULA>), <NOME 3> (<MATRÍCULA>)
- Links para vídeos de explicação (um por participante):
  - <NOME 1>: <URL_DO_VÍDEO>
  - <NOME 2>: <URL_DO_VÍDEO>
  - <NOME 3>: <URL_DO_VÍDEO>
