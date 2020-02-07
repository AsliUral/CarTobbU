"use strict";
var User = require("../model/userModel.js");

/* Register */
exports.create_a_user = function(req, res) {
  var new_user = new User(req.body);

  //handles null error
  if (!new_user.username) {
    res.status(400).send({ error: true, message: "Please provide user" });
  } else {
    User.createUser(new_user, function(err, new_user) {
      if (err) res.send(err);
      res.json(new_user);
    });
  }
};

/* Login */
exports.login_user = function(req, res) {
  var user = new User(req.body);
  //handles null error
  if (!user.username) {
    res.status(400).send({ error: true, message: "Please provide user" });
  } else {
    User.loginUser(user, function(err, user) {
      if (err) res.send(err);
      res.json(user);
    });
  }
};

/* Update User */
exports.update_user = function(req, res) {
  User.updateUser(req.params.apiKey, req.body, function(err, user) {
    if (err) res.send(err);
    res.json(user);
  });
};

/* Get user */
exports.get_user = function(req, res) {
  var apiKey = req.params.apiKey;
  User.getUser(apiKey, function(err, car) {
    if (err) res.send(err);
    res.json(car);
  });
};
