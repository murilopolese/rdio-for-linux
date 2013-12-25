const Lang = imports.lang;
const Gtk = imports.gi.Gtk;
const WebKit = imports.gi.WebKit;
const Soup = imports.gi.Soup;

const Application = new Lang.Class({
    Name: 'Application',
    _init: function() {
        this.application = new Gtk.Application();
        this.application.connect('activate', Lang.bind(this, this._onActivate));
        this.application.connect('startup', Lang.bind(this, this._onStartup));
    },
    _buildUI: function() {
        // Application main window
        this._window = new Gtk.ApplicationWindow({ 
            application: this.application,
            title: "Rdio" 
        });
        this._window.set_default_size(800, 600);
        // Scrollable container
        let sw = new Gtk.ScrolledWindow({});
        this._window.add(sw);
        // Web view
        let view = new WebKit.WebView();
        view.load_uri('https://rdio.com');
        sw.add(view);
        // Cookies persistance
        let session = WebKit.get_default_session();
        let cookies = new Soup.CookieJarText({
            filename: './cookies.txt'
        });
        cookies.set_accept_policy(Soup.CookieJarAcceptPolicy.ALWAYS);
        cookies.attach(session);
        // System tray icon
        let tray = new Gtk.StatusIcon();
        tray.file = './rdio-icon.png';
        tray.connect('activate', Lang.bind(this, this._toggleWindowVisibility));

    },
    _onActivate: function() {
        this._window.show_all();
    },
    _onStartup: function() {
        this._buildUI();
    },
    _toggleWindowVisibility: function() {
        if(this._window.visible) {
            this._window.hide();
        } else {
            this._window.show_all();
        }
    }
});

//run the application
let app = new Application();
app.application.run(ARGV);