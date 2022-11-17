
function startDateStr(){
  var d = new Date();
  return d.getFullYear() + '-' + (d.getMonth() + 1) + "-" + + d.getDate();
}
function endDateStr(){
  var now = new Date();
  var d = new Date(now.getTime() + 3600 * 1000 * 24 * 30);
  return d.getFullYear() + '-' + (d.getMonth() + 1) + "-" + + d.getDate();
}