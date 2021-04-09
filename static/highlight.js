
function g(w)    { return w.join("") }
function s(c,g)  { return "<span class="+c+">"+g+"</span>" }
function u(rl)   { return "<a href="+rl+">"+rl+"</a>" }
function e(mail) { return "<a href=mailto:"+mail+">"+mail+"</a>" }

shared = `
eq      = w:" = "                 {return s("op",w)}
int     = n:[0-9]+                {return s("integer",g(n))}
hex     = "0x" n:[0-9a-fA-F]+     {return "0x"+s("integer",g(n))}
bin     = "0b" n:[01]+            {return "0b"+s("integer",g(n))}
`

dump = peg.generate(`
dump    = w:(class/gt/hash/cycle/slot/hex/bin/int/.)*

email   = n:name a:"@" d:domain   {return e(n+a+d)}
url     = h:"http://" d:domain    {return u(h+d)}
domain  = w:[a-z\.\-]+            {return g(w)}

slot    = n:name e:eq             {return s("slot",n)+e}
class   = l:lt n:name c:":"       {return l+s("clazz",n)+s("op",c)}
name    = w:[a-zA-Z0-9А-Яа-я_]+   {return g(w)}
lt      = "<"                     {return s("lg","&lt;")}
gt      = "> "                    {return s("lg","&gt; ")}
hash    = a:"@" w:[0-9a-f]+       {return s("hash",a+g(w))}
cycle   = w:" _/"                 {return s("op",w)}
`+shared)

metaL = peg.generate(`
metaL   = w:(comment/hex/bin/int/.)*

comment = h:"#" c:[ a-z]*         {return s("comment",h+g(c))}
`+shared)

$(
    $(".dump").each(
        function(idx,item) {
            $(this).html(
                dump.parse(
                    $(this).text()))}))
$(
    $("#cli").each(
        function(idx,item) {
            $(this).html(
                metaL.parse(
                    $(this).text()))}))
