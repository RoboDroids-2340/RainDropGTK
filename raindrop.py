import os

from gi.repository import Gtk
from scenes.user_management import LoginView, RegisterView
from pymongo import MongoClient

build_file = gtk_builder_file = os.path.splitext(__file__)[0] + '.ui'

STORAGE_URL = "https://raindrop-3c2ba.firebaseio.com"

MONGO_CLIENT = MongoClient('localhost', 27017)
DATABASE = MONGO_CLIENT['raindrop']

class Application(object):
    def __init__(self):
        self.builder = Gtk.Builder()
        self.builder.add_from_file(gtk_builder_file)
        
        self.window = self.builder.get_object('main_window')
        self.stage = self.builder.get_object('stage')
        self.scene_start = self.builder.get_object('scene_start')
        self.stage.pack_end(self.scene_start ,
                            True,
                            True,
                            10
                        )
        
        self.login_view = None
        self.register_view = None

        self.button_login = self.builder.get_object('main_login')
        self.button_register = self.builder.get_object('main_register')

        self.window.connect('destroy', self.signal_window_destroy)
        self.button_login.connect('clicked', self.signal_window_login)
        self.button_register.connect('clicked', self.signal_window_register)

        self.window.show()        
    
    def signal_window_destroy(self, _):
        self.window.destroy()
        Gtk.main_quit()

    def signal_window_login(self, _):
        self.scene_login = self.builder.get_object('scene_login')
        self.stage.remove(self.scene_start)
        self.stage.pack_end(self.scene_login,
                            True,
                            True,
                            10
                        )
        
        if not self.login_view:
            self.login_view = LoginView(self.scene_start, self.stage, self.builder, DATABASE, self.window)
        
                    

    def signal_window_register(self, _):
        self.scene_register = self.builder.get_object('scene_register')
        self.stage.remove(self.scene_start)
        self.stage.pack_end(self.scene_register,
                            True,
                            True,
                            10
                        )
        if not self.register_view:
            self.register_view = RegisterView(self.scene_start, self.stage, self.builder, DATABASE, self.window)

if __name__ == '__main__':
    Application()
    Gtk.main()
