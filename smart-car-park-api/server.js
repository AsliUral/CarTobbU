const express = require("express"),
  app = express(),
  bodyParser = require("body-parser");

/* Local Port */
//port = process.env.PORT || 3000;

/* Google Cloud Port */
port = process.env.PORT || 8080;

const mysql = require("mysql");

/*

*Local DB Connection Configurations* 

const mc = mysql.createConnection({
  host: "localhost",
  user: "root",
  password: "<Enter Your DB Password Here!>",
  database: "smart-car-park-tobb-etu"
});

*/

/* Google Cloud Deployment */
const mc = mysql.createConnection({
  socketPath:
    "/cloudsql/smart-car-park-api:us-central1:tobb-etu-smart-car-park",
  user: "samaritan",
  password: "samaritan",
  database: "smart_car_park_tobb_etu"
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
