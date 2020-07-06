let socket = new WebSocket("wss://localhost:6868");
let request = { "id": 0, "jsonrpc": "2.0" };
let subscribedStreams = ["pow", "met"];//["met", "fac"]; // Met aprox 10', fac = 1'
let cortexToken = "";
let headset = null;
let session = null;
let isCollecting = false;
let variables = {};
let userId = 0


var xhr = new XMLHttpRequest();
var url = "http://localhost:8086/write?db=brain_readings";

function startConnection() {
    request.method = "requestAccess";
    request.params = {
        "clientId": document.getElementById("client-id").value,
        "clientSecret": document.getElementById("client-secret").value
    };

    send();
}

function startCollecting() {
    isCollecting = true;
    userId = document.getElementById("user-id").value;
}

function postData(id, variable, measures, time) {
    for (var i = 0; i < measures.length; i++) {
        xhr.open("POST", url, true);
        xhr.setRequestHeader("Content-Type", "application/x-binary");
        xhr.onreadystatechange = function () {};
        
        const stringToSend = `sensors,id=${id} ${variables[variable][i]}=${measures[i]} ${time}`;

        xhr.send(stringToSend);
    }
}

function send() {
    socket.send(JSON.stringify(request));
    request.id++;
}

function createToken() {
    request.method = "authorize";
    send();
    console.log("Creating token");
}

function authenticate() {
    request.method = "queryHeadsets";
    request.params = null;
    send();
    console.log("Searching for headsets");
}

function createSession() {
    request.method = "createSession";
    request.params = {
        "cortexToken": cortexToken,
        "headset": headset.id,
        "status": "open"
    };

    send();
    console.log("Creating session");
}

function startSubscription() {
    request.method = "subscribe";
    request.params = {
        "cortexToken": cortexToken,
        "session": session.id,
        "streams": subscribedStreams
    }

    send();
    console.log("Starting subscription");
}

socket.onopen = function (e) {
    console.log("Connection established");
    console.log("Logging-in to server");
}

socket.onmessage = function (event) {
    var response = JSON.parse(event.data);

    switch (response.id) {
        case 0: if (response.result.accessGranted) createToken(); break;

        case 1:
            if (!response.error) {
                cortexToken = response.result.cortexToken;
                authenticate();
            }
            else {
                alert("Error con las claves");
                request.id = 1;
            }
            break;

        case 2:
            if (!response.error) {
                headset = response.result[0];
                createSession();
            }
            else {
                alert("Error authenticating");
                request.id = 1;
            }
            break;

        case 3:
            if (!response.error) {
                session = response.result;
                startSubscription();
            }
            else {
                alert("Error creating session");
                request.id = 1;
            }
            break;

        case 4:
            if (!response.error && !response.failure) {
                for (var i = 0; i < response.result.success.length; i++) {
                    variables[response.result.success[i].streamName] = response.result.success[i].cols;
                }
                alert("Estoy enviando datos!")
            }
            else {
                alert("Error suscribing to data streams");
                request.id = 1;
            }

        default:    // main loop
                if (isCollecting) {
                    if ("pow" in response) {
                        postData(userId, "pow", response.pow, new Date().getTime() + "000000")
                    } else if ("met" in response) {
                        postData(userId, "met", response.met, new Date().getTime() + "000000")
                    }
                }
            break;
    }
}