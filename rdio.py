#!/usr/bin/python

from gi.repository import Gtk
from gi.repository import WebKit
from gi.repository import Soup
from datetime import datetime
import os, sys

class Rdio(Gtk.Window):
	def __init__(self):
		Gtk.Window.__init__(self, title="Rdio")
		# Initial windows size
		self.set_size_request(1024,600)

		self.create_app_dir()
		self.build_ui()
		self.config_ui()
		self.tray()
		self.set_icons()

	def create_app_dir(self):
		self.current_folder = os.path.dirname(os.path.realpath(__file__))
		self.user_home = os.path.expanduser('~');
		self.user_data_dir = self.user_home + "/.local/share/rdio"
		if os.path.isdir(self.user_data_dir) == False:
			os.makedirs(self.user_data_dir)	

	def build_ui(self):
		# Create a scrolled window to wrap the webview
		self.scrolled = Gtk.ScrolledWindow()
		# Create the webview
		self.webview = WebKit.WebView()
		# Set Rdio url as webview initial location
		url = "https://rdio.com/"
		# self.webview.load_uri(url)
		# Add webview to scrolled window
		self.scrolled.add(self.webview)
		# Add scrolled to main window
		self.add(self.scrolled)

	def config_ui(self):
		# Disable context menu
		settings = self.webview.get_settings()
		settings.set_property('enable-default-context-menu', False)
		self.webview.set_settings(settings)
		uri = self.user_data_dir + '/cookiejar'
		cookiejar = Soup.CookieJarText.new(uri, False)
		cookiejar.set_accept_policy(Soup.CookieJarAcceptPolicy.ALWAYS)
		session = WebKit.get_default_session()
		session.add_feature(cookiejar)

	def tray(self):
		self.visible = True;
		self.statusicon = Gtk.StatusIcon()
		self.statusicon.connect("activate", self.activate)
		self.statusicon.connect("popup_menu", self.popup)
		self.statusicon.set_visible(True)

	def set_icons(self):
		self.statusicon.set_from_file(self.current_folder+'/resources/icon-25x25.png')
		self.set_icon_from_file(self.current_folder+"/resources/icon-96x96.png")
		

	def activate(self, widget, data=None):
		if self.visible == True:
			self.hide()
			self.visible = False;
		else :
			self.show_all()
			self.present()
			self.visible = True;
		return True;

	def popup(self, button, widget, data=None):
		self.menu = Gtk.Menu()
		quit = Gtk.MenuItem()
		quit.set_label("Quit")
		quit.connect("activate", Gtk.main_quit)

		self.menu.append(quit)

		self.menu.show_all()

		def pos(menu, icon):
			return (Gtk.StatusIcon.position_menu(menu, icon))

		self.menu.popup(None, None, pos, button, 1, data)


app = Rdio()
app.connect("delete-event", app.activate)
app.show_all()
Gtk.main()
