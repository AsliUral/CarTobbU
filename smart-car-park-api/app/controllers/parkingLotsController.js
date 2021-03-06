"use strict";
var ParkingLot = require("../model/parkingLotsModel");

/* Handle Parking Event */
exports.handle_parking = function (req, res) {
  ParkingLot.updateToOccuiped(
    req.params.parkingLotID,
    new ParkingLot(req.body),
    function (err, parkinglot) {
      if (err) res.send(err);
      res.json(parkinglot);
    }
  );
};

/* Handle Leaving Event */
exports.handle_leaving = function (req, res) {
  ParkingLot.updateToAvailable(
    req.params.parkingLotID,
    new ParkingLot(req.body),
    function (err, parkinglot) {
      if (err) res.send(err);
      res.json(parkinglot);
    }
  );
};

/* Handle Select Event */
exports.handle_select = function (req, res) {
  ParkingLot.updateToSelected(
    req.params.parkingLotID,
    new ParkingLot(req.body),
    function (err, parkinglot) {
      if (err) res.send(err);
      res.json(parkinglot);
    }
  );
};

/* Handle UnSelect Event */
exports.handle_unselect = function (req, res) {
  ParkingLot.updateToUnSelected(
    req.params.parkingLotID,
    new ParkingLot(req.body),
    function (err, parkinglot) {
      if (err) res.send(err);
      res.json(parkinglot);
    }
  );
};

/* Handle Set Api Key Event */
exports.set_api_key = function (req, res) {
  console.log("Debug : ", req.body);
  var apiKey = req.body.ApiKey;
  ParkingLot.updateApiKey(apiKey, req.params.parkingLotID, function (
    err,
    parkinglot
  ) {
    if (err) res.send(err);
    res.json(parkinglot);
  });
};

/* Handle Set Select Time Event */
exports.set_select_time = function (req, res) {
  console.log("Debug : ", req.body.SelectTime);
  var selectTime = req.body.SelectTime;
  ParkingLot.updateSelectTime(selectTime, req.params.parkingLotID, function (
    err,
    parkinglot
  ) {
    if (err) res.send(err);
    res.json(parkinglot);
  });
};

/* Create a Parking Lot */
exports.create_a_parkinglot = function (req, res) {
  var new_parkinglot = new ParkingLot(req.body);
  //handles null error
  if (!new_parkinglot.ParkingLotStatus) {
    res
      .status(400)
      .send({ error: true, message: "Please provide status of park place" });
  } else {
    ParkingLot.createParkingLot(new_parkinglot, function (err, parkinglot) {
      if (err != null && err.errno == 1062) {
        console.log("Duplicate entry", new_parkinglot);

        ParkingLot.updateById(
          new_parkinglot.ParkingLotID,
          new_parkinglot,
          function (err, parkinglot) {
            //if (err) res.send(err);
            //res.json(parkinglot);
          }
        );
        res.status(400).send({
          error: true,
          message: "Parking lot updated.",
        });
      } else {
        res.json(parkinglot);
      }
    });
  }
};

/* Update A Parking Lot */
exports.update_a_parkinglot = function (req, res) {
  var new_parkinglot = new ParkingLot(req.body);

  ParkingLot.updateById(req.params.parkingLotID, new_parkinglot, function (
    err,
    parkinglot
  ) {
    if (err) res.send(err);
    res.json(parkinglot);
  });
};

/* Delete A Parking Lot */
exports.delete_a_parkinglot = function (req, res) {
  ParkingLot.remove(req.params.parkingLotID, function (err, parkinglot) {
    if (err) res.send(err);
    res.json({ message: "Parking lot successfully deleted" });
  });
};

/* Get All Parking Lots */
exports.get_all_parking_lots = function (req, res) {
  ParkingLot.getAllParkingLots(function (err, parkinglot) {
    console.log("controller");
    if (err) res.send(err);
    console.log("res", parkinglot);
    res.send(parkinglot);
  });
};

/* Get Parking Lot by Parking Lot ID */
exports.get_parking_lot_by_id = function (req, res) {
  ParkingLot.getParkingLotById(req.params.parkingLotID, function (
    err,
    parkinglot
  ) {
    if (err) res.send(err);
    res.json(parkinglot);
  });
};

/* Update Parking Lot by Parking Lot ID */
exports.update_parking_lot_by_id = function (req, res) {
  ParkingLot.updateParkingLotById(req.params.parkingLotID, function (
    err,
    parkinglot
  ) {
    if (err) res.send(err);
    res.json(parkinglot);
  });
};

/* Delete Parking Lot by Parking Lot ID */
exports.delete_parking_lot_by_id = function (req, res) {
  ParkingLot.deleteParkingLotById(req.params.parkingLotID, function (
    err,
    parkinglot
  ) {
    if (err) res.send(err);
    res.json(parkinglot);
  });
};

/* Get All Occupied Parking Lots */
exports.get_all_occupied_parking_lots = function (req, res) {
  ParkingLot.getAllOccupiedParkingLots(function (err, parkinglot) {
    console.log("controller");
    if (err) res.send(err);
    console.log("res", parkinglot);
    res.send(parkinglot);
  });
};

/* Get All Available Parking Lots */
exports.get_all_available_parking_lots = function (req, res) {
  ParkingLot.getAllAvailableParkingLots(function (err, parkinglot) {
    console.log("controller");
    if (err) res.send(err);
    console.log("res", parkinglot);
    res.send(parkinglot);
  });
};

/* Get All Out of Service Parking Lots */
exports.get_all_out_of_service_parking_lots = function (req, res) {
  ParkingLot.getAllOutOfServiceParkingLots(function (err, parkinglot) {
    console.log("controller");
    if (err) res.send(err);
    console.log("res", parkinglot);
    res.send(parkinglot);
  });
};

/* Get All Parking Lots of Parking Zone */
exports.get_all_parking_lots_of_parking_zone = function (req, res) {
  var parkZoneID = req.params.parkZoneID;
  ParkingLot.getAllParkingLotsOfParkZone(parkZoneID, function (
    err,
    parkinglot
  ) {
    console.log("controller");
    if (err) res.send(err);
    console.log("res", parkinglot);
    res.send(parkinglot);
  });
};

/* Get Occupied Parking Lots of Parking Zone */
exports.get_occiped_parking_lots_of_parking_zone = function (req, res) {
  var parkZoneID = req.params.parkZoneID;
  ParkingLot.getOccupiedParkingLotsOfParkZone(parkZoneID, function (
    err,
    parkinglot
  ) {
    console.log("controller");
    if (err) res.send(err);
    console.log("res", parkinglot);
    res.send(parkinglot);
  });
};

/* Get Available Parking Lots of Parking Zone */
exports.get_available_parking_lots_of_parking_zone = function (req, res) {
  var parkZoneID = req.params.parkZoneID;
  ParkingLot.getAvailableParkingLotsOfParkZone(parkZoneID, function (
    err,
    parkinglot
  ) {
    console.log("controller");
    if (err) res.send(err);
    console.log("res", parkinglot);
    res.send(parkinglot);
  });
};

/* Get Out Of Service Parking Lots of Parking Zone */
exports.get_out_of_service_parking_lots_of_parking_zone = function (req, res) {
  var parkZoneID = req.params.parkZoneID;
  ParkingLot.getOutOfServiceParkingLotsOfParkZone(parkZoneID, function (
    err,
    parkinglot
  ) {
    console.log("controller");
    if (err) res.send(err);
    console.log("res", parkinglot);
    res.send(parkinglot);
  });
};
