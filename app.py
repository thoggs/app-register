import json
import os
from tabulate import tabulate
from termcolor import colored


# DESCOMENTAR caso esteja utilizando PyCharm
# def displayclear():
#     print('\n' * 100)


def displayclear():
    """
    MANTER DESCOMENTADO caso esteja executando no VScode, terminal Linux/macOS
    e Windows (cmd)
    COMENTAR caso esteja executando no PyCharm

    :return: not return
    """
    os.system('cls' if os.name == 'nt' else 'clear')


class Optionsjson:
    """
    classe para opções no arquivo JSON
    """
    def __init__(self, file_data):
        try:
            os.makedirs('./jsonCache')
        except FileExistsError:
            pass
        for item in file_data:
            self.data = {}
            try:
                with open(f'jsonCache/{item}' + '.json', 'r') as f:
                    self.data = json.load(f)
            except FileNotFoundError:
                with open(f'jsonCache/{item}' + '.json', 'w') as f:
                    json.dump(self.data, f, indent=4)

    @staticmethod
    def setdata(file_data):
        data = {}
        try:
            with open(f'jsonCache/{file_data}' + '.json', 'r') as f:
                data = json.load(f)
        except FileNotFoundError:
            with open(f'jsonCache/{file_data}' + '.json', 'w') as f:
                json.dump(data, f, indent=4)
        return data

    @staticmethod
    def writejason(data, file_data):
        with open(f'jsonCache/{file_data}' + '.json', 'w') as f:
            json.dump(data, f, indent=4)

    @staticmethod
    def valid_reg(file_data, column, value):
        data = op.setdata(file_data)
        for x, y in data.items():
            for item in y:
                if item == column.upper():
                    try:
                        numint = int(y[item])
                        numval = int(value)
                        if numval == numint:
                            return True
                        else:
                            continue
                    except ValueError:
                        if file_data == 'turma':
                            if y[item] == value:
                                return True
                            else:
                                continue
        return None

    @staticmethod
    def create_new_register(file_data):
        topbar(None, file_data, 'criar novo registro')
        data = op.setdata(file_data)
        print(tabulate(data.values(), headers='keys', tablefmt='psql'))
        new = dict()
        idem = '1'
        ids = [int(k) for k in data.keys()]
        if len(ids) != 0:
            idem = str(max(ids) + 1)
        columns = eval(file_data)
        for column in columns:
            while True:
                value = input(f'Informe, {column.capitalize()}: ').title()
                if op.valid_reg(file_data, column, value) is True:
                    print(f'{column.upper()}: {value}, já foi cadastrado!')
                    continue
                else:
                    new[column.upper()] = value
                    break
        data[idem] = new
        op.writejason(data, file_data)
        topbar(None, file_data, 'criar novo registro')
        print(tabulate(data.values(), headers='keys', tablefmt='psql'),
              colored('\n\tCADASTRO REALIZADO COM SUCESSO!\n',
                      'green', attrs=['bold']))
        while input('Deseja continuar cadastrando (S/N): ').lower() == 's':
            op.create_new_register(file_data)
            break

    @staticmethod
    def read_register(file_data):
        data = op.setdata(file_data)
        record = None
        identifier = None
        yes = True
        reg_user = list()
        while yes:
            identifier = input('Entre com o ID: ')
            displayclear()
            if identifier in data.keys():
                record = data[identifier]
                print('\n')
                reg_user.append(data.get(identifier))
                print(f'ID:', colored(identifier, 'red', attrs=['bold']))
                if len(reg_user) is 1:
                    print(tabulate(reg_user, headers='keys', tablefmt='psql'))
                    break
                else:
                    print(tabulate(reg_user, headers='keys', tablefmt='psql'))
                    break
            else:
                reg_user.clear()
                print('ID sem registro!')
                answer = input('Deseja buscar outro ID? (S/N): ').lower()
                if 'n' in answer:
                    yes = False
        return record, identifier

    @staticmethod
    def compare_term(file_data, term, param):
        data = op.setdata(file_data)
        resultlist = list()
        for identf, item in data.items():
            if item.get(param.upper()) == term:
                resultlist.append(item)
        return resultlist

    @staticmethod
    def update_register(file_data):
        topbar(None, file_data, 'atualizar registro')
        data = op.setdata(file_data)
        registerlist = list()
        print('-' * 30)
        for x, y in data.items():
            print('ID:', colored(x, 'red', attrs=['bold']))
            registerlist.append(y)
            print(tabulate(registerlist, headers='keys', tablefmt='psql'))
            registerlist.pop(0)
        record, identifier = op.read_register(file_data)
        if record is None or identifier is None:
            print('O ID do registro não pode ser nulo!')
            finalize_program()
        columns = eval(file_data)
        for column in columns:
            flag = True
            while flag:
                value = input(f'Atualizar {column.upper()}: ').title()
                if op.valid_reg(file_data, column, value) is True:
                    print(f'{column.upper()}: {value}, já foi cadastrado!')
                    continue
                else:
                    record[column.upper()] = value
                    data[identifier] = record
                    op.writejason(data, file_data)
                    flag = False
        displayclear()
        print(f'\nRegistro ID: {identifier}, alterado com sucesso!')
        input('\nPressione Enter para continuar...')

    @staticmethod
    def remove_register(file_data):
        data = op.setdata(file_data)
        while True:
            results = dict()
            topbar(None, file_data, 'Excluir registro')
            if len(data) is 0:
                input(
                    f'{colored("BASE VAZIA!", "red", attrs=["bold"])}{ln * 2}'
                    f'Pressione ENTER para continuar...')
                return None
            print(tabulate(data.values(), headers='keys', tablefmt='psql'))
            term = input(f'Entre como termo: ')
            for identifier, record in data.items():
                for column, value in record.items():
                    if term in value.lower():
                        results[identifier] = record
                        continue
            topbar(None, file_data, 'Excluir registro')
            if len(results) is 0:
                print(colored('\nSEM REGISTROS PARA O TERMO INFORMADO!',
                              'red', attrs=['bold']))
                input(f'{ln}'
                      f'Pressione ENTER para continuar...')
                continue
            else:
                print(f'Resultado para:', colored(term, 'yellow'))
                print(tabulate(results.values(),
                               headers='keys', tablefmt='psql'))
            choice = input(f'{tb}'
                           f'{colored("ATENÇÃO!", "red", attrs=["bold"])}'
                           f'\nEssa operação apagará '
                           f'todos os registros encontrados!{ln}'
                           f'Deseja continuar (S/N): ').lower()
            if choice == 's':
                for identifier in results:
                    data.pop(identifier)
                op.writejason(data, file_data)
            if choice == 'n':
                break
        return None

    @staticmethod
    def fetch_by_column(file_data):
        """
        Função para buscar registros em um arquivo json  a partir de um texto.

        :param file_data: valor de file_data
        :return: False if the column is 0, or return None
        """
        data = op.setdata(file_data)
        while True:
            topbar(None, file_data, 'Pesquisar registro')
            results = dict()
            if len(data) == 0:
                print(colored(f'\n\tBASE VAZIA!', 'red', attrs=['bold']))
                input(f'{ln}Pressione ENTER para continuar...')
                return None
            text = input('\nEntre com o termo que deseja buscar: ').lower()
            for identifier, record in data.items():
                for coluna, valor in record.items():
                    if coluna == '0':
                        return False
                    if text in valor.lower():
                        results[identifier] = record
                        continue
            topbar(None, file_data, 'Pesquisar registro')
            if len(results) is 0:
                print(colored('SEM REGISTROS PARA O TERMO INFORMADO!',
                              'red', attrs=['bold']))
            else:
                print(f'Resultado para:', colored(text, 'yellow'))
                print(tabulate(results.values(),
                               headers='keys', tablefmt='psql'))
            remake = input(
                f'Desenja continuar pesquisando (S/N): ').lower()
            if 'n' in remake:
                break
            else:
                continue
        return results

    @staticmethod
    def record_list(file_data):
        """
        Função para listar itens.

        :param file_data: valor de file_data
        :return: not return
        """
        topbar(None, file_data, 'Listar Registros')
        data = op.setdata(file_data)
        if len(data) == 0:
            topbar(None, file_data, 'Listar Registros')
            print(f'{tb}{colored("BASE VAZIA!", "red", attrs=["bold"])}')
        print(tabulate(data.values(), headers='keys', tablefmt='psql'))
        input(f'Pressione ENTER para continuar...')


def list_by_registration(classes, students, discipline):
    displayclear()
    dataclasses = op.setdata(classes)
    datadiscipline = op.setdata(discipline)
    turmlist = list()
    disciplist = list()
    print('Escolha a opção de listagem:\n')
    print('(1) Todas as Matriculas\n'
          '(2) Matriculas por Estudantes\n'
          '(9) Voltar ao Menu\n')
    option = input('Faça sua escolha: ')
    for x, y in dataclasses.items():
        turmlist.append(y.get('cod. turma'.upper()))
    for x, y in datadiscipline.items():
        disciplist.append(y.get('turma'.upper()))
    if option == '1':
        displayclear()
        for cod in turmlist:
            print(tabulate(op.compare_term(classes, cod, 'cod. turma'),
                           headers='keys', tablefmt='plain'))
            print(tabulate(op.compare_term(students, cod, 'turma'),
                           headers='keys', tablefmt='psql'))
            print('')
        input('\nPressione ENTER para continar...')
    if option == '2':
        for cod in turmlist:
            print(tabulate(op.compare_term(discipline, cod, 'turma')))
        input('Pressione ENTER para continuar...')


def advancedopt(file_data):
    """
    Função para excluir todos os registros.

    :param file_data: valor de file_data
    :return: not return
    """
    data = op.setdata(file_data)
    checkdata = data.items()
    while True:
        topbar(None, file_data, 'Opções Avançadas')
        choice = input(
            f'(0) {colored("Excluir tudo em: ", "red", attrs=["bold"])}'
            f'{colored(file_data.title(), "cyan")}\n'
            f'(9) <=| Voltar ao menu de operações\n\n'
            f'Selecione uma opção: ')
        if choice == '0':
            topbar(None, file_data, 'Opções Avançadas')
            if len(checkdata) == 0:
                print(f'Não há nada para apagar na lista: '
                      f'{colored(file_data.capitalize(), "cyan")}...')
                input('\nPressione ENTER para continuar... ')
                break
            print(tabulate(data.values(), headers='keys', tablefmt='psql'))
            opt = input(f'{tb}{colored("ATENÇÃO!", "red", attrs=["bold"])}\n'
                        f'Essa operação apagará TUDO em: '
                        f'{colored(file_data.capitalize(), "cyan")}{ln}'
                        f'Tem certeza que deseja continuar (S/N): ').lower()
            if opt == 's':
                data.clear()
                op.writejason(data, file_data)
                topbar(None, file_data, 'Opções Avançadas')
                print(colored('\tOPERAÇÃO REALIZADA COM SUCESSO!\n',
                              'green', attrs=['bold']))
                input('Pressione ENTER para continuar...')
                continue
            if opt == 'n':
                continue
            else:
                input(f'{colored("Valor inválido", "red", attrs=["bold"])}\n'
                      f'Pressione ENTER para Continuar...')
                continue
        if choice == '9':
            return None
        break


def finalize_program():
    """
    Função para finalizar o programa.

    :return: not return
    """
    print('Finalizando o programa...')
    exit(0)


def topbar(bool_or_None, file_data, option):
    displayclear()
    starttext = f'{tb}GERENCIADOR DE REGISTROS v1.1{tb * 2}'
    file_data_cyan = colored(file_data.upper(), 'blue', attrs=['bold'])
    file_data_grey = file_data.upper()
    optioncontext = colored(option.upper(), 'blue', attrs=['bold'])
    menutext = colored('MENU', 'blue', attrs=['bold'])
    menutext_grey = 'MENU'

    print(colored(starttext,
                  'yellow', attrs=['reverse', 'blink', 'bold']), f'\n')
    if bool_or_None:
        print(colored(
            f'[ {menutext_grey} ]-'
            f'[ {file_data_cyan} ]'))
    if bool_or_None is None:
        print(colored(
            f'[ {menutext_grey} ]-'
            f'[ {file_data_grey} ]-'
            f'[ {optioncontext} ]\n'))
    if bool_or_None is False:
        print(colored(f'[ {menutext} ]'))


def operacao(tabela):
    opcoes = ['1', '2', '3', '4', '5', '9', '0']
    active = True
    while active:
        displayclear()
        topbar(True, tabela, '')
        option = input(f'\n(1) Criar novo registro\n'
                       f'(2) Excluir registro\n'
                       f'(3) Atualizar Registro\n'
                       f'(4) Listar Registros\n'
                       f'(5) Pesquisar registro\n'
                       f'(9) Voltar menu\n'
                       f'(0) Opções Avançadas |=>{ln}'
                       f'Selecione uma das opções: ')
        if option not in opcoes:
            input('Opção Invalida! Tente novamente...').lower()
        else:
            displayclear()
            if option == '1':
                op.create_new_register(tabela)
            if option == '2':
                op.remove_register(tabela)
            if option == '3':
                op.update_register(tabela)
            if option == '4':
                op.record_list(tabela)
            if option == '5':
                op.fetch_by_column(tabela)
            if option == '0':
                advancedopt(tabela)
            elif option == '9':
                active = False


def menu():
    """
    Função main, a qual faz a chamada para a função operacoes().

    :return: not return
    """
    opcoes = ['1', '2', '3', '4', '5', '6', '9']
    active = True
    while active:
        displayclear()
        topbar(False, '', '')
        option = input(f'\n(1) Gerenciar Estudantes\n'
                       f'(2) Gerenciar Professores\n'
                       f'(3) Gerenciar Diciplina\n'
                       f'(4) Gerenciar Turma\n'
                       f'(5) Gerenciar Matricula\n'
                       f'(6) Listagem de Matriculas\n'
                       f'(9) Sair{ln}'
                       f'Faça sua escolha: ').lower()
        if option in opcoes:
            if option == '1':
                operacao('estudantes')
            if option == '2':
                operacao('professores')
            if option == '3':
                operacao('disciplina')
            if option == '4':
                operacao('turma')
            if option == '5':
                operacao('matricula')
            if option == '6':
                list_by_registration('turma', 'estudantes', 'disciplina')
            elif option == '9':
                active = False
            else:
                print('Opção invalida! Tente novamente.')
    finalize_program()


if __name__ == '__main__':
    tb = '\t' * 2
    ln = '\n' * 2
    # definindo as tabelas
    tabelas = list(['estudantes', 'professores', 'disciplina', 'turma',
                    'matricula'])
    # passando as tabelas para a classe
    op = Optionsjson(tabelas)
    # definindo os nomes das colunas para as tabelas
    estudantes = ['matricula', 'nome/sobrenome', 'turma']
    professores = ['matricula', 'nome/sobrenome', 'docência']
    disciplina = ['cod. geral', 'nome', 'turma', 'professor']
    turma = ['cod. turma', 'disciplina', 'professor']
    matricula = ['cod. geral', 'nome']
    # chamada principal do programa
    menu()
 
