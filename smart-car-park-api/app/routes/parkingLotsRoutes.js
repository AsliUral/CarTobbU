module.exports = function (app) {
    var parkingLotsController = require("../controllers/parkingLotsController");
    app
        .route("/handleParking/:parkingLotID")
        .put(parkingLotsController.handle_parking);
    app
        .route("/handleLeaving/:parkingLotID")
        .put(parkingLotsController.handle_leaving);
}