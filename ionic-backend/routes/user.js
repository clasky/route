
/*
 * GET users listing.
 */

exports.list = function(req, res, next){
  res.send([{name: 'John Smith'}, {name: 'Tim Johnson'}]);
};