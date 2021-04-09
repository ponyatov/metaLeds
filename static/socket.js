
sio = io()

reload = {
    timeout: 222,
    handler: undefined,
    go:      function()        { location.reload() },
    start:   function(timeout) { reload.handler = setTimeout(reload.go,timeout) },
    stop:    function()        { clearTimeout(reload.handler) },
}

sio.on('connect',(msg)=>{
    console.log('sio','connect',msg)
    $('#localtime').addClass('online').removeClass('offline')
    reload.stop()
})

sio.on('disconnect',(msg)=>{
    console.log('sio','disconnect',msg)
    $('#localtime').addClass('offline').removeClass('online')
    reload.start(reload.timeout)
})

sio.on('reload',(msg)=>{
    console.log('sio','reload',msg)
    reload.go()
})

sio.on('localtime',(msg)=>{
    console.log('sio','localtime',msg)
    $('#localtime').text(msg.date+" | "+msg.time)
})

function gui_onchange(gid,name,value) {
    console.log('gui/onchange',[gid,name,value])
    sio.emit('gui/onchange',[gid,name,value])
}

sio.on('gui/changed',(msg)=>{
    console.log('sio','gui/changed',msg)
    $('#'+msg[1]).removeClass('error')
})

sio.on('gui/error',(msg)=>{
    console.log('sio','gui/error',msg)
    $('#'+msg[1]).addClass('error')
})
