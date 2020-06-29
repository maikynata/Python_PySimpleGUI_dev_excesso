import psycopg2
import PySimpleGUI as sg

print = sg.Print

def add_ids():
    try:

        conn_string = "host='10.14.0.6' dbname='erp' user='powerbi' password='B3L3Z4.powerbi'"
        connection = psycopg2.connect(conn_string)
        cursor = connection.cursor()

        sql_update_query = """update produtos
                              set prod_extra3 = CONCAT(prod_extra3,',98,18')
                              where prod_codigo in (select prun_prod_codigo from produn
                              where prun_unid_codigo='001' and prun_setor='ECOMMERCE' and prun_oferta='S')"""
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


def remove_ids():
    try:

        conn_string = "host='10.14.0.6' dbname='erp' user='powerbi' password='B3L3Z4.powerbi'"
        connection = psycopg2.connect(conn_string)
        cursor = connection.cursor()

        sql_update_query = """update produtos
                              set prod_extra3 = removed_id_oferta.ids_categ from 
                              (SELECT prod_codigo, prod_descricao, prod_complemento, prod_marca, prod_extra3, 
                              regexp_replace(prod_extra3, ',\m98,18', '', 'gi') as ids_categ from produtos
                              where (prod_extra3 like '%,98' or prod_extra3 like '%,18') order by prod_codigo) as removed_id_oferta
                              where produtos.prod_codigo=removed_id_oferta.prod_codigo"""
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
dispatch_dictionary = {'Adicionar IDs':add_ids, 'Remover IDs':remove_ids}

# Layout the design of the GUI
layout = [[sg.Text("Adicionar ou Remover IDs de Oferta",auto_size_text=True)],
          [sg.Button("Adicionar IDs"), sg.Button("Remover IDs", button_color=('red','#FFFFFF'))],]

# Create a window to the user
window = sg.Window("Category Off", layout)

# Create an event loop
while True:
    event, values = window.read()
    # End program if user closes window or
    # presses the OK button
    if event == sg.WIN_CLOSED or event == 'Cancelar':  # if user closes window or clicks cancel
        break
    if event in dispatch_dictionary:
        func_to_call = dispatch_dictionary[event]  # get function from dispatch dictionary
        func_to_call()
    else:
        sg.popup_ok('Event {} not in dispatch dictionary'.format(event))

window.close()

# All done!
sg.popup_ok('Ferramenta de Gestão de IDs Encerrada!!!')

