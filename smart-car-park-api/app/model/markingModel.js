"user strict";
var sql = require("./dbModel/db.js");

//Marking object constructor
var Marking = function (marking) {
    this.personID = marking.personID;
    this.carPlate = marking.carPlate;
    this.parkingLotID = car.parkingLotID;
    this.ParkingTime = car.ParkingTime;
};

Marking.handleMarkingEvent = function (apiKey, parkingLotID, result) {
    sql.query(
        "Select * from user where ApiKey = ? ",
        apiKey,
        function (err, res) {
            if (err) {
                console.log("error: ", err);
                result(err, null);
            } else {
                var personID = res[0].PersonID;
                sql.query(
                    "Select * from car where PersonID = ? ",
                    personID,
                    function (err, res1) {
                        if (err) {
                            console.log("error: ", err);
                        } else {
                            newMarking = {
                                "PersonID": personID,
                                "CarPlate": res1[0].CarPlate,
                                "ParkingLotID": parkingLotID
                            }
                            sql.query("INSERT INTO marking set ?", newMarking, function (err, res) {
                                if (err) {
                                    console.log("error: ", err);
                                    result(err, null);
                                } else {
                                    console.log(res2.insertId);
                                    result(null, res2.insertId);
                                }
                            });
                        }
                    }
                );
            }
        }
    );
};

module.exports = Marking;
