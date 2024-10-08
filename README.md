﻿
# Projeto de Biblioteca

Este projeto é uma aplicação de terminal para gerenciar uma biblioteca, permitindo a criação de contas de autores e leitores, adição de livros, empréstimos e devoluções.

## Tecnologias Utilizadas
- **Python:** Linguagem de programação principal.
- **Peewee:** ORM utilizado para interagir com o banco de dados SQLite.
- **SQLite:** Banco de dados utilizado para armazenar as informações.
- **dotenv:** Biblioteca para carregar variáveis de ambiente a partir de um arquivo `.env`.
- **bcrypt:** Biblioteca para hashing de senhas.
- **requests:** Biblioteca para fazer requisições HTTP.

## Estrutura do Projeto

- `main.py`: Contém a lógica principal da aplicação, incluindo criação de usuários, login, adição de livros, visualização de livros e empréstimos.
- `models.py`: Define os modelos de dados usando o Peewee ORM e configura o banco de dados SQLite.
- `api_validator.py`: Contém funções para validação de CPF usando uma API externa.

## Pré-requisitos

- Python 3.x
- Bibliotecas: `peewee`, `bcrypt`, `requests`, `python-dotenv`

## Instalação

1. Clone o repositório:

   ```bash
   git clone https://github.com/seu-usuario/projeto-biblioteca.git
   cd projeto-biblioteca
   ```
2. Crie um ambiente virtual e ative-o:

   ```bash
   python -m venv venv
   source venv/bin/activate  # No Windows use `venv\Scripts\activate`
   ```
3. Instale as dependências:

   ```bash
   pip install -r requirements.txt
   ```
4. Crie um arquivo `.env` na raiz do projeto e adicione as seguintes variáveis:

   ```env
   DB_NAME=seu_banco_de_dados.db
   API_KEY=sua_chave_api
   ```

## Uso

1. **Criação do Banco de Dados**: Execute o `models.py` para criar o banco de dados e as tabelas necessárias:

   ```bash
   python models.py
   ```
2. **Execução da Aplicação**: Execute o `main.py` para iniciar a aplicação:

   ```bash
   python main.py
   ```

## Funcionalidades

- **Criação de Conta**: Permite criar contas de autores e leitores.
- **Login**: Autenticação de usuários (autores, leitores e administradores).
- **Adicionar Livro**: Autores podem adicionar livros à biblioteca.
- **Visualizar Livros**: Autores podem ver seus livros adicionados; leitores podem ver todos os livros disponíveis.
- **Empréstimo de Livro**: Leitores podem pegar livros emprestados.
- **Devolução Automática**: Administradores podem devolver livros automaticamente quando a data de devolução é atingida.

## Observações

- Esta aplicação é executada no terminal e não possui interface web.
- Certifique-se de executar o `models.py` antes de iniciar a aplicação para garantir que o banco de dados e as tabelas sejam criados corretamente.

## Contribuição

Contribuições são bem-vindas! Sinta-se à vontade para abrir issues e pull requests.

## Licença

Este projeto está licenciado sob a MIT License.
