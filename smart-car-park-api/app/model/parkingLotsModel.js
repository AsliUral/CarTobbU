"user strict";
var sql = require("./dbModel/db.js");

//ParkingLot object constructor
var ParkingLot = function (parkingLot) {
  this.ParkingLotStatus = parkingLot.status;
  this.ParkingLotID = parkingLot.parkingLotID;
  this.ParkZoneName = parkingLot.parkZoneName;
  this.FirstPoint = parkingLot.firstPoint;
  this.SecondPoint = parkingLot.secondPoint;
  this.ThirdPoint = parkingLot.thirdPoint;
  this.FourthPoint = parkingLot.fourthPoint;
};

/* Create a Parking Lot */
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

/* Update to Occupied */
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

/* Update to Available */
ParkingLot.updateToAvailable = function (parkingLotID, parkingLot, result) {
  sql.query(
    "UPDATE parkinglots SET ParkingLotStatus = ? WHERE ParkingLotID = ?",
    ["Available", parkingLotID],
    function (err, res) {
      if (err) {
        console.log("error: ", err);
        result(null, err);
      } else {
        sql.query("DELETE FROM marking WHERE ParkingLotID = ?", [parkingLotID]);
        sql.query(
          "UPDATE car SET CurrentParkingLot = ? WHERE CurrentParkingLot = ?",
          ["", parkingLotID]
        );
        result(null, res);
      }
    }
  );
};

/* Get Parking Lot By Parking Lot ID */
ParkingLot.getParkingLotById = function (parkingLotID, result) {
  sql.query(
    "Select * from parkinglots where ParkingLotID = ? ",
    parkingLotID,
    function (err, res) {
      if (err) {
        console.log("error: ", err);
        result(err, null);
      } else {
        result(null, res);
      }
    }
  );
};

/* Get All Parking Lots */
ParkingLot.getAllParkingLots = function (result) {
  sql.query("Select * from parkinglots", function (err, res) {
    if (err) {
      console.log("error: ", err);
      result(null, err);
    } else {
      console.log("parkinglots : ", res);

      result(null, res);
    }
  });
};

/* Get All Occupied Parking Lots */
ParkingLot.getAllOccupiedParkingLots = function (result) {
  sql.query(
    "Select * from parkinglots where ParkingLotStatus = ? ",
    "Occupied",
    function (err, res) {
      if (err) {
        console.log("error: ", err);
        result(null, err);
      } else {
        console.log("parkinglots : ", res);

        result(null, res);
      }
    }
  );
};

/* Get All Occupied Parking Lots */
ParkingLot.getAllAvailableParkingLots = function (result) {
  sql.query(
    "Select * from parkinglots where ParkingLotStatus = ? ",
    "Available",
    function (err, res) {
      if (err) {
        console.log("error: ", err);
        result(null, err);
      } else {
        console.log("parkinglots : ", res);

        result(null, res);
      }
    }
  );
};

/* Get All Out of Service Parking Lots */
ParkingLot.getAllOutOfServiceParkingLots = function (result) {
  sql.query(
    "Select * from parkinglots where ParkingLotStatus = ? ",
    "OutOfService",
    function (err, res) {
      if (err) {
        console.log("error: ", err);
        result(null, err);
      } else {
        console.log("parkinglots : ", res);

        result(null, res);
      }
    }
  );
};

/* Get All Parking Lots of Park Zone */
ParkingLot.getAllParkingLotsOfParkZone = function (parkZoneID, result) {
  sql.query(
    "Select * from parkzone where ParkingZoneID = ? ",
    parkZoneID,
    function (err, res) {
      if (err) {
        result(null, err);
      } else {
        var parkZoneName = res[0].ParkZoneName;

        sql.query(
          "Select * from parkinglots where ParkZoneName = ? ",
          parkZoneName,
          function (err, res) {
            if (err) {
              console.log("error: ", err);
              result(null, err);
            } else {
              console.log("Parking Lots of " + parkZoneName + " : ", res);

              result(null, res);
            }
          }
        );
      }
    }
  );
};

/* Get Occupied Parking Lots of Park Zone */
ParkingLot.getOccupiedParkingLotsOfParkZone = function (parkZoneID, result) {
  sql.query(
    "Select * from parkzone where ParkingZoneID = ? ",
    parkZoneID,
    function (err, res) {
      if (err) {
        result(null, err);
      } else {
        var parkZoneName = res[0].ParkZoneName;

        sql.query(
          'Select * from parkinglots where ParkZoneName = ? and ParkingLotStatus = "Occupied" ',
          parkZoneName,
          function (err, res) {
            if (err) {
              console.log("error: ", err);
              result(null, err);
            } else {
              console.log(
                "Occupied Parking Lots of " + parkZoneName + " : ",
                res
              );
              result(null, res);
            }
          }
        );
      }
    }
  );
};

/* Get Available Parking Lots of Park Zone */
ParkingLot.getAvailableParkingLotsOfParkZone = function (parkZoneID, result) {
  sql.query(
    "Select * from parkzone where ParkingZoneID = ? ",
    parkZoneID,
    function (err, res) {
      if (err) {
        result(null, err);
      } else {
        var parkZoneName = res[0].ParkZoneName;

        sql.query(
          'Select * from parkinglots where ParkZoneName = ? and ParkingLotStatus = "Available" ',
          parkZoneName,
          function (err, res) {
            if (err) {
              console.log("error: ", err);
              result(null, err);
            } else {
              console.log(
                "Available Parking Lots of " + parkZoneName + " : ",
                res
              );

              result(null, res);
            }
          }
        );
      }
    }
  );
};

/* Get Out Of Service Parking Lots of Park Zone */
ParkingLot.getOutOfServiceParkingLotsOfParkZone = function (parkZoneID, result) {
  sql.query(
    "Select * from parkzone where ParkingZoneID = ? ",
    parkZoneID,
    function (err, res) {
      if (err) {
        result(null, err);
      } else {
        var parkZoneName = res[0].ParkZoneName;

        sql.query(
          'Select * from parkinglots where ParkZoneName = ? and ParkingLotStatus = "OutOfService" ',
          parkZoneName,
          function (err, res) {
            if (err) {
              console.log("error: ", err);
              result(null, err);
            } else {
              console.log(
                "Out Of Service Parking Lots of " + parkZoneName + " : ",
                res
              );

              result(null, res);
            }
          }
        );
      }
    }
  );
};

module.exports = ParkingLot;
