import gi
gi.require_version('Gtk', '3.0') 
from gi.repository import Gtk 
from gi.repository import Gdk 
import Llegir
import threading                           #Import threads 

class Finestra(Gtk.Window):
    def __init__(self):
         super().__init__()
         css_provider = Gtk.CssProvider()
         css_provider.load_from_path("style/style.css")
         Gtk.StyleContext().add_provider_for_screen(Gdk.Screen.get_default(), css_provider, Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION)

         # Creem la finestra
         self.set_border_width(10)

         # Creem una caixa per situar l'etiqueta a dalt i el botó a baix
         self.box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=20)
         # Afegim la caixa a la finestra
         self.add(self.box)

         # Creem una caixa eventual, que canviarà de color
         self.evbox = Gtk.EventBox()
         self.evbox.get_style_context().add_class("blue_label")
         #self.evbox.override_background_color(0, Gdk.RGBA(0,0,8,1))

         # Creem l’etiqueta
         self.label = Gtk.Label(label="Text")
         self.label.set_text("<span>Please, login with your university card</span>")
         self.label.set_use_markup(True)
         self.label.set_name("Bluelabel")
         self.label.set_size_request(500,100)

         # L'afegim a la caixa
         self.evbox.add(self.label)

         # Creem el botó
         self.button = Gtk.Button(label="Clear")
         self.button.connect("clicked", self.clicked)

         # L'afegim a la caixa
         self.box.pack_start(self.evbox, True, True, 0)
         self.box.pack_start(self.button, True, True, 0)

         # Creem i comencem un Thread
         thread = threading.Thread(target=self.scan_uid)
         thread.setDaemon(True)
         thread.start()

         # Mostrar-ho tot
         self.show_all()
         Gtk.main()


    # Funció que es crida en pulsar el botó
    def clicked(self, widget):
         if self.label.get_text()!="Please, login with your university card":
               # Canviem de nou la label a la inicial, la blava
               self.label.set_label('<span foreground="white" size="x-large">Please, login with your university card</span>')
               self.evbox.get_style_context().remove_class("red_label")
               self.evbox.get_style_context().add_class("blue_label")

               # Tornem a començar el Thread
               thread = threading.Thread(target=self.scan_uid)
               thread.start()

    # Funció que es crida quan la funció readuid retorna l'UID de la targeta
    def scan_uid(self):
         # Creem el lector i llegim l'UID
         uid=0
         llegir = Llegir.Llegir()
         uid = llegir.llegir_targeta()

         if uid != 0:
               # Canviem la label a la de color vermell que mostra l'UID
               self.label.set_label('<span foreground="white" size="x-large">UID: '+uid+'</span>')
               self.evbox.get_style_context().remove_class("blue_label")
               self.evbox.get_style_context().add_class("red_label")

win = Finestra()
win.connect("destroy",Gtk.main_quit)
win.show_all()
Gtk.main()


