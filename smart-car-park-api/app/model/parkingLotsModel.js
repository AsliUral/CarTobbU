"user strict";
var sql = require("./dbModel/db.js");

//ParkingLot object constructor
var ParkingLot = function (parkingLot) {
  this.status = parkingLot.status;
  this.parkingLotID = parkingLot.parkingLotID;
  this.carParkName = parkingLot.carParkName;
};

ParkingLot.createParkingLot = function (newParkingLot, result) {
  sql.query("INSERT INTO parkinglots set ?", newParkingLot, function (err, res) {
    if (err) {
      console.log("error: ", err);
      result(err, null);
    } else {
      console.log(res.insertId);
      result(null, res.insertId);
    }
  });
};

ParkingLot.updateToOccuiped = function (parkingLotID, parkingLot, result) {
  sql.query(
    "UPDATE parkinglots SET ParkingLotStatus = ? WHERE ParkingLotID = ?",
    ["Occupied", parkingLotID],
    function (err, res) {
      if (err) {
        console.log("error: ", err);
        result(null, err);
      } else {
        result(null, res);
      }
    }
  );
};

ParkingLot.updateToAvailable = function (parkingLotID, parkingLot, result) {
  sql.query(
    "UPDATE parkinglots SET ParkingLotStatus = ? WHERE ParkingLotID = ?",
    ["Available", parkingLotID],
    function (err, res) {
      if (err) {
        console.log("error: ", err);
        result(null, err);
      } else {
        sql.query(
          "DELETE FROM marking WHERE ParkingLotID = ?",
          [parkingLotID]
        );
        sql.query(
          "UPDATE car SET CurrentParkingLot = ? WHERE CurrentParkingLot = ?",
          ["", parkingLotID]
        );
        result(null, res);
      }
    }
  );
};

module.exports = ParkingLot;
