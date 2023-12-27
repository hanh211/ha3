var express=require("express")
var app=express();
app.use(express.static("public"));
var server=require("http").Server(app);
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

app.get("/ap",function(req,res){
  console.log("hello");
});
