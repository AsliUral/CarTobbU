module.exports = function (app) {
    var carController = require("../controllers/carController");
    app
        .route("/cars/createCar/:apiKey")
        .post(carController.create_a_new_car);
    app
        .route("/cars/updateCar/:apiKey")
        .put(carController.update_a_car);
};
