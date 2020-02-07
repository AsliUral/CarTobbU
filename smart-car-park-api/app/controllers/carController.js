"use strict";
var Car = require("../model/carModel.js");

exports.create_a_new_car = function (req, res) {
  var new_car = new Car(req.body);
  var apiKey = req.params.apiKey;
  if (!apiKey) {
    res
      .status(400)
      .send({ error: true, message: "Please provide a name of car" });
  } else {
    Car.createCar(new_car, apiKey, function (err, car) {
      if (err) res.send(err);
      res.json(car);
    });
  }
};
exports.update_a_car = function (req, res) {
  Car.updateCar(
    req.params.apiKey,
    req.body,
    function (err, car) {
      if (err) res.send(err);
      res.json(car);
    }
  );
};