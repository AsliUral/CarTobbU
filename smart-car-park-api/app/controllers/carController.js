"use strict";
var Car = require("../model/carModel.js");

/* Create user car */
exports.create_a_new_car = function(req, res) {
  var new_car = new Car(req.body);
  var apiKey = req.params.apiKey;
  if (!apiKey) {
    res
      .status(400)
      .send({ error: true, message: "Please provide a name of car" });
  } else {
    Car.createCar(new_car, apiKey, function(err, car) {
      if (err) res.send(err);
      res.json(car);
    });
  }
};

/* Update user car */
exports.update_a_car = function(req, res) {
  Car.updateCar(req.params.apiKey, req.body, function(err, car) {
    if (err) res.send(err);
    res.json(car);
  });
};

/* Get All Cars */
exports.get_all_cars = function(req, res) {
  Car.getAllCars(function(err, car) {
    console.log("controller");
    if (err) res.send(err);
    console.log("res", car);
    res.send(car);
  });
};

/* Get user car */
exports.get_user_car = function(req, res) {
  Car.getUserCar(req.params.apiKey, function(err, car) {
    if (err) res.send(err);
    res.json(car);
  });
};

/* Get All Cars */
exports.get_all_marked_cars = function(req, res) {
  Car.getAllMarkedCars(function(err, car) {
    console.log("controller");
    if (err) res.send(err);
    console.log("res", car);
    res.send(car);
  });
};

/* Get All Cars */
exports.get_all_unmarked_cars = function(req, res) {
  Car.getAllUnmarkedCars(function(err, car) {
    console.log("controller");
    if (err) res.send(err);
    console.log("res", car);
    res.send(car);
  });
};

/* Get All Cars */
exports.get_cars_by_color = function(req, res) {
  var carColor = req.params.carColor;
  Car.getCarsByColor(carColor, function(err, car) {
    console.log("controller");
    if (err) res.send(err);
    console.log("res", car);
    res.send(car);
  });
};
