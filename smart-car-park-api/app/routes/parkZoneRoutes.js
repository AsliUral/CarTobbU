"use strict";
module.exports = function (app) {
    var parkZoneController = require("../controllers/parkZoneController");
    app
        .route("/parkZone")
        .get(parkZoneController.list_all_parkzones)
        .post(parkZoneController.create_a_new_parkZone)
        .put(parkZoneController.update_a_parkZone)
}