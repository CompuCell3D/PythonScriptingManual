
/**
 * Returns true if the string has a valid URL syntax. 
 * Does not check whether the page gives 200 or 404 status.
 */
function isUrlValid(string) {
    try {
        new URL(string);
        return true;
    } catch (err) {
        return false;
    }
}

var path = window.location.pathname;
var page = path.split("/").pop();

BASE_URL = "https://compucell3dreferencemanual.readthedocs.io/en/latest/"; //assume latest
var newUrl = BASE_URL + "/" + page;

if (isUrlValid(newUrl)) {
    window.location.href = newUrl;
}
else {
    alert("The PythonScriptingManual is deprecated. Please visit us at " + BASE_URL);
}
