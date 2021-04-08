class Web(Net): pass

## web interface data
web = Web('interface') ; glob << web
web['host'] = IP(config.HOST) ; web << Port(config.PORT)
