"user strict";
var sql = require("./dbModel/db.js");

//Car object constructor
var Car = function (car) {
  this.personID = car.personID;
  this.carPlate = car.carPlate;
  this.carColor = car.carColor;
  this.carName = car.carName;
  this.currentParkingLot = car.currentParkingLot;
  this.previousParkingLots = car.previousParkingLots;
};

Car.createCar = function (new_car, apiKey, result) {
  sql.query("Select * from user where ApiKey = ? ", apiKey, function (err, res) {
    if (err) {
    } else {
      var personID = res[0].PersonID;
      new_car.personID = personID;
      sql.query("INSERT INTO car set ?", new_car, function (err, res) {
        if (err) {
          console.log("error: ", err);
          result(err, null);
        } else {
          console.log(res.insertId);
          result(null, res.insertId);
        }
      });
    }
  });
};

Car.updateCar = function (apiKey, updatedCar, result) {
  sql.query("Select * from user where ApiKey = ? ", apiKey, function (err, res) {
    if (err) {
    } else {
      var personID = res[0].PersonID;
      var carPlate = updatedCar.carPlate;
      sql.query(
        "UPDATE car SET ? WHERE PersonID = ? and CarPlate = ?",
        [updatedCar, personID, carPlate],
        function (err, res) {
          if (err) {
            console.log("error: ", err);
            result(null, err);
          } else {
            result(null, res);
          }
        }
      );
    }
  });

}

module.exports = Car;
