module.exports = function (app) {
    var markingController = require("../controllers/markingController");
    app
        .route("/marking/handleMarking/:apiKey")
        .post(markingController.handle_marking);
}