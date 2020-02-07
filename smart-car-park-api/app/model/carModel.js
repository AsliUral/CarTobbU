"user strict";
var sql = require("./dbModel/db.js");

//Car object constructor
var Car = function(car) {
  this.personID = car.personID;
  this.carPlate = car.carPlate;
  this.carColor = car.carColor;
  this.carName = car.carName;
  this.currentParkingLot = car.currentParkingLot;
  this.previousParkingLots = car.previousParkingLots;
};

/* Create User Car */
Car.createCar = function(new_car, apiKey, result) {
  sql.query("Select * from user where ApiKey = ? ", apiKey, function(err, res) {
    if (err) {
    } else {
      var personID = res[0].PersonID;
      new_car.personID = personID;
      sql.query("INSERT INTO car set ?", new_car, function(err, res) {
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

/* Update User Car */
Car.updateCar = function(apiKey, updatedCar, result) {
  sql.query("Select * from user where ApiKey = ? ", apiKey, function(err, res) {
    if (err) {
    } else {
      var personID = res[0].PersonID;
      var carPlate = updatedCar.carPlate;
      sql.query(
        "UPDATE car SET ? WHERE PersonID = ? and CarPlate = ?",
        [updatedCar, personID, carPlate],
        function(err, res) {
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
};

/* Get All Cars */
Car.getAllCars = function(result) {
  sql.query("Select * from car", function(err, res) {
    if (err) {
      console.log("error: ", err);
      result(null, err);
    } else {
      console.log("cars : ", res);
      result(null, res);
    }
  });
};

/* Get User Car */
Car.getUserCar = function(apiKey, result) {
  var query = "SELECT * FROM user JOIN car ON user.PersonID = car.PersonID";
  var personID = "";
  sql.query(query, function(err, resFirst) {
    if (err) throw err;
    resFirst.forEach(function(obj) {
      if (obj.ApiKey === apiKey) {
        personID = obj.PersonID;
        sql.query("Select * from car where PersonID = ? ", personID, function(
          err,
          res
        ) {
          if (err) {
            result(err, null);
          } else {
            console.log(res[0]);
            result(null, res[0]);
            return;
          }
        });
      }
    });
  });
};

/* Get All Unmarked Cars */
Car.getAllMarkedCars = function(result) {
  sql.query(
    "Select * from car where CurrentParkingLot IS NOT NULL and CurrentParkingLot != ? ",
    "",
    function(err, res) {
      if (err) {
        console.log("error: ", err);
        result(null, err);
      } else {
        console.log("cars : ", res);
        result(null, res);
      }
    }
  );
};

/* Get All Unmarked Cars */
Car.getAllUnmarkedCars = function(result) {
  sql.query(
    "Select * from car where CurrentParkingLot IS NULL or CurrentParkingLot = ? ",
    "",
    function(err, res) {
      if (err) {
        console.log("error: ", err);
        result(null, err);
      } else {
        console.log("cars : ", res);
        result(null, res);
      }
    }
  );
};

/* Get All Cars by Color */
Car.getCarsByColor = function(carColor, result) {
  sql.query("Select * from car where CarColor  = ? ", carColor, function(
    err,
    res
  ) {
    if (err) {
      console.log("error: ", err);
      result(null, err);
    } else {
      console.log("Cars which is " + carColor + " : ", res);
      result(null, res);
    }
  });
};

module.exports = Car;
