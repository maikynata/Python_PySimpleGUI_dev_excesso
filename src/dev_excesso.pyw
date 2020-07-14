#####
# Author: Maiky Nata
# Version: 1.0
#####

import psycopg2
import PySimpleGUI as sg
import datetime
import random

print = sg.Print
newlist = []
conn_string = "host='127.0.0.1' dbname='erp_teste' user='postgres' password='teste123'"

def select_prod(prod_codigo):
    try:

        connection = psycopg2.connect(conn_string)
        cursor = connection.cursor()

        sql_prod_cod_query = """select prod_codigo, prod_descricao, prod_complemento, prod_marca, prun_prvenda, prun_estoque1, 
                                prun_estmin  from produtos, produn
                                where prod_codigo=prun_prod_codigo and prun_unid_codigo='001' 
                                and prod_codbarras=%s"""
        #CAST(prod_codigo=%s as numeric)
        cursor.execute(sql_prod_cod_query, [prod_codigo])
        rows = cursor.fetchall()

        if len(rows) == 0:
            sql_prod_cbalt_query = """select prod_codigo, prod_descricao, prod_complemento, prod_marca, prun_prvenda, prun_estoque1, 
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


def select_unid(unidade):
    try:

        connection = psycopg2.connect(conn_string)
        cursor = connection.cursor()

        query_unid = """select unid_codigo from unidades
                                where unid_codigo=%s"""
        cursor.execute(query_unid, [unidade])
        row_unid_codigo = cursor.fetchall()

        return row_unid_codigo

    except(Exception, psycopg2.Error) as error:
        sg.popup_ok("Error while connecting to PostgreSQL", error)

    finally:
        # Closing database connection.
        if (connection):
            cursor.close()
            connection.close()



def cria_transacao(unidade):
    try:

        connection = psycopg2.connect(conn_string)
        cursor = connection.cursor()

        unid_cod = unidade
        # Cria a Transacao
        nextVal_transacao = """SELECT NextVal(CONCAT('transacao', %s)) As Proximo"""
        cursor.execute(nextVal_transacao, [unidade])
        nextVal = cursor.fetchone()
        dig_verif = str(random.randint(0,9))
        transacao = (unid_cod + str(nextVal[0]) + dig_verif)

        return transacao

    except(Exception, psycopg2.Error) as error:
        sg.popup_ok("Error while connecting to PostgreSQL", error)

    finally:
        # Closing database connection.
        if (connection):
            cursor.close()
            connection.close()


def insert_pendest(newlist):
    try:

        connection = psycopg2.connect(conn_string)
        cursor = connection.cursor()

        sql_update_query = """INSERT INTO PendEst (pest_operacao, pest_transacao, pest_status, pest_datamvto, pest_unid_origem, 
        pest_unid_destino, pest_prod_codigo, pest_cpes_codigo, pest_cpes_tipo, pest_catentidade, pest_codEntidade, 
        pest_sequencial, pest_valor, pest_qemb, pest_qtde, pest_qtdebx, pest_transacaobx, pest_bxcompleta, Pest_DataBaixa, 
        Pest_CtCompra, Pest_CtFiscal, Pest_CtEmpresa, Pest_CtTransf, Pest_Espe_Codigo, Pest_DataValidade, Pest_DataEntrega) 
        VALUES(CONCAT(%s, '1'), %s, 'P', CAST(%s AS DATE), %s, %s, %s, '001', 'PI', 
        'N', 0, 1, 10.27, 0, %s, 0, '', '', CAST(null AS DATE), 11.50228, 11.50228, 11.50228, 12.52944, '', CAST(%s AS DATE), 
        CAST(null AS DATE))"""

        cursor.executemany(sql_update_query, newlist)
        connection.commit()
        count = cursor.rowcount
        transacao_gravada = newlist[0][0]
        sg.popup_ok('Transação Gravada: ', transacao_gravada)


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

column1 = [[sg.Text("     Estoque Ideal"), sg.Text("      Qtd. Sug. P/ Devolver")],
          [sg.Input(size=(11,1), readonly=True), sg.Input(size=(11,1), readonly=True)]]

column_text = [[sg.Text("Unidade"), sg.Text("Descrição do Produto")],
               [sg.Input(change_submits=True, key='unidade', size=(6,1), focus=True, border_width=2, text_color='Black', background_color='#ccc'),
                sg.Input(readonly=True, key='nome_prod', size=(40,1))]]

layout = [[sg.Column(column_text, element_justification='left', pad=(1,2))],
          [sg.Text("Pr. Venda"), sg.Text("       Estoque"), sg.Text("         Est. Min")],
          [sg.Input(size=(12,1), readonly=True, key='preco_prod'),
           sg.Input(size=(12,1), readonly=True, key='estoque_prod'), sg.Input(size=(12,1), readonly=True, key='estmin_prod')],
          [sg.Text("V.M.3"), sg.Text("            V.M.12"), sg.Text("           Venda Mês")],
          [sg.Input(size=(12,1), readonly=True), sg.Input(size=(12,1), readonly=True), sg.Input(size=(12,1), readonly=True)],
          [sg.Column(column1, element_justification='center')],
          [sg.Text("Cód. Prod."), sg.Text("        Data Valid."), sg.Text("      Qtd. Dev.")],
          [sg.Input(size=(12, 1), text_color='Black', background_color='#ccc', border_width=3, key='-COD-', change_submits=True),
           sg.Input(size=(12, 1), text_color='Black', background_color='#ccc', border_width=3, key='-DATA-', change_submits=True),
           sg.Input(size=(12, 1), key='-QTD-', change_submits=True, background_color='#ccc', border_width=3)],
          [sg.Button('SEND', visible=False, bind_return_key=True, change_submits=True)],
          [sg.Button('Gravar', key='INSERT', pad=(1,2))],]

# Create a window to the user
window = sg.Window("Dev_Excesso v1.0", layout, size=(285,235), element_justification='center', margins=(2,2))

# Create an event loop
while True:
    event, values = window.read()
    # End program if user closes window
    if event == sg.WIN_CLOSED:
        break

    # delete char from input. Only accept numbers
    if len(values['unidade']) and values['unidade'][-1] not in ('0123456789'):
        window['unidade'].update(values['unidade'][:-1])

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

    if event == 'unidade' and ((len(window.FindElement(event).Get()) == 3) or (len(window.FindElement(event).Get()) == 3)):
        unidade = values['unidade']

        row = select_unid(unidade)
        if len(row) == 0:
            sg.popup('Unidade inválida: ', unidade)
        else:
            window.FindElement('-COD-').SetFocus()
            window['unidade'].update(disabled=True)
            transacao = cria_transacao(unidade)

    if event == '-COD-' and ((len(window.FindElement(event).Get()) == 13) or (len(window.FindElement(event).Get()) == 14)):
        codigo = values['-COD-']
        #print(codigo)

        row = select_prod(codigo)
        if len(row) == 0:
            sg.popup('Produto não encontrado: ', codigo)

        for row in select_prod(codigo):
            codigo_interno = row[0]
            window['nome_prod'].update(row[1] + ' ' + row[2] + ' ' + row[3])
            window['preco_prod'].update(row[4])
            window['estoque_prod'].update(row[5])
            window['estmin_prod'].update(row[6])
            window.FindElement('-DATA-').SetFocus()

    if event == 'SEND' and values['-QTD-'] != '':
        if values['-COD-'] == '':
            sg.popup('É Necessário digitar o código')
            window.FindElement('-COD-').SetFocus()
        else:
            qtd = values['-QTD-']

            today = datetime.date.today()
            dateMvto = today.strftime("%Y-%m-%d")

            data_postgres = datetime.datetime.strptime(data2, '%d/%m/%y').strftime('%Y-%m-%d')
            newlist.append((transacao,
                            transacao,
                            dateMvto,
                            unidade,
                            unidade,
                            codigo_interno,
                            qtd,
                            data_postgres))

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

        insert_pendest(newlist)
        break

window.close()
sg.popup_ok('Ferramenta de Dev_Excesso Encerrada!!!')

# Não está na CBALT
# 7891182890045

# Está na CBALT
# 7899820806069
# 17896044936920

# All done!
