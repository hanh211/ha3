const express=require("express");
const app=express();
app.use(express.static("public"));
const server = require("http").Server(app);
app.set("view engine","ejs");
app.set("views","public");
// const port=3000;
app.listen(process.env.PORT || 3000);
// app.use(bodyParser.json());
// app.use(bodyParser.urlencoded({extended:false}));

app.get("/",(req,res)=>{
  res.render("a");
});

// app.listen(port,()=>{
//   console.log('listen 3000')
// });
