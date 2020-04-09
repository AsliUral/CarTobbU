module.exports = function (app) {
  var userController = require("../controllers/userController");
  var carController = require("../controllers/carController");

  /* Change my password */
  app
    .route("/user/changeMyPassword/:apiKey")
    .post(userController.change_my_password);

  /* Create a user */
  app.route("/user/register").post(userController.create_a_user);

  /* Login */
  app.route("/user/login").post(userController.login_user);

  /* Google Sign In */
  app.route("/user/googleSignIn/:Email").post(userController.signin_google);

  /* Update user settings */
  app.route("/user/updateUser/:apiKey").put(userController.update_user);

  /* Activate user */
  app.route("/activate/:Email").get(userController.activate_user);

  /* Get User */
  app.route("/user/:apiKey").get(userController.get_user);

  /* Get User */
  app
    .route("/user/forgotMyPassword/:email")
    .get(userController.forgot_my_password);

  /* Change my password with form */
  app
    .route("/user/changeMyPasswordWithForm/:apiKey")
    .post(userController.change_my_password_with_form);

  /* Get User Car */
  app.route("/user/cars/:apiKey").get(carController.get_user_car);
};
