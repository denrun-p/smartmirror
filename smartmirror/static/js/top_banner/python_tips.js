// Function for timer
function callOnInterval(time, url, fn) {
    setInterval(function () {
        $.getJSON($SCRIPT_ROOT + url, fn);
        return false;
    }, time);
}

// Update date/time endpoint every 30m
callOnInterval(1800000, '/top_banner',
    function(data) {
    	$("#py_tips").text(data["tip"]);
    });