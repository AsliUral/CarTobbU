const express = require("express"),
  app = express(),
  bodyParser = require("body-parser"),
  path = require("path"),
  busboy = "then-busboy",
  fileUpload = require("express-fileupload");

/* Local Port */
//port = process.env.PORT || 3000;

/* Google Cloud Port */

port = process.env.PORT || 8080;

const mysql = require("mysql");

//gc.getBuckets().then((x) => console.log(x));

//*Local DB Connection Configurations*
/*
const mc = mysql.createConnection({
  host: "localhost",
  user: "root",
  password: "<Enter password here>",
  database: "smart-car-park-tobb-etu",
});
*/

/* Google Cloud Deployment */

const mc = mysql.createConnection({
  socketPath:
    "/cloudsql/smart-car-park-api:us-central1:tobb-etu-smart-car-park",
  user: "samaritan",
  password: "samaritan",
  database: "smart_car_park_tobb_etu",
});

// connect to database
mc.connect();

app.listen(port);
app.set("views", __dirname + "/views");
app.set("view engine", "ejs");

console.log("API server started on: " + port);

app.use(bodyParser.urlencoded({ extended: true }));
app.use(bodyParser.json());
app.use(express.static(path.join(__dirname, "public")));
app.use(fileUpload());

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

var penaltyReportRoutes = require("./app/routes/penaltyRoutes");
penaltyReportRoutes(app);
