//Note, no jQuery, dont really need it
function formValueRegex(match, name) {
    if (document.forms[0][name]) {
        return document.forms[0][name].value;
    } else {
        console.log('NOT FOUND ' + name);
        return '';
    }
}

function mysubmit() {
    var values = {}
    var regex = /\<var ([a-zA-Z0-9]*)>/g;
    if (postBackValues.Msg) values.Msg = postBackValues.Msg.replace(regex, formValueRegex);
    if (postBackValues.Subject) values.Subject = postBackValues.Subject.replace(regex, formValueRegex);
    window.opener.postMessage(values);
    window.close()
}
window.addEventListener('DOMContentLoaded', function() {
    document.forms[0].onsubmit = mysubmit;
    //console.log(document.getElementById('Submit'))
    //document.getElementById('Submit').addEventListener('click', mysubmit);
});