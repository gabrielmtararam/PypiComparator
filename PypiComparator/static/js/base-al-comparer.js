let ALSocket = null;
let spansALLen = 0;
let spansALErrorsLen = 0;

$(document).ready(function () {
    $("#start-processs-al-list").click(function () {
        startProcessALWebSocket()
    });

    $("#stop-processs-al-list").click(function () {
        stopProcessAL()
    });

    $("#start-comparing-al-list").click(function () {
        startCompareALWebSocket()
    });

    $("#stop-comparing-al-list").click(function () {
        stopCompareAL()
    });


    $("#start-comparing-similar-al-list").click(function () {
        startCompareSimilarALWebSocket()
    });

    $("#stop-comparing-similar-al-list").click(function () {
        stopCompareSimilarAL()
    });

});


function startCompareSimilarALWebSocket() {
    spansALErrorsLen = 0;
    spansALLen = 0;
    $("#compare-similar-al-list-messages>.messages-content").html("")
    let url = `ws://${window.location.host}/ws/compare-similar-al-urls/`
    if (ALSocket) {
        ALSocket.close()
        stopProcessAL()
    }
    ALSocket = new WebSocket(url)

    ALSocket.onmessage = function (e) {
        let data = JSON.parse(e.data)

        if (data['message'] === 'started_socket_sucessefuly') {
            ALSocket.send(JSON.stringify({
                'message': "start_processing_al"
            }))
        }
        let new_span_message = $('<span />').addClass(`message-${data['type']}`).html(data['message']);
        if (data['type'] === 'error') {
            spansALErrorsLen += 1;
        }
        $("#compare-similar-al-list-messages>.messages-content").append(new_span_message)
        spansALLen += 1;
        $("#comparing-al-list-span-len").html(`Awsome Python List URLs equivalents with FlaPy URLs: ${spansALLen}`)
        $("#comparing-al-list-error-len").html(`Awsome Python List URLs NOT equivalents with FlaPy URLs ${spansALErrorsLen}`)

    }

}

function stopCompareSimilarAL() {
    ALSocket.send(JSON.stringify({
        'message': "stop_processing_al"
    }))
}



function startCompareALWebSocket() {
    spansALErrorsLen = 0;
    spansALLen = 0;
    $("#compare-al-list-messages>.messages-content").html("")
    let url = `ws://${window.location.host}/ws/compare-al-urls/`
    if (ALSocket) {
        ALSocket.close()
        stopProcessAL()
    }
    ALSocket = new WebSocket(url)

    ALSocket.onmessage = function (e) {
        let data = JSON.parse(e.data)

        if (data['message'] === 'started_socket_sucessefuly') {
            ALSocket.send(JSON.stringify({
                'message': "start_processing_al"
            }))
        }
        let new_span_message = $('<span />').addClass(`message-${data['type']}`).html(data['message']);
        if (data['type'] === 'error') {
            spansALErrorsLen += 1;
        }
        $("#compare-al-list-messages>.messages-content").append(new_span_message)
        spansALLen += 1;
        $("#comparing-al-list-span-len").html(`Awsome Python List URLs equivalents with FlaPy URLs: ${spansALLen}`)
        $("#comparing-al-list-error-len").html(`Awsome Python List URLs NOT equivalents with FlaPy URLs ${spansALErrorsLen}`)

    }

}

function stopCompareAL() {
    ALSocket.send(JSON.stringify({
        'message': "stop_processing_al"
    }))
}



function startProcessALWebSocket() {
    spansALErrorsLen = 0;
    spansALLen = 0;
    $("#processs-al-list-messages>.messages-content").html("")
    let url = `ws://${window.location.host}/ws/process-al-urls/`
    if (ALSocket) {
        ALSocket.close()
        stopProcessAL()
    }
    ALSocket = new WebSocket(url)

    ALSocket.onmessage = function (e) {
        let data = JSON.parse(e.data)


        if (data['message'] === 'started_socket_sucessefuly') {
            ALSocket.send(JSON.stringify({
                'message': "start_processing_al"
            }))
        }
        let new_span_message = $('<span />').addClass(`message-${data['type']}`).html(data['message']);
        if (data['type'] === 'error') {
            spansALErrorsLen += 1;
        }
        $("#process-al-list-messages>.messages-content").append(new_span_message)
        spansALLen += 1;
        $("#processs-al-list-span-len").html(`Processed urls: ${spansALLen}`)

    }

}

function stopProcessAL() {
    ALSocket.send(JSON.stringify({
        'message': "stop_processing_al"
    }))
}

