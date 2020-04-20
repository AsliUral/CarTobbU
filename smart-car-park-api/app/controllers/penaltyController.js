"use strict";
path = require("path");

var db = require("../model/dbModel/db.js");
var Penalty = require("../model/penaltyModel");

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

//var Penalty = require("../model/penaltyModel.js");

exports.create_penalty = function (req, res) {
  var post = req.body;
  var date = post.date;
  var time = post.time;
  var type = post.type;
  var carPlate = post.carPlate;
  var notes = post.notes;
  var fullname = post.fullname;
  var phoneNumber = post.phoneNumber;

  console.log("Debug upload : ", req.files);
  if (req.files == null) {
    console.log("Buraya girdi");
    var sql =
      "INSERT INTO `penalty`(`date`,`time`,`carPlate`,`notes` ,`fullname`,`phoneNumber`) VALUES ('" +
      date +
      "','" +
      time +
      "','" +
      carPlate +
      "','" +
      notes +
      "','" +
      fullname +
      "','" +
      phoneNumber +
      "')";
    var query = db.query(sql, function (err, result) {
      //result.publicUrl = publicUrl;
      console.log("Error  : ", err);
      console.log("Result : ", result);
      res.json(result);
    });
  } else {
    var file = req.files.penaltyImage;
    var img_name = file.name;
    file = req.files.penaltyImage;
    // Create a new blob in the bucket and upload the file data.
    const blob = bucket.file(file.name);
    const blobStream = blob.createWriteStream();

    blobStream.on("error", (err) => {
      next(err);
    });
    blobStream.on("finish", () => {
      // The public URL can be used to directly access the file via HTTP.
      const publicUrl = format(
        `https://storage.googleapis.com/${bucket.name}/${blob.name}`
      );

      var sql =
        "INSERT INTO `penalty`(`date`,`time`,`type`, `carPlate`,`notes` ,`image`) VALUES ('" +
        date +
        "','" +
        time +
        "','" +
        type +
        "','" +
        carPlate +
        "','" +
        notes +
        "','" +
        publicUrl +
        "')";
      var query = db.query(sql, function (err, result) {
        result.publicUrl = publicUrl;
        res.json(result);
      });

      //res.status(200).send(publicUrl);
    });

    blobStream.end(file.data);
  }
};

/* Get All Penalties */
exports.get_penalties = function (req, res) {
  var sql = "Select * from penalty";
  var query = db.query(sql, function (err, result) {
    res.json(result);
  });
};
