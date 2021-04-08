from metaL import *

def test_metaL(): assert True

def test_object_hello():
    hello = Object('Hello')
    assert hello.test() == '\n<object:Hello>'
    hello // hello
    assert hello.test() == '\n<object:Hello>\n\t0: <object:Hello> _/'

def test_object_world():
    world = Object('World')
    assert world.test() == '\n<object:World>'
    # hello // world
