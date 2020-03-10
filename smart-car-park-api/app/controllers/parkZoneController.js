"use strict";
var Parkzone = require("../model/parkZoneModel.js");

exports.create_a_new_parkZone = function(req, res) {
  var new_parkZone = new Parkzone(req.body);
  if (!new_parkZone.parkzonename) {
    res
      .status(400)
      .send({ error: true, message: "Please provide a name of park zone" });
  } else {
    Parkzone.createParkZone(new_parkZone, function(err, parkzone) {
      if (err) res.send(err);
      res.json(parkzone);
    });
  }
};

exports.update_a_parkZone = function(req, res) {
  console.log(req);
  Parkzone.updateParkZone(
    req.body.ParkingZoneID,
    req.body.ParkZoneName,
    function(err, parkzone) {
      if (err) res.send(err);
      res.json(parkzone);
    }
  );
};

/* Get All Parking Lots */
exports.get_all_parkzones = function(req, res) {
  Parkzone.getAllParkZones(function(err, parkinglot) {
    console.log("controller");
    if (err) res.send(err);
    console.log("res", parkinglot);
    res.send(parkinglot);
  });
};
