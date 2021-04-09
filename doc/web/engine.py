from flask          import Flask, render_template, redirect
from flask_socketio import SocketIO     # WebSockets   library
                                        # inotify file watcher
from watchdog.observers import Observer
from watchdog.events    import FileSystemEventHandler

class Engine(Web): pass
    def __init__(self, V='Flask'): # really modular^ framework
        super().__init__(V)
        self.app = Flask(__name__) # Flask needs metaL.py path
        self.app.config['SECRET_KEY'] = config.SECRET_KEY
        self.sio = SocketIO(self.app)
    def eval(self, env=glob):
        self.route()   ; self.socket()
        self.inotify() ; self.reload()
        self.sio.run(self.app, debug=True,  # run debug server
                     host=web['host'].value,
                     port=web['port'].value)

    def socket(self, env=glob): # WebSocket.IO async messaging

        @self.sio.on('localtime')
        def localtime():
            self.sio.emit('localtime', Time().json(), 
                                        broadcast=True)
        @self.sio.on('connect')
        def connect(): localtime()
    ## classical HTTP routing
    def route(self, env=glob):

        @self.app.route('/')
        def index(env=glob):
            return render_template('index.html',
                                    glob=glob, env=env)

        @self.app.route('/dump/')
        @self.app.route('/dump/<path:path>')
        def dump(path='', env=glob):
            for i in path.split('/'): # lookup
                if i: env = env[i]
            return render_template('dump.html',
                                    glob=glob, env=env)
    def reload(self):
        self.no_caching()
        # self.sio.emit('reload')

    def no_caching(self):
        # middleware: block caching for automatic page reload
        @self.app.after_request
        def force_no_caching(req):
            req.headers["Cache-Control"] = \
                        "no-cache, no-store, must-revalidate"
            req.headers["Pragma"] = "no-cache"
            req.headers["Expires"] = "0"
            req.headers['Cache-Control'] = 'public, max-age=0'
            return req

    def inotify(self):
        watch = Observer()
        sio = self.sio      # var for clojure

        class event_handler(FileSystemEventHandler):
            def on_closed(self, filev):
                if not filev.is_directory:
                    sio.emit('reload', f'{filev}')

        watch.schedule(event_handler(), 'static',
                                            recursive=True)
        watch.schedule(event_handler(), 'templates',
                                            recursive=True)
        watch.start()

## system init

if __name__ == '__main__':
    if sys.argv[1] == 'all':
        pass # circular.sync()
    elif sys.argv[1] == 'web':
        Engine().eval(glob)
    else:
        raise SyntaxError(sys.argv)
