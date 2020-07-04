#####
# Author: Maiky Nata
# Version: 1.0
#####

import psycopg2
import PySimpleGUI as sg
import datetime

print = sg.Print
newlist = []

def select_prod(prod_codigo):
    try:

        conn_string = "host='127.0.0.1' dbname='erp_teste' user='postgres' password='teste123'"
        connection = psycopg2.connect(conn_string)
        cursor = connection.cursor()

        sql_prod_cod_query = """select prod_descricao, prod_complemento, prod_marca, prun_prvenda, prun_estoque1, 
                                prun_estmin  from produtos, produn
                                where prod_codigo=prun_prod_codigo and prun_unid_codigo='001' 
                                and prod_codbarras=%s"""
        #CAST(prod_codigo=%s as numeric)
        cursor.execute(sql_prod_cod_query, [prod_codigo])
        rows = cursor.fetchall()

        if len(rows) == 0:
            sql_prod_cbalt_query = """select prod_descricao, prod_complemento, prod_marca, prun_prvenda, prun_estoque1, 
                                            prun_estmin  from produtos, produn
                                            where prod_codigo=prun_prod_codigo and prun_unid_codigo='001' 
                                            and prod_codigo in (select cbal_prod_codigo from cbalt where cbal_prod_codbarras=%s)"""
            # CAST(prod_codigo=%s as numeric)
            cursor.execute(sql_prod_cbalt_query, [prod_codigo])
            rows = cursor.fetchall()

        return rows
        connection.commit()
        count = cursor.rowcount
        sg.popup_ok(count, 'Produtos selecionados!')


    except(Exception, psycopg2.Error) as error:
        sg.popup_ok("Error while connecting to PostgreSQL", error)

    finally:
        # Closing database connection.
        if (connection):
            cursor.close()
            connection.close()


def insert_pendest():
    try:

        conn_string = "host='127.0.0.1' dbname='erp_teste' user='postgres' password='teste123'"
        connection = psycopg2.connect(conn_string)
        cursor = connection.cursor()

        sql_update_query = """update produn
                              set prun_estmin=2
                              where prun_unid_codigo='001' and prun_prod_codigo=101567"""
        cursor.execute(sql_update_query)
        connection.commit()
        count = cursor.rowcount
        sg.popup_ok(count, 'Produtos alterados!')


    except(Exception, psycopg2.Error) as error:
        sg.popup_ok("Error while connecting to PostgreSQL", error)

    finally:
        # Closing database connection.
        if (connection):
            cursor.close()
            connection.close()

# Layout the design of the GUI
QT_ENTER_KEY1 = 'special 16777220'
QT_ENTER_KEY2 = 'special 16777221'
#enter_buttons = [chr(13), "Return:13"]

sg.SetOptions(element_padding=(4, 0))

layout = [[sg.Text("Descrição do Produto", auto_size_text=True)],
          [sg.Input( readonly=True, key='nome_prod')],
          [sg.Text("Pr. Venda"), sg.Text("   Estoque"), sg.Text("  Est. Min", justification='right')],
          [sg.Input(size=(9,1), readonly=True, key='preco_prod'),
           sg.Input(size=(9,1), readonly=True, key='estoque_prod'), sg.Input(size=(9,1),readonly=True, key='estmin_prod')],
          [sg.Text("V.M.3"), sg.Text("       V.M.12"), sg.Text("     Venda Mês"), ],
          [sg.Input(size=(9,1), readonly=True), sg.Input(size=(9,1), readonly=True), sg.Input(size=(9,1), readonly=True)],
          [sg.Text("Estoque Ideal"), sg.Text("Qtd. Sug. P/ Devolver")],
          [sg.Input(size=(11,1), readonly=True), sg.Input(size=(11,1), readonly=True)],
          [sg.Text("Cód. Prod."), sg.Text("     Data Valid."), sg.Text("Qtd. Dev.")],
          [sg.Input(size=(11, 1), text_color='Black', background_color='White', border_width=3, key='-COD-', focus=True, change_submits=True),
           sg.Input(size=(9, 1), text_color='Black', background_color='White', border_width=3, key='-DATA-', change_submits=True),
           sg.Input(size=(9, 1), key='-QTD-', change_submits=True, background_color='White', border_width=3)],
          [sg.Button('SEND', visible=False, bind_return_key=True, change_submits=True)],
          [sg.Button('Gravar', key='INSERT', pad=(1,3))],]

# Create a window to the user
window = sg.Window("Dev_Excesso v1.0", layout, element_justification='center', size=(235,235), margins=(2,2))

# Create an event loop
while True:
    event, values = window.read()
    # End program if user closes window
    if event == sg.WIN_CLOSED:
        break

    # delete char from input. Only accept numbers
    if len(values['-COD-']) and values['-COD-'][-1] not in ('0123456789'):
        window['-COD-'].update(values['-COD-'][:-1])

    if len(values['-DATA-']) and values['-DATA-'][-1] not in ('0123456789'):
        window['-DATA-'].update(values['-DATA-'][:-1])

    if event == '-DATA-' and len(window.FindElement(event).Get()) == 6:
        validade = str(values['-DATA-'])
        try:
            data = datetime.datetime.strptime(validade, '%d%m%y').date()
            data2 = datetime.datetime.strftime(data, '%d/%m/%y')
            window['-DATA-'].update(data2)
            window.FindElement('-QTD-').SetFocus()
        except ValueError:
            sg.popup_ok('Data inexistente, por favor redigite!')


    if len(values['-QTD-']) and values['-QTD-'][-1] not in ('0123456789'):
         window['-QTD-'].update(values['-QTD-'][:-1])


    if event == '-COD-' and ((len(window.FindElement(event).Get()) == 13) or (len(window.FindElement(event).Get()) == 14)):
        codigo = values['-COD-']
        #print(codigo)

        row = select_prod(codigo)
        if len(row) == 0:
            sg.popup('Produto não encontrado: ', codigo)

        for row in select_prod(codigo):
            window['nome_prod'].update(row[0] + ' ' + row[1] + ' ' + row[2])
            window['preco_prod'].update(row[3])
            window['estoque_prod'].update(row[4])
            window['estmin_prod'].update(row[5])
            window.FindElement('-DATA-').SetFocus()

    if event == 'SEND' and values['-QTD-'] != '':
        if values['-COD-'] == '':
            sg.popup('É Necessário digitar o código')
            window.FindElement('-COD-').SetFocus()
        else:
            qtd = values['-QTD-']

            newlist.append((codigo,
                            data2,
                            qtd))

            window['-COD-'].update(values['-COD-'][:0])
            window['nome_prod'].update(values['nome_prod'][:0])
            window['preco_prod'].update(values['preco_prod'][:0])
            window['estoque_prod'].update(values['estoque_prod'][:0])
            window['estmin_prod'].update(values['estmin_prod'][:0])
            window['-DATA-'].update(values['-DATA-'][:0])
            window['-QTD-'].update(values['-QTD-'][:0])

            window.FindElement('-COD-').SetFocus()

    if event == 'INSERT':
        sg.popup('Produtos Relacionados:', newlist, title='Teste')

        window.close()
        sg.popup_ok('Ferramenta de Dev_Excesso Encerrada!!!')


window.close()
sg.popup_ok('Ferramenta de Dev_Excesso Encerrada!!!')

# Não está na CBALT
# 7891182890045

# Está na CBALT
# 7899820806069
# 17896044936920

# All done!
