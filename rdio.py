#!/usr/bin/python

from gi.repository import Gtk
from gi.repository import WebKit
from gi.repository import Soup
import os, sys

class Rdio(Gtk.Window):
	def __init__(self):
		Gtk.Window.__init__(self, title="Rdio")
		# Initial windows size
		self.set_size_request(800,600)

		self.create_app_dir()
		self.build_ui()
		self.config_ui()

	def create_app_dir(self):
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
		self.webview.load_uri(url)
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



app = Rdio()
app.connect("delete-event", Gtk.main_quit)
app.show_all()
Gtk.main()
