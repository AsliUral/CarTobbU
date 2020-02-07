const express = require("express"),
  app = express(),
  bodyParser = require("body-parser");
port = process.env.PORT || 3002;

const mysql = require("mysql");
// connection configurations
const mc = mysql.createConnection({
  host: "localhost",
  user: "root",
  password: "enterPasswordhere",
  database: "smart-car-park-tobb-etu"
});

// connect to database
mc.connect();

app.listen(port);

console.log("API server started on: " + port);

app.use(bodyParser.urlencoded({ extended: true }));
app.use(bodyParser.json());

var userRoutes = require("./app/routes/userRoutes");
userRoutes(app);

var parkingLotsRoutes = require("./app/routes/parkingLotsRoutes");
parkingLotsRoutes(app);

var markingRoutes = require("./app/routes/markingRoutes");
markingRoutes(app);

var parkZoneRoutes = require("./app/routes/parkZoneRoutes");
parkZoneRoutes(app);

var carRoutes = require("./app/routes/carRoutes");
carRoutes(app);


