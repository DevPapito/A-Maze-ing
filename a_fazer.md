# Resumo do Projeto e Status de Desenvolvimento (A-Maze-ing)

## 1. Resumo do Projeto (`README.md` e `pt.subject.md`)

O projeto **A-Maze-ing** (parte do currículo da 42, desenvolvido por `jzampier` e `pezio`) consiste em desenvolver um gerador e solucionador de labirintos robusto em Python 3.10+. 

**Principais Requisitos e Funcionalidades:**
- **Configuração via Arquivo (`config.txt`):** Lê parâmetros obrigatórios (`WIDTH`, `HEIGHT`, `ENTRY`, `EXIT`, `OUTPUT_FILE`, `PERFECT`).
- **Dois Modos de Labirinto:**
  - **Perfeito (`PERFECT=True`):** Apenas um caminho único entre entrada e saída (sem loops, árvore geradora mínima).
  - **Estilo Pac-Man (`PERFECT=False`):** Múltiplos loops, cantos e centro abertos, padrão "42" desenhado com células fechadas, corredores com largura máxima de 2 células e poucos/nenhum beco sem saída.
- **Representação de Paredes (Hexadecimal):** Cada célula codifica suas paredes (Norte, Leste, Sul, Oeste) em um dígito hexadecimal (0-F) usando um bitmask de 4 bits.
- **Solucionador (Shortest Path):** Computa e exporta a rota ótima (`N`, `E`, `S`, `W`) da entrada à saída.
- **Visualização:** Renderização ASCII no terminal ou gráfica (MiniLibX), com interatividade (regenerar, alternar exibição do caminho, mudar cores).
- **Reutilização de Código:** O gerador deve ser empacotado em um módulo reutilizável (`mazegen-*` `.whl` ou `.tar.gz`) na raiz do repositório, acompanhado de `LICENSE.md` e documentação.
- **Qualidade de Código:** Conformidade estrita com `flake8` e verificação de tipos estáticos com `mypy`, além de tratamento robusto de exceções e `Makefile` automatizado.

---

## 2. O que já foi feito

1. **Automação e Ambiente (`Makefile` & `requirements.txt`):**
   - Regras para criar ambiente virtual (`venv`), instalar dependências (`pandas`, etc.), rodar, depurar (`pdb`), limpar caches (`clean`), e linting (`flake8` e `mypy`).
2. **Parser e Validação de Configuração (`a_maze_ing/parse/`):**
   - Validação rigorosa de argumentos de linha de comando (`argument_validate`).
   - Verificação de existência e permissões do arquivo `config.txt` (`file_validate`).
   - Lexer e interpretador robustos para ler pares `CHAVE=VALOR`, ignorar comentários (`#`), validar sintaxe e detectar chaves duplicadas (`config_interpretor.py`).
   - Parser completo que valida chaves obrigatórias, converte tipos (`int`, `float`, `bool`) e retorna um objeto estruturado `Config` (`parser.py`).
   - Exceções personalizadas de parsing (`exceptions_parser.py`).
3. **Estrutura Base do Gerador de Labirintos (`a_maze_ing/maze_interpretor/`):**
   - Classe de DTO `Cell` (coordenadas `x`, `y`, `walls` inicializadas como `15`/todos os muros fechados, e `passed`).
   - Classe `MazeGenerator` inicializada com a configuração e responsável por instanciar a matriz bidimensional da grade (`self._grid`).
4. **Ponto de Entrada Principal (`a_maze_ing/a_maze_ing.py`):**
   - Script principal integrando o parser e inicializando o gerador de labirintos.

---

## 3. O que ainda falta ser feito

1. **Algoritmo de Geração de Labirintos:**
   - Implementar o algoritmo de geração (ex: *Recursive Backtracker*, Prim ou Kruskal) que construa o labirinto respeitando o modo (`PERFECT=True` ou `PERFECT=False`).
   - Garantir a coerência das paredes entre células vizinhas.
   - Implementar a lógica para desenhar o padrão "42" (células fechadas) e abrir cantos/centro no modo Pac-Man.
2. **Solucionador de Caminho (Pathfinding):**
   - Implementar o algoritmo de busca do caminho mais curto (ex: BFS / A*) da entrada (`ENTRY`) até a saída (`EXIT`) e gerar a string de direções (`N`, `E`, `S`, `W`).
3. **Geração do Arquivo de Saída:**
   - Escrever no `OUTPUT_FILE` o grid em formato hexadecimal linha por linha, seguido de linha em branco, coordenadas de entrada, de saída e o caminho mais curto.
4. **Visualização e Interatividade:**
   - Desenvolver a renderização visual em ASCII (no terminal) ou gráfica (MLX) com suporte a interações (regeneração, exibir/ocultar caminho, mudança de cores).
5. **Empacotamento e Documentação (Requisito Reutilizável):**
   - Criar o pacote Python reutilizável `mazegen-*` (.whl / .tar.gz) na raiz do projeto.
   - Adicionar o arquivo `LICENSE.md`.
   - Escrever a documentação de uso do módulo `MazeGenerator`.
6. **Testes Unitários e README Final:**
   - Adicionar suíte de testes unitários (com `pytest` ou `unittest`).
   - Completar o `README.md` com todas as seções obrigatórias da 42.
