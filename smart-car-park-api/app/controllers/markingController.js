"use strict";

var Marking = require("../model/markingModel.js");

exports.handle_marking = function (req, res) {
    Marking.handleMarkingEvent(req.params.apiKey, req.body.ParkingLotID, function (err, marking) {
        if (err) res.send(err);
        res.json(marking);
    });
};
