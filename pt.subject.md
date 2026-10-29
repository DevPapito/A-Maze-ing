<p align="center">
  <b>A-Maze-ing</b><br>
  <i>Este é o caminho</i>
</p>

<p align="center">
  <b>Resumo:</b> Crie seu próprio gerador de labirintos e exiba seu resultado!<br>
  <b>Versão:</b> 2.3
</p>

---

## Sumário

- [I. Prefácio](#i-prefácio)
- [II. Instruções de IA](#ii-instruções-de-ia)
- [III. Instruções Comuns](#iii-instruções-comuns)
  - [III.1 Regras Gerais](#iii1-regras-gerais)
  - [III.2 Makefile](#iii2-makefile)
  - [III.3 Diretrizes Adicionais](#iii3-diretrizes-adicionais)
- [IV. Parte Obrigatória](#iv-parte-obrigatória)
  - [IV.1 Resumo](#iv1-resumo)
  - [IV.2 Uso](#iv2-uso)
  - [IV.3 Formato do arquivo de configuração](#iv3-formato-do-arquivo-de-configuração)
  - [IV.4 Requisitos do Labirinto](#iv4-requisitos-do-labirinto)
  - [IV.5 Formato do Arquivo de Saída](#iv5-formato-do-arquivo-de-saída)
- [V. Representação Visual](#v-representação-visual)
- [VI. Requisitos de Reutilização de Código](#vi-requisitos-de-reutilização-de-código)
- [VII. Requisitos do Readme](#vii-requisitos-do-readme)
- [VIII. Bônus](#viii-bônus)
- [IX. Submissão e Avaliação por Pares](#ix-submissão-e-avaliação-por-pares)

---

## Capítulo I
### Prefácio

Labirintos fascinam os seres humanos há milhares de anos. Do lendário Labirinto de Cnossos na mitologia grega, construído por Dédalo para aprisionar o Minotauro, aos livros de quebra-cabeças modernos e videogames, os labirintos sempre simbolizaram mistério, desafio e design inteligente. Na ciência da computação, a geração de labirintos é mais do que apenas diversão: é uma aplicação prática de algoritmos, aleatoriedade e teoria dos grafos. Alguns algoritmos famosos usados para geração de labirintos, como o de Prim, Kruskal ou o *recursive backtracker*, também são usados em problemas do mundo real, como design de redes ou geração procedural de conteúdo. Curiosamente, labirintos perfeitos (com um caminho único entre quaisquer dois pontos) estão diretamente relacionados a árvores geradoras mínimas (*spanning trees*) na teoria dos grafos. Construir um labirinto, especialmente um que você possa visualizar e compartilhar, é uma ótima maneira de explorar como os computadores podem criar estrutura a partir do caos, e se divertir um pouco no processo.

> *"Um labirinto não é um lugar para se perder, mas um caminho a ser encontrado."*
> - Anônimo

---

## Capítulo II
### Instruções de IA

#### ● Contexto
Durante sua jornada de aprendizado, a IA pode ajudar em muitas tarefas diferentes. Aproveite o tempo para explorar as várias capacidades das ferramentas de IA e como elas podem apoiar o seu trabalho. No entanto, sempre aborde-as com cautela e avalie criticamente os resultados. Seja código, documentação, ideias ou explicações técnicas, você nunca pode ter certeza absoluta de que sua pergunta foi bem formulada ou de que o conteúdo gerado é preciso. Seus colegas são um recurso valioso para ajudá-lo a evitar erros e pontos cegos.

#### ● Mensagem Principal
- ☛ Use IA para reduzir tarefas repetitivas ou tediosas.
- ☛ Desenvolva habilidades de *prompt* — tanto de código quanto não relacionadas a código — que beneficiarão sua futura carreira.
- ☛ Aprenda como os sistemas de IA funcionam para antecipar e evitar melhor riscos comuns, vieses e questões éticas.
- ☛ Continue construindo habilidades técnicas e comportamentais (*power skills*) trabalhando com seus colegas.
- ☛ Use apenas conteúdo gerado por IA que você compreenda totalmente e pelo qual possa assumir responsabilidade.

#### ● Regras do Aluno:
- Você deve reservar um tempo para explorar as ferramentas de IA e entender como elas funcionam, para poder usá-las eticamente e reduzir potenciais vieses.
- Você deve refletir sobre seu problema antes de criar um *prompt* — isso ajuda a escrever *prompts* mais claros, detalhados e relevantes usando um vocabulário preciso.
- Você deve desenvolver o hábito de verificar, revisar, questionar e testar sistematicamente qualquer coisa gerada por IA.
- Você deve sempre buscar revisão por pares — não confie apenas na sua própria validação.

#### ● Resultados da Fase:
- Desenvolver habilidades de *prompt* de uso geral e específicas de domínio.
- Aumentar sua produtividade com o uso eficaz de ferramentas de IA.
- Continuar fortalecendo o pensamento computacional, resolução de problemas, adaptabilidade e colaboração.

#### ● Comentários e Exemplos:
- Você encontrará regularmente situações — exames, avaliações e mais — onde deve demonstrar compreensão real. Esteja preparado, continue construindo suas habilidades técnicas e interpessoais.
- Explicar seu raciocínio e debater com colegas frequentemente revela lacunas na sua compreensão. Faça do aprendizado entre pares uma prioridade.
- Ferramentas de IA frequentemente carecem do seu contexto específico e tendem a fornecer respostas genéricas. Seus colegas, que compartilham seu ambiente, podem oferecer insights mais relevantes e precisos.
- Onde a IA tende a gerar a resposta mais provável, seus colegas podem fornecer perspectivas alternativas e nuances valiosas. Confie neles como um ponto de verificação de qualidade.

**✓ Boa prática:**
> Eu pergunto à IA: “Como eu testo uma função de ordenação?” Ela me dá algumas ideias. Eu as experimento e reviso os resultados com um colega. Refinamos a abordagem juntos.

**✗ Má prática:**
> Eu peço à IA para escrever uma função inteira, copio e colo no meu projeto. Durante a avaliação por pares, não consigo explicar o que ela faz ou por quê. Perco credibilidade — e reprovo no meu projeto.

**✓ Boa prática:**
> Uso a IA para me ajudar a desenhar um *parser*. Depois, percorro a lógica com um colega. Encontramos dois bugs e reescrevemos juntos — melhor, mais limpo e totalmente compreendido.

**✗ Má prática:**
> Deixo o Copilot gerar meu código para uma parte fundamental do meu projeto. Ele compila, mas não sei explicar como ele lida com *pipes*. Durante a avaliação, não consigo justificar e reprovo no projeto.

---

## Capítulo III
### Instruções Comuns

#### III.1 Regras Gerais
- Seu projeto deve ser escrito em **Python 3.10 ou superior**.
- Seu projeto deve aderir ao padrão de codificação **flake8**.
- Suas funções devem tratar exceções de forma graciosa para evitar falhas (*crashes*). Use blocos `try-except` para gerenciar erros potenciais. Prefira gerenciadores de contexto para recursos como arquivos ou conexões para garantir limpeza automática. Se seu programa falhar devido a exceções não tratadas durante a avaliação, ele será considerado não funcional.
- Todos os recursos (ex.: manipuladores de arquivos, conexões de rede) devem ser gerenciados adequadamente para evitar vazamentos. Use gerenciadores de contexto sempre que possível.
- Seu código deve incluir dicas de tipos (*type hints*) para parâmetros de funções, tipos de retorno e variáveis onde aplicável (usando o módulo `typing`). Use `mypy` para verificação estática de tipos. Todas as funções devem passar no `mypy` sem erros.
- Inclua *docstrings* em funções e classes seguindo o padrão **PEP 257** (ex.: estilo Google ou NumPy) para documentar propósito, parâmetros e retornos.

#### III.2 Makefile
Inclua um `Makefile` em seu projeto para automatizar tarefas comuns. Ele deve conter as regras a seguir (o lint obrigatório implica as flags especificadas; é altamente recomendável testar `--strict` para verificação avançada):
- `install`: Instala as dependências do projeto usando `pip`, `uv`, `pipx` ou outro gerenciador de pacotes de sua escolha.
- `run`: Executa o script principal do seu projeto (ex.: via interpretador Python).
- `debug`: Executa o script principal em modo de depuração usando o depurador embutido do Python (`pdb`).
- `clean`: Remove arquivos temporários ou caches (ex.: `__pycache__`, `.mypy_cache`) para manter o ambiente do projeto limpo.
- `lint`: Executa os comandos `flake8 .` e `mypy . --warn-return-any --warn-unused-ignores --ignore-missing-imports --disallow-untyped-defs --check-untyped-defs`.
- `lint-strict` (opcional): Executa os comandos `flake8 .` e `mypy . --strict`.

#### III.3 Diretrizes Adicionais
- Crie programas de teste para verificar a funcionalidade do projeto (não submetidos ou avaliados). Use frameworks como `pytest` ou `unittest` para testes unitários, cobrindo casos limite (*edge cases*).
- Inclua um arquivo `.gitignore` para excluir artefatos do Python.
- É recomendado o uso de ambientes virtuais (ex.: `venv` ou `conda`) para isolamento de dependências durante o desenvolvimento.

*Se houver requisitos adicionais específicos do projeto, eles serão declarados imediatamente abaixo desta seção.*

---

## Capítulo IV
### Parte Obrigatória

#### IV.1 Resumo
Você implementará um gerador de labirintos em Python que recebe um arquivo de configuração, gera um labirinto (possivelmente perfeito, com um único caminho entre entrada e saída) e o grava em um arquivo usando uma representação de parede em hexadecimal. Você também fornecerá uma representação visual do labirinto e organizará seu código para que a lógica de geração possa ser reutilizada posteriormente.

#### IV.2 Uso
Seu programa deve ser executado com o seguinte comando:
```bash
python3 a_maze_ing.py config.txt
```
- `a_maze_ing.py` é o arquivo principal do programa. Você deve usar este nome.
- `config.txt` é o único argumento. É um arquivo de texto simples que define as opções de geração do labirinto. Você pode usar um nome de arquivo diferente.

Seu programa deve tratar todos os erros de forma graciosa: configuração inválida, arquivo não encontrado, sintaxe incorreta, parâmetros de labirinto impossíveis, etc. Ele nunca deve travar inesperadamente e deve sempre fornecer uma mensagem de erro clara ao usuário.

#### IV.3 Formato do arquivo de configuração
O arquivo de configuração deve conter um par `CHAVE=VALOR` por linha.
Linhas iniciadas com `#` são comentários e devem ser ignoradas.

As seguintes chaves são **obrigatórias**:

| Chave | Descrição | Exemplo |
|---|---|---|
| `WIDTH` | Largura do labirinto (número de células) | `WIDTH=20` |
| `HEIGHT` | Altura do labirinto | `HEIGHT=15` |
| `ENTRY` | Coordenadas de entrada (x,y) | `ENTRY=0,0` |
| `EXIT` | Coordenadas de saída (x,y) | `EXIT=19,14` |
| `OUTPUT_FILE` | Nome do arquivo de saída | `OUTPUT_FILE=maze.txt` |
| `PERFECT` | O labirinto é perfeito? | `PERFECT=True` |

Você pode adicionar chaves adicionais (ex.: `seed`, `algorithm`, `display_mode`) se achar útil.
Um arquivo de configuração padrão deve estar disponível em seu repositório Git.

#### IV.4 Requisitos do Labirinto
- O labirinto deve ser gerado aleatoriamente, mas a reprodutibilidade via semente (`seed`) é obrigatória.
- Cada célula do labirinto possui entre 0 e 4 paredes, em cada ponto cardinal (Norte, Leste, Sul, Oeste).
- O labirinto deve ser válido, o que significa:
  - Entrada e saída existem e são diferentes, dentro dos limites do labirinto.
  - A estrutura garante conectividade total e nenhuma célula isolada (exceto o padrão "42", veja abaixo).
  - Como a entrada e a saída são células específicas, deve haver paredes nas bordas externas.
  - Seus dados gerados devem ser coerentes: cada célula vizinha deve ter a mesma parede se houver. Ex.: é proibido ter uma célula com parede a leste e a célula vizinha atrás dessa parede sem parede a oeste.
- O labirinto não pode ter grandes áreas abertas. Os corredores não podem ter mais de 2 células de largura. Por exemplo, você pode ter uma área aberta de 2x3 ou 3x2, mas nunca de 3x3.
- Quando representado visualmente, o labirinto deve conter um "42" visível desenhado por várias células totalmente fechadas.
- Se a flag `PERFECT` estiver ativada (`True`), o labirinto deve conter exatamente um caminho entre a entrada e a saída (ou seja, um labirinto perfeito: sem loops).
- Se a flag `PERFECT` não estiver ativada (`False`, o padrão), o labirinto deve ser um tabuleiro diretamente utilizável por um jogo estilo Pac-Man:
  - todo corredor é alcançável (conectividade total), de modo que todo o tabuleiro pode ser preenchido com pastilhas (*pac-gums*) e permanece vencível;
  - os quatro cantos e o centro são corredores abertos (os fantasmas e super-pastilhas ficam nos cantos, o jogador começa no centro);
  - oferece pelo menos duas rotas independentes (loops), para que um jogador perseguido sempre tenha uma alternativa (um labirinto perfeito, ou com apenas uma parede removida, não é aceitável neste modo);
  - becos sem saída devem ser raros (alguns poucos são tolerados); um tabuleiro sem nenhum beco sem saída é o ideal e é recompensado como bônus.

> **Nota:** O padrão "42" pode ser omitido caso o tamanho do labirinto não permita (muito pequeno). Imprima uma mensagem de erro no console nesse caso.

#### IV.5 Formato do Arquivo de Saída
O labirinto deve ser gravado no arquivo de saída usando um dígito hexadecimal por célula, onde cada dígito codifica quais paredes estão fechadas:

| Bit | Direção |
|---|---|
| 0 (LSB) | Norte |
| 1 | Leste |
| 2 | Sul |
| 3 | Oeste |

- Uma parede fechada define o bit como `1`, aberta significa `0`.
  - Exemplo: `3` (binário `0011`) significa paredes abertas ao sul e oeste. Ou `A` (binário `1010`) significa paredes leste e oeste fechadas.
- As células são armazenadas linha por linha, uma linha por linha do arquivo.
- Após uma linha vazia, os 3 elementos seguintes são inseridos no arquivo de saída em 3 linhas:
  - as coordenadas de entrada, as coordenadas de saída e o caminho válido mais curto da entrada até a saída, usando as quatro letras `N`, `E`, `S`, `W`.
- Todas as linhas terminam com `\n`.

Em conjunto com seu arquivo de configuração específico, este arquivo de saída pode ser testado automaticamente por uma *Moulinette*. Um script de análise (`maze_analyzer.py`) também é fornecido com este assunto para verificar a coerência e o modo do labirinto.

---

## Capítulo V
### Representação Visual

Seu programa deve fornecer uma maneira de exibir o labirinto visualmente, usando:
- Renderização ASCII no terminal, ou
- Uma exibição gráfica usando a biblioteca **MiniLibX (MLX)**.

A visualização deve mostrar claramente as paredes, entrada, saída e o caminho da solução.
As interações do usuário devem estar disponíveis enquanto o programa estiver rodando, devendo incluir pelo menos:
- Regenerar um novo labirinto e exibi-lo.
- Mostrar/Ocultar o caminho mais curto válido da entrada à saída.
- Alterar as cores das paredes do labirinto.
- Opcional: definir cores específicas para exibir o padrão "42".

---

## Capítulo VI
### Requisitos de Reutilização de Código

- Você deve implementar a geração do labirinto como uma classe única (ex.: `MazeGenerator`) dentro de um módulo independente que possa ser importado em um projeto futuro.
- Você deve fornecer uma documentação curta descrevendo como:
  - Instanciar e usar seu gerador, com pelo menos um exemplo básico.
  - Passar parâmetros personalizados (tamanho, semente).
  - Acessar a estrutura gerada e pelo menos uma solução.
- Todo este módulo reutilizável (código e documentação) deve estar disponível em um único arquivo adequado para instalação posterior via `pip`.
- Este pacote deve se chamar `mazegen-*` e o arquivo deve estar localizado na raiz do seu repositório Git (extensões `.tar.gz` e `.whl` são permitidas, ex: `mazegen-1.0.0-py3-none-any.whl`).
- Você deve incluir um arquivo `LICENSE.md` na raiz do seu repositório declarando a licença de reutilização.

---

## Capítulo VII
### Requisitos do Readme

Um arquivo `README.md` deve ser fornecido na raiz do seu repositório Git. Deve incluir pelo menos:
- A primeira linha deve estar em itálico e conter: *This project has been created as part of the 42 curriculum by <login1>[, <login2>[, <login3>[...]]]*.
- Uma seção "Description" apresentando claramente o projeto.
- Uma seção "Instructions" contendo informações de compilação, instalação e execução.
- Uma seção "Resources" listando referências e descrevendo como a IA foi utilizada (especificando tarefas e partes do projeto).
- Adições requeridas: estrutura completa do arquivo de configuração, algoritmo de geração escolhido e justificativa, parte reutilizável do código, gerenciamento de equipe (papéis, planejamento, o que funcionou bem, ferramentas utilizadas).

---

## Capítulo VIII
### Bônus

Você pode adicionar vários bônus ao seu projeto, tais como:
- Um labirinto padrão (não perfeito) sem nenhum beco sem saída (*braided*), confirmado pelo script com `--max-dead-ends 0`.
- Suporte a múltiplos algoritmos de geração de labirintos.
- Adicionar animação durante a geração do labirinto.

---

## Capítulo IX
### Submissão e Avaliação por Pares

Submeta sua tarefa em seu repositório Git. Durante a defesa, uma breve modificação no projeto (alteração de comportamento, linhas de código ou nova funcionalidade) poderá ser solicitada para verificar sua compreensão real.
