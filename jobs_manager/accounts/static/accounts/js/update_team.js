function getIDs(val) {
    for(let i = 0; i < document.getElementsByTagName('input').length; i++) {
       if(document.getElementsByTagName('input')[i].value == val) {
          return document.getElementsByTagName('input')[i].id;
       }
    }
}


function check(val) {
    document.getElementById(val).checked = true;
}


function checkBoxes(members){
    for (let i = 0; i < members.length; i++) {
        let id = getIDs(members[i]);
        check(id);
    }
}