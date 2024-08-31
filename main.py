from models import *
from bcrypt import checkpw, hashpw, gensalt
from api_validator import validator_cpf, format_result
from datetime import date, timedelta

def create_user(name, cpf, password, user_type):
    try:
        with db.atomic():
            salt = gensalt()
            hashed_password = hashpw(password.encode('utf-8'), salt)

            if user_type == 'author':
                Author.create(name=name, cpf=cpf, password=hashed_password)
            elif user_type == 'reader':
                Reader.create(name=name, cpf=cpf, password=hashed_password)

            print('Conta criada com sucesso!')
    except Exception as e:
        print(f'Erro ao criar o usuário: {e}')

def register_user(user_type):
    name = input('Digite seu nome: ')
    cpf = input('Digite seu CPF: ')
    password = input('Digite sua senha: ')

    if cpf:
        result = validator_cpf(cpf)
        if "error" in result:
            print(f"Erro na validação do CPF: {result['error']}")
        elif format_result(result):
            create_user(name, cpf, password, user_type)
        else:
            print('Não foi possível criar a conta. CPF inválido.')
    else:
        print('CPF não informado. Conta não pode ser criada.')

def login_user(user_type):
    cpf = input('Digite seu CPF: ')
    password_attempts = 0

    while password_attempts < 3:
        password = input('Digite sua senha: ')

        try:
            if user_type == 'author':
                user = Author.get(Author.cpf == cpf)
            elif user_type == 'reader':
                user = Reader.get(Reader.cpf == cpf)
            else:
                print('Tipo de usuário inválido.')
                return

            if checkpw(password.encode('utf-8'), user.password.encode('utf-8')):
                print('Login bem-sucedido!')
                home(user_type, cpf)
                return
            else:
                print('Senha incorreta.')
                password_attempts += 1

        except Author.DoesNotExist:
            print('Autor não encontrado.')
            return
        except Reader.DoesNotExist:
            print('Leitor não encontrado.')
            return
        except Exception as e:
            print(f'Erro ao fazer login: {e}')
            return

    print('Número de tentativas excedido. Retornando ao menu.')
    menu()

def add_book(name_book, category_book, descr_book, cpf):
    try:
        with db.atomic():
            Book.create(
                name_book=name_book,
                category_book=category_book,
                descr_book=descr_book,
                author=Author.get(Author.cpf == cpf)
            )
        print(f'Livro {name_book} criado com sucesso!\n')
    except AttributeError as e:
        print(f'Erro ao adicionar o livro: {e}')
    finally:
        home('author', cpf)

def register_book(cpf):
    name_book = input('Digite o nome do livro: ')
    category_book = input('Digite a categoria do livro: ')
    descr_book = input('Digite a descrição do livro: ')
    add_book(name_book, category_book, descr_book, cpf)

def view_books(cpf, user_type):
    try:
        if user_type == 'author':
            author = Author.get(Author.cpf == cpf)
            books = Book.select().where(Book.author == author)
            if books:
                print(f'Livros do Autor: {author.name}\n')
                for book in books:
                    status = "Livro Emprestado" if Loan.select().where(Loan.book == book, Loan.status == 'emprestado').exists() else "Livro Disponível"
                    print(f"ID: {book.id}\nNome: {book.name_book}\nCategoria: {book.category_book}\nStatus: {status}\n")
            else:
                print('\nNenhum livro foi cadastrado...\n')

        elif user_type == 'reader':
            books = Book.select().join(Loan, JOIN.LEFT_OUTER).where((Loan.status.is_null(True)) | (Loan.status == 'disponível'))
            for book in books:
                print(f"ID: {book.id}\nNome: {book.name_book}\nCategoria: {book.category_book}\nStatus: Disponível\n")
    except Author.DoesNotExist:
        print("\nCliente não encontrado...\n")
    except AttributeError as e:
        print(f'Erro: {e}')
    finally:
        home(user_type, cpf)

def view_borrowed_books(cpf):
    try:
        reader = Reader.get(Reader.cpf == cpf)
        loans = Loan.select().where(Loan.reader == reader, Loan.status == 'emprestado')
        if loans:
            print(f'Livros emprestados por {reader.name}:\n')
            for loan in loans:
                book = loan.book
                print(f"ID: {book.id}\nNome: {book.name_book}\nCategoria: {book.category_book}\nData de Empréstimo: {loan.loan_date}\nData de Devolução: {loan.return_date}\n")
        else:
            print('Nenhum livro emprestado.')
    except Reader.DoesNotExist:
        print('Leitor não encontrado.')
    finally:
        home('reader', cpf)

def borrow_book(cpf):
    book_id = input('Digite o ID do livro que deseja pegar emprestado: ')
    try:
        book = Book.get(Book.id == book_id)
        reader = Reader.get(Reader.cpf == cpf)
        if Loan.select().where(Loan.book == book, Loan.status == 'emprestado').exists():
            print('Livro já está emprestado.')
        else:
            Loan.create(
                book=book,
                reader=reader,
                loan_date=date.today(),
                return_date=date.today() + timedelta(days=30),
                status='emprestado'
            )
            print(f'Livro {book.name_book} emprestado com sucesso!')
    except Book.DoesNotExist:
        print('Livro não encontrado.')
    except Reader.DoesNotExist:
        print('Leitor não encontrado.')
    finally:
        home('reader', cpf)

def admin_return_books():
    try:
        overdue_loans = Loan.select().where(Loan.return_date <= date.today(), Loan.status == 'emprestado')
        for loan in overdue_loans:
            loan.status = 'disponível'
            loan.save()
            print(f'Livro {loan.book.name_book} devolvido automaticamente.')
    except Exception as e:
        print(f'Erro ao devolver livros automaticamente: {e}')

def home(user_type, cpf):
    while True:
        if user_type == 'author':
            print('\n1 - Adicionar livro\n2 - Ver livros adicionados\n3 - Sair\n')
            user = input(': ')
            if user == '1':
                register_book(cpf)
            elif user == '2':
                view_books(cpf, user_type)
            elif user == '3':
                exit()
        elif user_type == 'reader':
            print('\n1 - Ver livros\n2 - Seus livros\n3 - Pegar livro emprestado\n4 - Sair\n')
            user = input(': ')
            if user == '1':
                view_books(cpf, user_type)
            elif user == '2':
                view_borrowed_books(cpf)
            elif user == '3':
                borrow_book(cpf)
            elif user == '4':
                exit()
        elif user_type == 'admin':
            print('\n1 - Devolver livros automaticamente\n2 - Sair\n')
            user = input(': ')
            if user == '1':
                admin_return_books()
            elif user == '2':
                exit()

def menu():
    print('\nBem vindo...\n1 - Criar conta\n2 - Fazer login\n3 - Sair\n')
    user = input(': ')

    if user == '1':
        print('\n1 - Escritor\n2 - Leitor\n3 - Voltar\n')
        user_type = input(': ')
        if user_type == '1':
            register_user(user_type='author')
            return menu()
        elif user_type == '2':
            register_user(user_type='reader')
            return menu()
    elif user == '2':
        print('\n1 - Escritor\n2 - Leitor\n3 - Administrador\n4 - Voltar\n')
        user_type = input(': ')
        if user_type == '1':
            login_user(user_type='author')
        elif user_type == '2':
            login_user(user_type='reader')
        elif user_type == '3':
            login_user(user_type='admin')
    else:
        return menu()

if __name__ == "__main__":
    menu()
