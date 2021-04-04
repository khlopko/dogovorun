// static/js/application.js

// Support TLS-specific URLs, when appropriate.
if (window.location.protocol == "https:") {
  var ws_scheme = "wss://";
} else {
  var ws_scheme = "ws://"
};

var inbox = new ReconnectingWebSocket(ws_scheme + location.host + "/receive");
var outbox = new ReconnectingWebSocket(ws_scheme + location.host + "/submit");

inbox.onmessage = function(message) {
  location.reload()
};

const Http = new XMLHttpRequest();

$("a").on('click', function(event) {
  event.preventDefault();
  var url = location.protocol + "//" + location.host + $(this).attr('href');
  Http.open("GET", url);
  Http.send();
  Http.onreadystatechange = (e) => {
    outbox.send(JSON.stringify({ event: "change" }));
  }
});
