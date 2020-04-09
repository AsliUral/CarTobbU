"user strict";
var sql = require("./dbModel/db.js");

//Marking object constructor
var Marking = function (marking) {
  this.personID = marking.personID;
  this.carPlate = marking.carPlate;
  this.parkingLotID = car.parkingLotID;
  this.ParkingTime = car.ParkingTime;
};

Marking.handleMarkingEvent = function (apiKey, parkingLotID, result) {
  CarPlate = "";
  ParkingLotID = parkingLotID;
  sql.query("Select * from user where ApiKey = ? ", apiKey, function (
    err,
    res
  ) {
    if (err) {
      console.log("error: ", err);
      result(err, null);
    } else {
      var personID = res[0].PersonID;
      sql.query("Select * from car where ApiKey = ? ", apiKey, function (
        err,
        res1
      ) {
        if (err) {
          console.log("error: ", err);
        } else {
          CarPlate = res1[0].CarPlate;
          ParkingLotID = parkingLotID;
          newMarking = {
            PersonID: personID,
            CarPlate: res1[0].CarPlate,
            ParkingLotID: parkingLotID,
            ApiKey: apiKey,
          };
          sql.query("INSERT INTO marking set ?", newMarking, function (
            err,
            res
          ) {
            if (err) {
              console.log("error: ", err);
              result(err, null);
            } else {
              var sqlUpdate =
                "UPDATE car SET CurrentParkingLot = " +
                "'" +
                ParkingLotID +
                "'" +
                " WHERE CarPlate = " +
                "'" +
                CarPlate +
                "'";
              sql.query(sqlUpdate, function (err, result) {
                if (err) throw err;
                console.log(result.affectedRows + " record(s) updated");
              });

              console.log(res.insertId);
              result(null, res.insertId);
            }
          });
        }
      });
    }
  });
};

Marking.handleDeleteEvent = function (apiKey, parkingLotID, result) {
  CarPlate = "";
  ParkingLotID = parkingLotID;
  sql.query("Select * from user where ApiKey = ? ", apiKey, function (
    err,
    res
  ) {
    if (err) {
      console.log("error: ", err);
      result(err, null);
    } else {
      var personID = res[0].PersonID;
      sql.query("Select * from car where ApiKey = ? ", apiKey, function (
        err,
        res1
      ) {
        if (err) {
          console.log("error: ", err);
        } else {
          CarPlate = res1[0].CarPlate;
          ParkingLotID = parkingLotID;
          var sqlDelete =
            "DELETE FROM marking WHERE ApiKey =" + "'" + apiKey + "'";
          sql.query(sqlDelete, function (err, result) {
            if (err) throw err;
            console.log("Number of records deleted: " + result.affectedRows);
          });
          sql.query(
            "UPDATE car SET CurrentParkingLot = ? WHERE CurrentParkingLot = ?",
            ["", ParkingLotID]
          );
          result(null, "Demarking successfull");
        }
      });
    }
  });
};

/* Get All Markings */
Marking.getAllMarkings = function (result) {
  sql.query("Select * from marking", function (err, res) {
    if (err) {
      console.log("error: ", err);
      result(null, err);
    } else {
      console.log("markings : ", res);
      result(null, res);
    }
  });
};

module.exports = Marking;
