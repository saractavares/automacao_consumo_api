from auto import scrap_master
from sender import sender_email


class master():

    def controller_master():

              
        scrap_master.db_connect()
        scrap_master.scrap()
        scrap_master.update_db()

        sender_email.con_banco()
        sender_email.enviar_email()

        print('\nTERMINOU O CONTROLLER\n')

        
