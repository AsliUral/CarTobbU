"use strict";
module.exports = function(app) {
  var parkZoneController = require("../controllers/parkZoneController");
  var parkingLotsController = require("../controllers/parkingLotsController");

  app
    .route("/parkZone")
    .get(parkZoneController.get_all_parkzones)
    .post(parkZoneController.create_a_new_parkZone)
    .put(parkZoneController.update_a_parkZone);

  app
    .route("/parkZone/:parkZoneID/parkingLots")
    .get(parkingLotsController.get_all_parking_lots_of_parking_zone);

  app
    .route("/parkZone/:parkZoneID/occupiedParkingLots")
    .get(parkingLotsController.get_occiped_parking_lots_of_parking_zone);

  app
    .route("/parkZone/:parkZoneID/availableParkingLots")
    .get(parkingLotsController.get_available_parking_lots_of_parking_zone);

  app
    .route("/parkZone/:parkZoneID/outOfServiceParkingLots")
    .get(parkingLotsController.get_out_of_service_parking_lots_of_parking_zone);
};
