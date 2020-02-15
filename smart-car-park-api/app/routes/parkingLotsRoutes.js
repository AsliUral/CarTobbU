module.exports = function (app) {
  var parkingLotsController = require("../controllers/parkingLotsController");

  /* Handle Parking Event */
  app
    .route("/handleParking/:parkingLotID")
    .put(parkingLotsController.handle_parking);

  /* Handle Leaving Event */
  app
    .route("/handleLeaving/:parkingLotID")
    .put(parkingLotsController.handle_leaving);

  /* Get All Parking Lots & Create A New Marking Lot */
  app.route("/parkingLots")
    .get(parkingLotsController.get_all_parking_lots)
    .post(parkingLotsController.create_a_parkinglot);

  /* Get A Parking Lot By Parking Lot ID */
  app
    .route("/parkingLots/:parkingLotID")
    .get(parkingLotsController.get_parking_lot_by_id);

  /* Get All Occupied Parking Lots */
  app
    .route("/occupiedParkingLots")
    .get(parkingLotsController.get_all_occupied_parking_lots);

  /* Get All Available Parking Lots */
  app
    .route("/availableParkingLots")
    .get(parkingLotsController.get_all_available_parking_lots);

  /* Get All Out of Service Parking Lots */
  app
    .route("/outOfServiceParkingLots")
    .get(parkingLotsController.get_all_out_of_service_parking_lots);
};
