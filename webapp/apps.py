from django.apps import AppConfig

import threading
import queue


import webapp.machine.cofi_app

class WebappConfig(AppConfig):
    name = 'webapp'
    send = queue.Queue()
    receive = queue.Queue()

    def ready(self):
        threading.Thread(target=webapp.machine.cofi_app.coffee, args=(self.send,self.receive,)).start()



