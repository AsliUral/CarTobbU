module.exports = function(app) {
  var userController = require("../controllers/userController");
  var carController = require("../controllers/carController");

  /* Create a user */
  app.route("/user/register").post(userController.create_a_user);

  /* Login */
  app.route("/user/login").post(userController.login_user);

  /* Update user settings */
  app.route("/user/updateUser/:apiKey").put(userController.update_user);

  /* Get User */
  app.route("/user/:apiKey").get(userController.get_user);

  /* Get User Car */
  app.route("/user/cars/:apiKey").get(carController.get_user_car);
};
