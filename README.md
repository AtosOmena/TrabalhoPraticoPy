# 🎮 Jogo da Forca - Python

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/)
[![Tkinter](https://img.shields.io/badge/GUI-Tkinter-green.svg)](https://docs.python.org/3/library/tkinter.html)

Implementação completa do clássico Jogo da Forca em Python com interface gráfica (Tkinter), seguindo princípios de **Clean Architecture** e boas práticas de desenvolvimento.

---

## 📋 Índice

- [Sobre o Projeto](#-sobre-o-projeto)
- [Funcionalidades](#-funcionalidades)
- [Arquitetura](#-arquitetura)
- [Instalação](#-instalação)
- [Como Usar](#-como-usar)
- [Estrutura do Projeto](#-estrutura-do-projeto)
- [Tecnologias](#-tecnologias)

---

## 🎯 Sobre o Projeto

Este projeto foi desenvolvido como trabalho prático da disciplina de **Nivelamento em Python**, demonstrando domínio dos conceitos fundamentais da linguagem através de uma aplicação completa e funcional.

O jogo oferece duas modalidades:
- **Single Player**: Jogue contra o computador com palavras aleatórias
- **Multiplayer (1v1)**: Um jogador escolhe a palavra, o outro adivinha

Além do jogo em si, o sistema mantém:
- 🏆 **Placar** com ranking de jogadores
- 📜 **Histórico** completo de partidas
- 📊 **Estatísticas** detalhadas de desempenho

---

## ✨ Funcionalidades

### 🎮 Modos de Jogo
- **Single Player**: Palavras aleatórias do dicionário
- **Multiplayer**: Palavra customizada entre dois jogadores

### 📊 Sistema de Pontuação
- Ranking de jogadores por vitórias
- Taxa de vitória (Win Rate)
- Persistência de dados em arquivos

### 📜 Histórico de Partidas
- Registro completo de todas as partidas
- Data, hora e duração de cada jogo
- Estatísticas agregadas (total de jogos, vitórias, derrotas)

### 🎨 Interface Gráfica
- Interface moderna e intuitiva com Tkinter
- Animação visual da forca
- Feedback visual de tentativas e erros
- Navegação fluida entre telas

---

## 🏛️ Arquitetura

O projeto segue os princípios de **Clean Architecture**, garantindo:
- ✅ Desacoplamento entre camadas
- ✅ Testabilidade
- ✅ Manutenibilidade
- ✅ Escalabilidade

```
┌─────────────────────────────────────────┐
│         Presentation Layer              │
│  (Views, Controllers - Tkinter UI)      │
└──────────────┬──────────────────────────┘
               │
┌──────────────▼──────────────────────────┐
│          Domain Layer                   │
│  (Use Cases, Entities - Business Logic) │
└──────────────┬──────────────────────────┘
               │
┌──────────────▼──────────────────────────┐
│           Data Layer                    │
│  (Repositories, Storage - File I/O)     │
└─────────────────────────────────────────┘
```

### Princípios Aplicados
- **Single Responsibility**: Cada classe tem uma única responsabilidade
- **Dependency Inversion**: Dependências apontam para abstrações
- **Open/Closed**: Extensível sem modificar código existente
- **Interface Segregation**: Interfaces específicas e coesas

---

## 🚀 Instalação

### Pré-requisitos
- Python 3.8 ou superior
- Tkinter (geralmente incluído no Python)

### Verificar Tkinter
```bash
python -m tkinter
```
Se uma janela aparecer, o Tkinter está instalado corretamente.

### Clonar o Repositório
```bash
git clone https://github.com/AtosOmena/TrabalhoPraticoPy
cd TrabalhoPraticoPy
```

### Executar o Jogo
```bash
python main.py
```

---

## 🎮 Como Usar

### 1️⃣ Menu Principal
Ao iniciar o jogo, você verá 4 opções:
- **🎯 Single Player**: Jogar sozinho contra o computador
- **👥 Multiplayer (1v1)**: Jogar com outra pessoa
- **🏆 Placar**: Ver ranking de jogadores
- **📜 Histórico**: Ver partidas anteriores

### 2️⃣ Single Player
1. Digite seu nome
2. Clique em "Iniciar Jogo"
3. Tente adivinhar a palavra letra por letra
4. Você tem 6 tentativas erradas

### 3️⃣ Multiplayer
1. Jogador 1 digita seu nome e escolhe a palavra secreta
2. Jogador 2 digita seu nome
3. Jogador 2 tenta adivinhar a palavra
4. A palavra fica oculta durante a digitação

### 4️⃣ Placar
- Visualize o ranking dos melhores jogadores
- Ordenado por número de vitórias
- Mostra taxa de vitória (Win Rate)

### 5️⃣ Histórico
- Veja todas as partidas jogadas
- Informações: data, jogador, palavra, resultado, duração
- Estatísticas gerais do jogo

---

## 📂 Estrutura do Projeto

```
jogo-da-forca/
│
├── main.py                          # Ponto de entrada da aplicação
│
├── domain/                          # Camada de Domínio (Lógica de Negócio)
│   ├── __init__.py
│   ├── entities/                    # Entidades do domínio
│   │   ├── __init__.py
│   │   ├── player.py               # Classe Player (com métodos mágicos)
│   │   ├── game_state.py           # Estado do jogo
│   │   ├── game_history.py         # Histórico de partidas
│   │   └── game_mode.py            # Enum de modos de jogo
│   │
│   └── use_cases/                   # Casos de uso (regras de negócio)
│       ├── __init__.py
│       ├── hangman_game_use_case.py
│       ├── scoreboard_use_case.py
│       └── history_use_case.py
│
├── data/                            # Camada de Dados (Persistência)
│   ├── __init__.py
│   ├── repositories/                # Interfaces (contratos)
│   │   ├── __init__.py
│   │   ├── player_repository.py
│   │   ├── word_repository.py
│   │   └── history_repository.py
│   │
│   └── storage/                     # Implementações (arquivos)
│       ├── __init__.py
│       ├── file_player_repository.py
│       ├── file_word_repository.py
│       └── file_history_repository.py
│
├── presentation/                    # Camada de Apresentação (UI)
│   ├── __init__.py
│   ├── controllers/                 # Controladores
│   │   ├── __init__.py
│   │   └── game_controller.py
│   │
│   └── views/                       # Views (Tkinter)
│       ├── __init__.py
│       ├── base_view.py            # Classe base para views
│       ├── main_menu_view.py
│       ├── player_setup_view.py
│       ├── game_view.py
│       ├── game_over_view.py
│       ├── scoreboard_view.py
│       └── history_view.py
│
└── assets/                          # Arquivos de dados
    ├── words.txt                    # Dicionário de palavras
    ├── scoreboard.txt               # Placar de jogadores
    └── history.txt                  # Histórico de partidas
```

---

## 🛠️ Tecnologias

- **Python 3.8+**: Linguagem principal
- **Tkinter**: Interface gráfica
- **Threading**: Operações assíncronas (evita travamento da UI)
- **ABC (Abstract Base Classes)**: Interfaces e contratos
- **Type Hints**: Tipagem estática para melhor manutenibilidade
- **Dataclasses**: Estruturas de dados imutáveis

---

## 📚 Conceitos Demonstrados

### Programação Orientada a Objetos
- ✅ Encapsulamento
- ✅ Herança (BaseView)
- ✅ Polimorfismo (Interfaces)
- ✅ Abstração (ABC)

### Padrões de Projeto
- ✅ Repository Pattern
- ✅ Dependency Injection
- ✅ MVC (Model-View-Controller)

### Boas Práticas
- ✅ Clean Code
- ✅ SOLID Principles
- ✅ Type Hints
- ✅ Docstrings
- ✅ Separation of Concerns

### Python Avançado
- ✅ List Comprehensions
- ✅ Métodos Mágicos (Dunder Methods)
- ✅ Properties (@property)
- ✅ Context Managers (with)
- ✅ Threading
- ✅ Enums
