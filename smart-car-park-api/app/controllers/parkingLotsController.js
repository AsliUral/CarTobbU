"use strict";
var ParkingLot = require("../model/parkingLotsModel");

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

exports.create_a_parkinglot = function (req, res) {
  var new_parkinglot = new ParkingLot(req.body);
  //handles null error
  if (!new_parkinglot.ParkingLotStatus) {
    res
      .status(400)
      .send({ error: true, message: "Please provide status of park place" });
  } else {
    ParkingLot.createParkingLot(new_parkplace, function (err, parkinglot) {
      if (err) res.send(err);
      res.json(parkinglot);
    });
  }
};

exports.update_a_parkinglot = function (req, res) {
  ParkingLot.updateById(
    req.params.parkingLotID,
    new ParkingLot(req.body),
    function (err, parkinglot) {
      if (err) res.send(err);
      res.json(parkinglot);
    }
  );
};

exports.delete_a_parkinglot = function (req, res) {
  ParkingLot.remove(req.params.parkingLotID, function (err, parkinglot) {
    if (err) res.send(err);
    res.json({ message: "Parking lot successfully deleted" });
  });
};
