"user strict";

var mysql = require("mysql");

//local mysql db connection
var connection = mysql.createConnection({
  host: "localhost",
  user: "root",
  password: "Enter Here Your DB Password to Develop",
  database: "smart-car-park-tobb-etu"
});

connection.connect(function(err) {
  if (err) throw err;
});

module.exports = connection;
