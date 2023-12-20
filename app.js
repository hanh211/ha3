const http=require('http');
const fs=require('fs');
http.createServer(function(req,res){
  fs.readFile('index.html',function(err,data){
    res.writeHead(200,{
      'Content-Type':'text/html',
      'Content-Length':data.length,
    });
    res.write(data);
    res.end();
  });
}).listen(process.env.PORT || 3000);
