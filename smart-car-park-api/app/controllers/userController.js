"use strict";
var User = require("../model/userModel.js");

/* Register */
exports.create_a_user = function (req, res) {
  var new_user = new User(req.body);
  new_user.Activated = "False";
  new_user.LoginCounter = 0;
  //handles null error
  if (!new_user.username) {
    res.status(400).send({ error: true, message: "Please provide user" });
  } else {
    User.createUser(new_user, function (err, new_user) {
      if (err) res.send(err);
      res.json(new_user);
    });
  }
};

/* Change my Password */
exports.change_my_password = function (req, res) {
  var newPassword = req.body.newPassword;
  var userApiKey = req.params.apiKey;
  //handles null error
  if (!newPassword) {
    res.status(400).send({ error: true, message: "Please provide user" });
  } else {
    User.changePassword(newPassword, userApiKey, function (err, new_user) {
      if (err) res.send(err);
      res.json(new_user);
    });
  }
};

/* Change my Password */
exports.change_my_password_with_form = function (req, res) {
  var newPassword = req.body.newPassword;
  var userApiKey = req.params.apiKey;

  //handles null error
  if (!newPassword) {
    res.status(400).send({ error: true, message: "Please provide user" });
  } else {
    User.changePassword(newPassword, userApiKey, function (err, new_user) {
      if (err) res.send(err);
      res.json(new_user);
    });
  }
};

/* Login */
exports.login_user = function (req, res) {
  var user = new User(req.body);
  //handles null error
  if (!user.username) {
    res.status(400).send({ error: true, message: "Please provide user" });
  } else {
    User.loginUser(user, function (err, user) {
      if (err) res.send(err);
      res.json(user);
    });
  }
};

/* Login */
exports.signin_google = function (req, res) {
  var user = new User(req.params.Email);
  var email = req.params.Email;
  var username = email.substring(0, email.indexOf("@"));
  user.username = username;
  user.personFullName = username;

  /* User type and studen ID will be added */
  user.userType = "Student";
  user.studentID = "11111111111";
  user.PhoneNumber = "05339345587";

  user.allowedCarParks = "Academic Only Car Park";
  user.personIsDisabled = "No";
  user.LoginCounter = "0";
  user.Activated = "True";
  user.Email = email;

  //handles null error
  if (!user.username) {
    res.status(400).send({ error: true, message: "Please provide user" });
  } else {
    User.googleSignIn(user, function (err, user) {
      if (err) res.send(err);
      res.json(user);
    });
  }
};

/* Update User */
exports.update_user = function (req, res) {
  User.updateUser(req.params.apiKey, req.body, function (err, user) {
    if (err) res.send(err);
    res.json(user);
  });
};

/* Activate User */
exports.activate_user = function (req, res) {
  User.activateUser(req.params.Email, function (err, user) {
    if (err) res.send(err);
    res.json(user);
  });
};

/* Get user */
exports.get_user = function (req, res) {
  var apiKey = req.params.apiKey;
  User.getUser(apiKey, function (err, car) {
    if (err) res.send(err);
    res.json(car);
  });
};

/* Forgot my password */
exports.forgot_my_password = function (req, res) {
  var email = req.params.email;
  User.forgotMyPassword(email, function (err, user) {
    if (err) res.send(err);
    res.json(user);
  });
};
