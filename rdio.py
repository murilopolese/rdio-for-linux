#!/usr/bin/python

from gi.repository import Gtk
from gi.repository import WebKit

class Rdio(Gtk.Window):
	def __init__(self):
		Gtk.Window.__init__(self, title="Rdio")
		# Initial windows size
		self.set_size_request(800,600)
		# Create a scrolled window to wrap the webview
		self.scrolled = Gtk.ScrolledWindow()
		# Create the webview
		self.webview = WebKit.WebView()
		# Disable context menu
		settings = self.webview.get_settings()
		settings.set_property('enable-default-context-menu', False)
		self.webview.set_settings(settings)
		# Set Rdio url as webview initial location
		url = "https://rdio.com/"
		self.webview.load_uri(url)
		# Add webview to scrolled window
		self.scrolled.add(self.webview)
		# Add scrolled to main window
		self.add(self.scrolled)

app = Rdio()
app.connect("delete-event", Gtk.main_quit)
app.show_all()
Gtk.main()
