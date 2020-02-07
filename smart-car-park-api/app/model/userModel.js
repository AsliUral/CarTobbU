"user strict";
var sql = require("./dbModel/db.js");
const uuidAPIKey = require("uuid-apikey");
var crypto = require("crypto");
var passwordHash;
var nsalt;

//User object constructor
var User = function(user) {
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
};

var genRandomString = function(length) {
  return crypto
    .randomBytes(Math.ceil(length / 2))
    .toString("hex")
    .slice(0, length);
};

var sha512 = function(password, salt) {
  var hash = crypto.createHmac("sha512", salt); /** Hashing algorithm sha512 */
  hash.update(password);
  var value = hash.digest("hex");
  return {
    salt: salt,
    passwordHash: value
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

User.createUser = function(user, result) {
  user.apiKey = uuidAPIKey.create().apiKey;
  var { nsalt, passwordHash } = saltHashPassword(user.password);
  user.salt = nsalt;
  user.hash = passwordHash;
  delete user["password"];

  sql.query("INSERT INTO user set ?", user, function(err, res) {
    if (err) {
      console.log("error: ", err);
      result(null, err);
    } else {
      console.log(res.insertId);
      result(null, res.insertId);
    }
  });
};

User.updateUser = function(apiKey, updatedUser, result) {
  sql.query(
    "UPDATE user SET ? WHERE ApiKey = ?",
    [updatedUser, apiKey],
    function(err, res) {
      if (err) {
        console.log("error: ", err);
        result(null, err);
      } else {
        result(null, res);
      }
    }
  );
};
User.loginUser = function(user, result) {
  sql.query("Select * from user where Username = ? ", user.username, function(
    err,
    res
  ) {
    if (err) {
      console.log("error: ", err);
    } else {
      for (var key in res) {
        if (res.hasOwnProperty(key)) {
          var { salt, passwordHash } = verify(user.password, res[key].Salt);
          if (passwordHash === res[key].Hash) {
            delete res[key]["password"];
            delete res[key]["Salt"];
            delete res[key]["Hash"];
            delete res[key]["PersonID"];
            result(null, res[key]);
            break;
          } else {
            var loginFailed = {
              responseCode: 401,
              message: "You're not authorized to use (/user/login) ",
              content: [],
              duration: "18ms"
            };
            result(null, loginFailed);
          }
        }
      }
    }
  });
};

/* Get User */
User.getUser = function(apiKey, result) {
  sql.query("Select * from user where ApiKey = ? ", apiKey, function(err, res) {
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

module.exports = User;
