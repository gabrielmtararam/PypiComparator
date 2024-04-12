let chatSocket = null;
let urlChatSocket = null;
let spansLen = 0;
let spansTotalLen = 0;
let spansErrorsLen = 0;
let spansErrorList = []

let spansUrlsLen = 0;
let spansUrlsErrorsLen = 0;
let spansUrlsErrorList = []

$(document).ready(function () {
    $("#process-pypi-index-file").click(function () {
        let url = $("#process-pypi-index-file").data("url")
        startProcessSimpleIndexWebSocket()
    });
    $("#send-message").click(function () {
        sendMessage()
    });

    $("#stop-simple-index-processing").click(function () {
        stopSimpleIndexProcessing()
    });


    $("#process-pypi-urls").click(function () {
        let url = $("#process-pypi-index-file").data("url")
        startProcessPypiUrlsWebSocket()
    });
    $("#stop-process-pypi-urls").click(function () {
        stopProcessPypiUrls()
    });

});


function startProcessPypiUrlsWebSocket() {
    console.log("startProcessPypiUrlsWebSocket")
    spansUrlsErrorsLen = 0;
    spansUrlsLen = 0;
    spansTotalLen = 0;
    $("#process-pypi-urls-messages>.content").html("")
    let url = `ws://${window.location.host}/ws/process-urls/`
    // if (chatSocket) {
    //     chatSocket.close()
    //     stopSimpleIndexProcessing()
    // }
    urlChatSocket = new WebSocket(url)
    console.log("WebSocket urlChatSocket ",url)
    urlChatSocket.onmessage = function (e) {
        let data = JSON.parse(e.data)
        if (data['message'] === 'started_socket_sucessefuly') {
            urlChatSocket.send(JSON.stringify({
                'message': "start_processing_simple_index_url"
            }))
        }
        let new_span_message = $('<span />').addClass(`message-${data['type']}`).html(data['message']);
        if (data['type'] === 'error') {
            spansErrorsLen += 1;
        }
        $("#process-pypi-urls-messages>.content").append(new_span_message)
        spansUrlsLen += 1;
        spansTotalLen += 1;
        if (spansUrlsLen>400){
            spansUrlsLen = 0;
             $("#process-pypi-urls-messages>.content").html("")
        }

        $("#process-pypi-urls-span-len").html(`Qtd links processados ${spansTotalLen}`)
        $("#process-pypi-urls-span-error-len").html(`Qtd links processados com erro ${spansErrorsLen}`)

    }


}

function stopProcessPypiUrls() {
    console.log("stop processing")
    urlChatSocket.send(JSON.stringify({
        'message': "stop_processing_simple_index_url"
    }))
}


function sendMessage() {
    console.log("send message")
    chatSocket.send(JSON.stringify({
        'message': "teste"
    }))
}

function stopSimpleIndexProcessing() {
    console.log("stop processing")
    chatSocket.send(JSON.stringify({
        'message': "stop_processing_simple_index"
    }))
}

function startProcessSimpleIndexWebSocket() {
    spansErrorsLen = 0;
    spansLen = 0;
    spansTotalLen = 0;
    $("#simple-index-processing-messages>.content").html("")
    let url = `ws://${window.location.host}/ws/socket-server/`
    if (chatSocket) {
        chatSocket.close()
        stopSimpleIndexProcessing()
    }
    chatSocket = new WebSocket(url)

    chatSocket.onmessage = function (e) {
        let data = JSON.parse(e.data)

        if (data['message'] === 'started_socket_sucessefuly') {
            chatSocket.send(JSON.stringify({
                'message': "start_processing_simple_index"
            }))
        }
        if (data['type'] === 'error') {
            spansErrorsLen += 1;
            spansTotalLen += 1;
            let new_span_message = $('<span />').addClass(`message-${data['type']}`).html(data['message']);

            spansErrorList.push(new_span_message)
            $("#simple-index-processing-messages>.content").append(new_span_message)
            if (spansErrorsLen > 100) {
                for (var i = 100; i < spansErrorList.length; i++) {
                    $("#simple-index-processing-messages>.content").removeChild(spansErrorList.shift());
                }
            }
        }
        spansLen += 1;
        $("#span-len").html(`Qtd links processados ${spansLen}`)
        $("#span-error-len").html(`Qtd links processados com erro ${spansErrorsLen}`)

    }


}