# Sistema de Triagem - Protocolo de Manchester

Este projeto é uma simulação simplificada de um sistema de triagem de pacientes em um hospital, baseado no Protocolo de Manchester. Ele utiliza uma interface gráfica criada com **Tkinter** para permitir o cadastro de pacientes e uma árvore de decisão lógica para classificá-los por prioridade.

## Visão Geral

O sistema é dividido em dois arquivos principais, separando a lógica de negócios da interface do usuário:

1.  **`logica.py`**: Contém as estruturas de dados (Árvore de Decisão e Fila) e a lógica de classificação.
2.  **`hud_tkinter.py`**: Contém a interface gráfica (GUI) com a qual o usuário interage, construída em Tkinter.

O programa permite que um atendente cadastre um paciente, responda a uma série de perguntas de triagem e, com base nas respostas, o paciente é classificado em uma cor (Vermelho, Laranja, Amarelo, Verde ou Azul) e colocado na fila de espera correspondente. O sistema também permite "chamar" o próximo paciente, respeitando a ordem de prioridade das filas.

-----

## Arquivos do Projeto

### `logica.py` (O "Back-end")

Este arquivo define o "cérebro" da aplicação. Ele não possui interface visual e é responsável apenas pelas regras de negócio e estruturas de dados.

**Componentes Principais:**

  * **`Classe NodoArvore`**: Representa um "nó" na árvore de decisão. Cada nó pode ser uma pergunta (com um caminho `yes` e `no`) ou uma folha (com uma `cor` de classificação final).
  * **`Classe Fila`**: Uma estrutura de dados simples (FIFO - First-In, First-Out) que armazena os pacientes de uma determinada cor. Ela é construída usando `collections.deque` para eficiência.
  * **`função montar_arvore()`**: Esta é a função crucial que constrói e retorna a árvore de decisão simplificada. Ela define a sequência de perguntas:
    1.  Está respirando? (Não -\> **Vermelho**)
    2.  Está consciente? (Não -\> **Laranja**)
    3.  Está com dor intensa? (Sim -\> **Amarelo**)
    4.  A queixa é não urgente? (Sim -\> **Azul** / Não -\> **Verde**)
  * **`função triagem_por_respostas()`**: Uma função auxiliar (não utilizada diretamente pela interface Tkinter) que permitiria a triagem automática se as respostas fossem fornecidas como uma lista.

### `hud_tkinter.py` (A "Interface")

Este é o arquivo principal que deve ser executado. Ele importa a lógica do `logica.py` e a apresenta ao usuário através de uma janela gráfica.

**Componentes Principais:**

  * **`Classe TriagemHUD`**: A classe principal da aplicação que constrói a janela do Tkinter e gerencia todos os elementos visuais (botões, campos de texto, etc.).
  * **`__init__`**:
      * Monta a árvore de decisão chamando `montar_arvore()` de `logica.py`.
      * Cria um dicionário de `Fila`s, uma para cada cor.
      * Desenha os componentes da tela (entrada de nome, botões, painel de status).
  * **`iniciar_triagem()`**:
      * Chamada quando o botão "Cadastrar Paciente" é clicado.
      * Pega o nome do paciente e inicia o processo de perguntas.
  * **`perguntar(nodo)`**:
      * Uma função recursiva inteligente que navega pela árvore de decisão.
      * Usa `messagebox.askyesno()` do Tkinter para fazer cada pergunta ao usuário em um pop-up.
      * Retorna a cor final quando uma folha da árvore é alcançada.
  * **`chamar_paciente()`**:
      * Chamada pelo botão "Chamar Próximo Paciente".
      * Verifica as filas na ordem de prioridade (Vermelho primeiro, Azul por último).
      * Remove (desenfileira) o primeiro paciente da fila de maior prioridade e exibe um pop-up informando quem está sendo chamado.
  * **`mostrar_status()` e `atualizar_periodicamente()`**:
      * Funções responsáveis por atualizar o painel "Status das Filas".
      * `mostrar_status` exibe quantos pacientes estão em cada fila, usando cores para fácil visualização.
      * `atualizar_periodicamente` usa `master.after()` para recarregar o status a cada 5 segundos, mantendo a tela atualizada automaticamente.

-----

## Como Funciona (Fluxo de Uso)

1.  Execute o arquivo `hud_tkinter.py`.
2.  Digite o nome do paciente no campo "Nome do Paciente".
3.  Clique em "Cadastrar Paciente".
4.  Uma série de pop-ups com perguntas "Sim/Não" aparecerá. Responda a cada uma.
5.  Ao final, um pop-up informará a classificação do paciente (ex: "Paciente foi classificado como Amarelo").
6.  O painel "Status das Filas" será atualizado, mostrando o paciente na fila correta.
7.  Para atender, clique em "Chamar Próximo Paciente". O sistema chamará o paciente da fila de maior prioridade disponível.

## Como Executar

1.  Certifique-se de que você tem o Python 3 instalado.
2.  Coloque os arquivos `hud_tkinter.py` e `logica.py` no mesmo diretório.
3.  Abra um terminal ou prompt de comando, navegue até esse diretório e execute: