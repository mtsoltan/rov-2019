function startSocket(outputHandler) {
    let socket = new WebSocket("ws://localhost:8123");

    socket.onmessage = function (event) {
        mapString(event.data, outputHandler);
    };

    return socket;
}
