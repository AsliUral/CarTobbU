module.exports = function(app) {
  var carController = require("../controllers/carController");
  /* Create a Car */
  app.route("/cars/createCar/:apiKey").post(carController.create_a_new_car);

  /* Update a Car */
  app.route("/cars/updateCar/:apiKey").put(carController.update_a_car);

  /* Get All Cars */
  app.route("/cars").get(carController.get_all_cars);

  /* Get Cars By Color */
  app.route("/cars/:carColor").get(carController.get_cars_by_color);

  /* Get All Marked Cars */
  app.route("/markedCars").get(carController.get_all_marked_cars);

  /* Get All Unmarked Cars */
  app.route("/unmarkedCars").get(carController.get_all_unmarked_cars);
};
