import config

import os, sys, re
import datetime as dt

MODULE = os.getcwd().split('/')[-1]

## base object graph node class = Marvin Minsky's Frame
class Object:
    def __init__(self, V):
        if isinstance(V, Object): V = V.value
        ## scalar value: name, string, number,..
        self.value = V
        ## associative array = environment = hash map
        self.slot = {}
        ## ordered container = vector = stack = nested AST
        self.nest = []
        ## unical [g]lobal [id]entifier: to distinct and address objects
        self.gid = id(self)

    ## Python types boxing
    def box(self, that):
        if isinstance(that, Object): return that
        if isinstance(that, int): return Integer(that)
        if isinstance(that, str): return String(that)
        if that == None: return Nil()
        # unknown
        raise TypeError(['box', type(that), that])

    ## @name tree-like text dump

    ## `print` callback
    def __repr__(self): return self.dump()
    ## used in `pytest`s
    def test(self): return self.dump(test=True)

    ## full text tree dump
    def dump(self, cycle=[], depth=0, prefix='', test=False):
        # header
        ret = self.pad(depth) + self.head(prefix, test)
        # block recursion on cyclic references
        if not depth: cycle = []
        if self.gid in cycle: return ret + ' _/'
        else: cycle.append(self.gid)
        # slot{}s
        for i in self.keys():
            ret += self[i].dump(cycle, depth + 1, f'{i} = ', test)
        # nest[]ed
        for j, k in enumerate(self.nest):
            ret += k.dump(cycle, depth + 1, f'{j}: ', test)
        # subgraph
        return ret

    ## tree padding proportinal to recursion depth
    def pad(self, depth): return '\n' + '\t' * depth

    ## short single line <T:V> header
    def head(self, prefix='', test=False):
        gid = '' if test else f' @{self.gid:x}'
        return f'{prefix}<{self.tag()}:{self.val()}>{gid}'

    ## `<T:` type/class tag
    def tag(self): return self.__class__.__name__.lower()

    ## `:V>` value represented for dumps (shorted strings,..)
    def val(self): return f'{self.value}'

    ## @name de/serialize

    def sync(self):
        raise NotImplementedError(['sync', self])

    def json(self, depth=0, prefix=''):
        raise NotImplementedError(['json', self, depth, prefix])

    ## @name operator

    ## `A.keys()` sorted slot keys
    def keys(self):
        return sorted(self.slot.keys())

    ## `iter(A)` iterator: `for i in Object():`
    def __iter__(self): return iter(self.nest)

    ## `A[key]` get node slot/nest element by name or index
    def __getitem__(self, key):
        if isinstance(key, str): return self.slot[key]
        if isinstance(key, int): return self.nest[key]
        raise TypeError(['__getitem__', type(key), key])

    ## `A[key] = B` assign by name/index
    def __setitem__(self, key, that):
        that = self.box(that)
        if isinstance(key, str): self.slot[key] = that; return self
        if isinstance(key, int): self.nest[key] = that; return self
        raise TypeError(['__setitem__', type(key), key])

    ## `A << B -> A[B.tag] = B` left/tag slot assignment
    def __lshift__(self, that):
        that = self.box(that)
        return self.__setitem__(that.tag(), that)

    ## `A >> B -> A[B.val] = B` right/val slot assignment
    def __rshift__(self, that):
        that = self.box(that)
        return self.__setitem__(that.val(), that)

    ## `A // B -> A.push(B)` stack-like push to end of vector
    def __floordiv__(self, that):
        that = self.box(that)
        self.nest.append(that); return self

    ## @name code generation

    def gen(self, depth, to):
        raise NotImplementedError(['gen', self, depth, to])

    ## f'strings' can be used for code generation
    def __format__(self, spec):
        raise NotImplementedError(['__format__', self, spec])

    ## @name computation

    ## Lisp eval() in context
    def eval(self, env):
        raise NotImplementedError(['eval', self, env])

    ## Lisp apply() to `that` object in context
    def apply(self, env, that):
        raise NotImplementedError(['apply', self, env, that])


class Primitive(Object):
    ## evaluates to itself
    def eval(self, env): return self

class Nil(Primitive):
    def __init__(self): super().__init__('')
    html = '\u2014'
    def html(self): return Nil.html

## Variable name
class Name(Primitive):
    ## evaluates by name lookup in `env`
    def eval(self, env): return env[self.value]

class String(Primitive):
    def val(self):
        ret = ''
        for c in self.value:
            if c == '\n': ret += '\\n'
            elif c == '\t': ret += '\\t'
            else: ret += c
        return ret

## floating point
class Number(Primitive):
    def __init__(self, V, prec=4):
        Primitive.__init__(self, float(V))
        ## precision: digits after decimal `.`
        self.prec = prec

    def val(self):
        if self.value == None: return Nil.html
        if isinstance(self.value, float):
            if not self.prec:
                return f'{int(self.value)}'
            else:
                return f'{round(self.value,self.prec)}'
        raise TypeError(['val', type(self.value), self.value])

class Integer(Number):
    def __init__(self, V):
        Primitive.__init__(self, int(V))
        self.prec = 0

    def val(self):
        if self.value == None: return Nil.html
        if isinstance(self.value, int):
            return f'{self.value}'
        raise TypeError(['val', type(self.value), self.value])


# data container
class Container(Object):
    ## can be created with optional name
    def __init__(self, V=''): super().__init__(V)

## ordered container
class Vector(Container):
    def json(self, depth=0, prefix=''):
        ret = f'{prefix}{tab*depth}[\n'
        ret += f'{tab*depth}]\n'
        return ret

## associative array
class Map(Container): pass

## unical set (unordered)
class Set(Container): pass

## LIFO
class Stack(Container): pass

## FIFO: deque or primitive message queue
class Queue(Container): pass


## EDS: executable data elements
class Active(Object): pass

## environment = namespace
class Env(Active, Map): pass


## global environment
glob = Env('global'); glob << glob >> glob


## input/output
class IO(Object): pass

class Time(IO):
    def __init__(self):
        self.now = dt.datetime.now()
        super().__init__(f'{self.now}')
        self.date = self.now.strftime('%Y-%m-%d')
        self.time = self.now.strftime('%H:%M:%S')

    def json(self):
        return {"date": self.date, "time": self.time}

class Path(IO): pass

class Dir(IO): pass

class File(IO): pass


## metaprogramming: source code components
class Meta(Object): pass


## application metainformation: app name, author, package version,...
info = Meta('info'); glob >> info

## software module/library
class Module(Meta):
    def __init__(self, V=MODULE): super().__init__(V)


## redefine MODULE as Module object
MODULE = Module(); info << MODULE

## application
class App(Module): pass


# application-wide state
app = App(MODULE); glob << app


## base networking
class Net(IO): pass

class Socket(Net): pass

## IP address
class IP(Net): pass

## IP port
class Port(Net): pass

class EMail(Net): pass


## Author's e-mail
EMAIL = EMail('dponyatov@gmail.com'); info << EMAIL


## Web-specific components and services
class Web(Net): pass


## web interface data
web = Web('interface'); glob << web
web['host'] = IP(config.HOST); web << Port(config.PORT)

## current user session
class Session(Web):
    def __init__(self, V=''): super().__init__(V)


## documenting
class Doc(Object): pass

## application title
class Title(Doc): pass


TITLE = Title(MODULE); info << TITLE

class Author(Doc): pass


AUTHOR = Author('Dmitry Ponyatov')
AUTHOR.ru = 'Понятов Д.А.'
AUTHOR << EMAIL

class DB(Object): pass

class Model(DB): pass

class User(Model): pass


user = DB('user'); glob >> user

ponyatov = User('ponyatov'); user // ponyatov >> ponyatov
ponyatov['fio'] = AUTHOR.ru
ponyatov << EMAIL

ses = Session(); ponyatov // ses; ses << ponyatov
glob['ses'] = ses


from flask import Flask, render_template, redirect
from flask_socketio import SocketIO

from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

class Engine(Web):
    def __init__(self, V='Flask'): # really modular^ framework
        super().__init__(V)
        self.app = Flask(__name__) # Flask needs metaL.py path
        self.app.config['SECRET_KEY'] = config.SECRET_KEY
        self.sio = SocketIO(self.app)

    def eval(self, env=glob):
        self.route(); self.socket()
        self.inotify(); self.reload()
        self.sio.run(self.app, debug=True,  # run debug server
                     host=web['host'].value,
                     port=web['port'].value)

    ## WebSocket.IO async messaging
    def socket(self, env=glob):

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
            return render_template('index.html', glob=glob, env=env)

        @self.app.route('/dump/')
        @self.app.route('/dump/<path:path>')
        def dump(path='', env=glob):
            for i in path.split('/'): # lookup
                if i: env = env[i]
            return render_template('dump.html', glob=glob, env=env)

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
        watch = Observer(); sio = self.sio # var for clojure

        class event_handler(FileSystemEventHandler):
            def on_closed(self, filev):
                if not filev.is_directory:
                    sio.emit('reload', f'{filev}')
        watch.schedule(event_handler(), 'static', recursive=True)
        watch.schedule(event_handler(), 'templates', recursive=True)
        watch.start()


web << Engine()

## system init

if __name__ == '__main__':
    if sys.argv[1] == 'all':
        pass # circular.sync()
    elif sys.argv[1] == 'web':
        Engine().eval(glob)
    else:
        raise SyntaxError(sys.argv)
