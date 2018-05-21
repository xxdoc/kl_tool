var net = require('net');
var server = net.createServer(function(c) { //'connection' listener
  console.log('client connected');
  c.on('end', function() {
    console.log('client disconnected');
  });
  c.write('<cross-domain-policy><allow-access-from domain="*" secure="false"/><allow-access-from domain="*" to-ports="*" secure="false"/><allow-http-request-headers-from domain="*" headers="*"/></cross-domain-policy>');
  c.end();
});
server.listen(843, function() { //'listening' listener
  console.log('server bound');
});

function noop(err){console.log(err);}
process.on('uncaughtException', noop)