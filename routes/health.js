const Promise = require('bluebird');
const express = require('express');
const router = express.Router();


function checkDatabase() {
  return Promise.resolve();
}

function checkDisk() {
  return Promise.resolve();
}

function healthCheck() {
  const checks = [checkDatabase, checkDisk]
  return Promise.reduce(checks, (result, check) => {
    return check().then((checkResult) => {
      result[check.name] = {
        failed: false,
        result: checkResult
      }
      return result;
    }, (error) => {
      result[check.name] = {
        failed: false,
        result: error.message
      }
      result.isSuccessful = false
      return result;
    })
  }, { isSuccessful: true} )
}

/* GET home page. */
router.get('/', function(req, res, next) {
  console.log('test');
  healthCheck().then((result) => {
    const status = result.isSuccessful === false ? 500 : 200;
    res.status(status).send(result);
  }, (err) => {
    res.status(500).send( { isSuccessful: false, error: err.message});
  })
  
});

module.exports = router;
