"user strict";
var sql = require("./dbModel/db.js");
const uuidAPIKey = require("uuid-apikey");
var crypto = require("crypto");
var passwordHash;
var nsalt;

//User object constructor
var User = function (user) {
  this.username = user.username;
  this.apiKey = user.apiKey;
  this.hash = user.hash;
  this.salt = user.salt;
  this.password = user.password;
  this.personFullName = user.personFullName;
  this.userType = user.userType;
  this.studentID = user.studentID;
  this.allowedCarParks = user.allowedCarParks;
  this.personIsDisabled = user.personIsDisabled;
  this.LoginCounter = user.LoginCounter;
  this.Email = user.Email;
  this.PhoneNumber = user.PhoneNumber;
};

var genRandomString = function (length) {
  return crypto
    .randomBytes(Math.ceil(length / 2))
    .toString("hex")
    .slice(0, length);
};

var sha512 = function (password, salt) {
  var hash = crypto.createHmac("sha512", salt); /** Hashing algorithm sha512 */
  hash.update(password);
  var value = hash.digest("hex");
  return {
    salt: salt,
    passwordHash: value,
  };
};

function saltHashPassword(userpassword) {
  var salt = genRandomString(16); /** Gives us salt of length 16 */
  var passwordData = sha512(userpassword, salt);
  passwordHash = passwordData.passwordHash;
  nsalt = passwordData.salt;
  return { nsalt, passwordHash };
}

function verify(userpassword, nsalt) {
  var passwordData = sha512(userpassword, nsalt);
  var passwordHash = passwordData.passwordHash;
  nsalt = passwordData.salt;
  return { nsalt, passwordHash };
}

User.createUser = function (user, result) {
  user.apiKey = uuidAPIKey.create().apiKey;
  var { nsalt, passwordHash } = saltHashPassword(user.password);
  user.salt = nsalt;
  user.hash = passwordHash;
  user.LoginCounter = 0;
  delete user["password"];

  sql.query("INSERT INTO user set ?", user, function (err, res) {
    if (err) {
      console.log("error: ", err);
      result(null, err);
    } else {
      console.log(res.insertId);
      result(null, res.insertId);
    }
  });
};

User.changePassword = function (newPassword, userApiKey, result) {
  newUser = null;
  sql.query("Select * from user where ApiKey = ? ", userApiKey, function (
    err,
    res
  ) {
    if (err) {
      console.log("error: ", err);
      result(null, err);
    } else {
      newUser = res[0];
      var sqlDelete =
        "DELETE FROM user WHERE ApiKey =" + "'" + userApiKey + "'";
      sql.query(sqlDelete, function (err, result) {
        if (err) throw err;
        console.log("Silindi");
      });

      newUser.password = newPassword;
      newUser.LoginCounter = 0;
      delete newUser["ApiKey"];
      delete newUser["Salt"];
      delete newUser["Hash"];

      newUser.apiKey = uuidAPIKey.create().apiKey;
      var { nsalt, passwordHash } = saltHashPassword(newUser.password);
      newUser.salt = nsalt;
      newUser.hash = passwordHash;
      newUser.LoginCounter = 0;
      delete newUser["password"];

      sql.query("INSERT INTO user set ?", newUser, function (err, res) {
        if (err) {
          console.log("error: ", err);
          result(null, err);
        } else {
          console.log(res.insertId);
          result(null, res.insertId);
        }
      });
    }
  });
};

User.updateUser = function (apiKey, updatedUser, result) {
  sql.query(
    "UPDATE user SET ? WHERE ApiKey = ?",
    [updatedUser, apiKey],
    function (err, res) {
      if (err) {
        console.log("error: ", err);
        result(null, err);
      } else {
        result(null, res);
      }
    }
  );
};
User.loginUser = function (user, result) {
  sql.query("Select * from user where Username = ? ", user.username, function (
    err,
    res
  ) {
    if (err) {
      console.log("error: ", err);
    } else {
      console.log("Debug : " + res.length);
      if (res.length == 1) {
        for (var key in res) {
          if (res.hasOwnProperty(key)) {
            var { salt, passwordHash } = verify(user.password, res[key].Salt);
            if (passwordHash === res[key].Hash) {
              person = res[0];
              sql.query(
                "UPDATE user SET LoginCounter = ? WHERE ApiKey = ?",
                ["0", person.ApiKey],
                function (err, res) {
                  if (err) {
                    console.log("error: ", err);
                    //result(null, err);
                  } else {
                    //result(null, res);
                  }
                }
              );

              delete res[key]["password"];
              delete res[key]["Salt"];
              delete res[key]["Hash"];
              delete res[key]["PersonID"];
              res[key]["LoginCounter"] = "0";
              result(null, res[key]);
              break;
            } else {
              person = res[0];
              currentLoginCounter = parseInt(person.LoginCounter, 10);
              if (currentLoginCounter < 3) {
                currentLoginCounter = currentLoginCounter + 1;
                newLogCounter = currentLoginCounter.toString();
                sql.query(
                  "UPDATE user SET LoginCounter = ? WHERE ApiKey = ?",
                  [newLogCounter, person.ApiKey],
                  function (err, res) {
                    if (err) {
                      console.log("error: ", err);
                      //result(null, err);
                    } else {
                      //result(null, res);
                    }
                  }
                );
              } else {
                person = res[0];
                var nodemailer = require("nodemailer");

                var transporter = nodemailer.createTransport({
                  service: "gmail",
                  auth: {
                    user: "samaritancartobbu@gmail.com",
                    pass: "Samaritan123456",
                  },
                });

                var mailOptions = {
                  from: "samaritancartobbu@gmail.com",
                  to: person.Email,
                  subject: "Login failed 3 times!",
                  text: "Warning warning!",
                };

                transporter.sendMail(mailOptions, function (error, info) {
                  if (error) {
                    console.log(error);
                  } else {
                    console.log("Email sent: " + info.response);
                  }
                });
              }
              var loginFailed = {
                responseCode: 401,
                message: "You're not authorized to use (/user/login) ",
                content: [],
                duration: "18ms",
              };
              result(null, loginFailed);
            }
          }
        }
      } else {
        var loginFailed = {
          responseCode: 401,
          message: "You're not authorized to use (/user/login) ",
          content: [],
          duration: "18ms",
        };
        result(null, loginFailed);
      }
    }
  });
};

/* Get User */
User.getUser = function (apiKey, result) {
  sql.query("Select * from user where ApiKey = ? ", apiKey, function (
    err,
    res
  ) {
    if (err) {
      console.log("error: ", err);
      result(null, err);
    } else {
      var user = res[0];
      console.log("user : ", user);
      result(null, user);
    }
  });
};

/* Get User */
User.forgotMyPassword = function (email, result) {
  sql.query("Select * from user where Email = ? ", email, function (err, res) {
    if (err) {
      console.log("error: ", err);
      result(null, err);
    } else {
      var user = res[0];
      console.log("user : ", user);

      var nodemailer = require("nodemailer");

      var transporter = nodemailer.createTransport({
        service: "gmail",
        auth: {
          user: "samaritancartobbu@gmail.com",
          pass: "Samaritan123456",
        },
      });

      var mailOptions = {
        from: "samaritancartobbu@gmail.com",
        to: user.Email,
        subject: "Change your password!",
        text: "You can change your password with this link below : ",
        html:
          `<form
                action="https://smart-car-park-api.appspot.com/user/changeMyPasswordWithForm/` +
          user.ApiKey +
          `"
                method="POST"
                enctype="application/x-www-form-urlencoded"
              >
              <label>
                New Password:
                <input type="text" name="newPassword">
              </label>
              <button type="submit">Send</button>
              </form>`,
      };

      transporter.sendMail(mailOptions, function (error, info) {
        if (error) {
          console.log(error);
        } else {
          console.log("Email sent: " + info.response);
        }
      });

      result(null, user);
    }
  });
};

module.exports = User;
