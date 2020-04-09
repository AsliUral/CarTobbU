"user strict";
var sql = require("./dbModel/db.js");

//Parkzone object constructor
var Parkzone = function (parkzone) {
  this.ParkingZoneID = parkzone.ParkingZoneID;
  this.parkzonename = parkzone.parkzonename;
  this.CameraIP = parkzone.CameraIP;
};

/* Create a Parking Zone */
Parkzone.createParkZone = function (parkingZone, result) {
  console.log("Parkzone debug : " + parkingZone.CameraIP);
  sql.query("INSERT INTO parkzone set ?", parkingZone, function (err, res) {
    if (err) {
      console.log("error: ", err);
      result(null, err);
    } else {
      console.log(res.insertId);
      result(null, res.insertId);
    }
  });
};

/* Update a Parking Zone */
Parkzone.updateParkZone = function (
  ParkZoneID,
  ParkZoneName,
  cameraIP,
  result
) {
  console.log(
    "Debug update parkzone : " +
      ParkZoneID +
      " " +
      ParkZoneName +
      " " +
      cameraIP
  );
  sql.query(
    "UPDATE parkzone SET ParkZoneName = ?, CameraIP = ? WHERE ParkingZoneID = ?",
    [ParkZoneName, cameraIP, ParkZoneID],
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

/* Get All Parking Zones */
Parkzone.getAllParkZones = function (result) {
  sql.query("Select * from parkzone", function (err, res) {
    if (err) {
      console.log("error: ", err);
      result(null, err);
    } else {
      console.log("parking zones : ", res);

      result(null, res);
    }
  });
};

module.exports = Parkzone;
