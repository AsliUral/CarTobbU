"use strict";

var Marking = require("../model/markingModel.js");

exports.handle_marking = function(req, res) {
  Marking.handleMarkingEvent(req.params.apiKey, req.body.ParkingLotID, function(
    err,
    marking
  ) {
    if (err) res.send(err);
    res.json(marking);
  });
};

/* Get All Markings */
exports.get_all_markings = function(req, res) {
  Marking.getAllMarkings(function(err, marking) {
    console.log("controller");
    if (err) res.send(err);
    console.log("Markings : ", marking);
    res.send(marking);
  });
};
