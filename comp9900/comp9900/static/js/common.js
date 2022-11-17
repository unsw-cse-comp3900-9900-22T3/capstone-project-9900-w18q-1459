function info(text){
  alert(text);
}
function warn(text){
  alert(text);
}
function error(text){
  alert(text);
}

function checkState(end_date){
  var now = new Date();
  console.log("now ", now.getFullYear(), now.getMonth() + 1, now.getDate());
  var strs = end_date.split('-');
  console.log("end_date", strs[0], strs[1], strs[2]);
  if(now.getFullYear() != Number(strs[0])){
    return now.getFullYear() > Number(strs[0]) ? 'Closed' : 'Open';
  }else if(now.getMonth() + 1 != Number(strs[1])){
    return now.getMonth() + 1 > Number(strs[1]) ? 'Closed' : 'Open';
  }else if(now.getDate() != Number(strs[2])){
    return now.getDate() > Number(strs[2]) ? 'Closed' : 'Open';
  }else{
    return 'Open';
  }
}