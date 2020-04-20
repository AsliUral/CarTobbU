"user strict";
var sql = require("./dbModel/db.js");

//ParkingLot object constructor
var Penalty = function (penalty) {
  this.id = penalty.id;
  this.date = penalty.date;
  this.time = penalty.time;
  this.type = penalty.type;
  this.carPlate = penalty.carPlate;
  this.notes = penalty.notes;
  this.image = penalty.image;
};

/* Get All Penalties */
Penalty.getAllPenalties = function (result) {
  sql.query("Select * from penalty", function (err, res) {
    if (err) {
      console.log("error: ", err);
      result(null, err);
    } else {
      console.log("penalties : ", res);

      result(null, res);
    }
  });
};
