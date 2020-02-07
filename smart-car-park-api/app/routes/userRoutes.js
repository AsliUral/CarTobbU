module.exports = function (app) {
    var userController = require("../controllers/userController");
    app
        .route("/user/register")
        .post(userController.create_a_user);

    app
        .route("/user/login")
        .post(userController.login_user);

    app
        .route("/user/updateUser/:apiKey")
        .put(userController.update_user);
}