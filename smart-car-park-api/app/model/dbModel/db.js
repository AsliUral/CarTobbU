"user strict";

var mysql = require("mysql");

/*
*Local DB Connection Configurations*

var connection = mysql.createConnection({
  host: "localhost",
  user: "root",
  password: "<Enter Your DB Password Here!>",
  database: "smart-car-park-tobb-etu"
});
*/

/* Google Cloud Deployment */
var connection = mysql.createConnection({
  socketPath:
    "/cloudsql/smart-car-park-api:us-central1:tobb-etu-smart-car-park",
  user: "samaritan",
  password: "samaritan",
  database: "smart_car_park_tobb_etu"
});

connection.connect(function(err) {
  if (err) throw err;
});

module.exports = connection;
