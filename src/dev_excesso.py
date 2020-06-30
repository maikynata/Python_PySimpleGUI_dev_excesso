import psycopg2
import PySimpleGUI as sg

print = sg.Print

def select_prod():
    try:

        conn_string = "host='127.0.0.1' dbname='erp_teste' user='postgres' password='teste123'"
        connection = psycopg2.connect(conn_string)
        cursor = connection.cursor()

        sql_update_query = """select prod_descricao, prod_complemento, prod_marca, prun_prvenda, prun_estoque1, 
                                prun_estmin  from produtos, produn
                                where prod_codigo=prun_prod_codigo and prun_unid_codigo='001' 
                                and prod_codigo in (101567,649848,590045)"""
        cursor.execute(sql_update_query)
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


def update_prod():
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


# Lookup dictionary that aps button to function to call
#dispatch_dictionary = {'Adicionar IDs':select_prod, 'Remover IDs':update_prod}


# Layout the design of the GUI
QT_ENTER_KEY1 = 'special 16777220'
QT_ENTER_KEY2 = 'special 16777221'
#enter_buttons = [chr(13), "Return:13"]

dispatch_dictionary = {'Adicionar IDs':select_prod, 'Remover IDs':update_prod}

layout = [[sg.Text("Descrição do Produto", auto_size_text=True)],
          [sg.Input('Tinta Biocolor 1.0 Preto Niasi', readonly=True, size=(37,1))],
          [sg.Text("Pr. Venda"), sg.Text("       Estoque"), sg.Text("       Est. Min", justification='right')],
          [sg.Input(size=(11,1), readonly=True), sg.Input(size=(11,1), readonly=True), sg.Input(size=(11,1),readonly=True)],
          [sg.Text("V.M.3"), sg.Text("            V.M.12"), sg.Text("        Venda Mês"), ],
          [sg.Input(size=(11,1), readonly=True), sg.Input(size=(11,1), readonly=True), sg.Input(size=(11,1), readonly=True)],
          [sg.Text("Estoque Ideal"), sg.Text("Qtd. Sug. P/ Devolver")],
          [sg.Input(size=(11,1), readonly=True), sg.Input(size=(11,1), readonly=True)],
          [sg.Text("Cód. Prod."), sg.Text("     Qtd. Dev.")],
          [sg.Input(size=(11, 1), background_color='#bebbbb', key='-COD-', focus=True), sg.Input(size=(11, 1), key='-QTD-')],
          [sg.Button('SEND', visible=False, bind_return_key=True)],]

# Create a window to the user
window = sg.Window("Dev_Excesso", layout, element_justification='center')

# Create an event loop
while True:
    event, values = window.read()
    # End program if user closes window
    if event == sg.WIN_CLOSED:
        break
    if event == 'SEND':
        query = values['-COD-'].rstrip()
        # EXECUTE YOUR COMMAND HERE
        sg.popup('The command you entered was {}'.format(query))
        #sg.popup('You have submited ENTER SEND')

    else:
        event == '-QTD-'
        sg.popup('teste')

window.close()

# All done!
sg.popup_ok('Ferramenta de Dev_Excesso Encerrada!!!')

