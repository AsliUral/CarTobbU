path = require("path");
var db = require("../model/dbModel/db.js");

const { Storage } = require("@google-cloud/storage");
const { format } = require("util");
const Multer = require("multer");

const storage = new Storage({
  keyFilename: path.join(
    __dirname,
    "../../smart-car-park-api-068196ef90ee.json"
  ),
});

const multer = Multer({
  storage: Multer.memoryStorage(),
  limits: {
    fileSize: 5 * 1024 * 1024, // no larger than 5mb, you can change as needed.
  },
});

const bucket = storage.bucket("penalty-report-images");

module.exports = function (app) {
  var penaltyController = require("../controllers/penaltyController");
  app
    .route("/penalty", multer.single("penaltyImage"))
    .post(penaltyController.create_penalty);

  app.route("/getPenalties").get(penaltyController.get_penalties);
};
