let ALFlapychatSocket = null;
let spansALFlapyLen = 0;
let spansALFlapyErrorsLen = 0;

$(document).ready(function () {
    $("#update-al-flapy-process").click(function () {
        // updateAlFlapyProcessList()
    });
    $("#download-al-flapy-list").click(function () {
        downloadALFlapyList()
    });

    $("#download-al-flapy-csv").click(function () {
        downloadALFlapyCSV()
    });

    $("#check-al-flapy-process").click(function () {
        checkAlFlapyProcess()
    });

    $("#check-al-flapy-process-by-log").click(function () {
        checkAlFlapyProcessByLog()
    });

    $("#check-al-flapy-process-by-log-400").click(function () {
        checkAlFlapyProcessByLog400()
    });


    $("#generate-csv-al-flapy-process-by-log-400").click(function () {
        generateCSVAlFlapyProcessByLog400()
    });

});

function downloadALFlapyList() {
    let url = $("#download-al-flapy-list").data("url");
    $.ajax({
        url: url,  // Substitua pela URL da sua view Django
        type: 'GET',
        success: function (response) {
            console.log("responder ",response)
            var blob = new Blob([response]);
            var link = document.createElement('a');
            link.href = window.URL.createObjectURL(blob);
            link.download = 'dados.csv';
            link.click();
        }
    });
}
function downloadALFlapyCSV() {
    let url = $("#download-al-flapy-csv").data("url");
    $.ajax({
        url: url,  // Substitua pela URL da sua view Django
        type: 'GET',
        success: function (response) {
            console.log("responder ",response)
            var blob = new Blob([response]);
            var link = document.createElement('a');
            link.href = window.URL.createObjectURL(blob);
            link.download = 'custom_flapy_teste.csv';
            link.click();
        }
    });
}
function checkAlFlapyProcessByLog() {
    let url = $("#check-al-flapy-process-by-log").data("url");
    $.ajax({
        url: url,  // Substitua pela URL da sua view Django
        type: 'GET',
        success: function (response) {
            console.log("responder ",response)
            // var blob = new Blob([response]);
            // var link = document.createElement('a');
            // link.href = window.URL.createObjectURL(blob);
            // link.download = 'custom_flapy_teste.csv';
            // link.click();
        }
    });
}


function checkAlFlapyProcessByLog400() {
    let url = $("#check-al-flapy-process-by-log-400").data("url");
    $.ajax({
        url: url,  // Substitua pela URL da sua view Django
        type: 'GET',
        success: function (response) {
            console.log("response ",response)
            // var blob = new Blob([response]);
            // var link = document.createElement('a');
            // link.href = window.URL.createObjectURL(blob);
            // link.download = 'custom_flapy_teste.csv';
            // link.click();
        }
    });
}

function generateCSVAlFlapyProcessByLog400() {
    let url = $("#generate-csv-al-flapy-process-by-log-400").data("url");
    $.ajax({
        url: url,  // Substitua pela URL da sua view Django
        type: 'GET',
        success: function (response) {
            console.log("response ",response)
            // var blob = new Blob([response]);
            // var link = document.createElement('a');
            // link.href = window.URL.createObjectURL(blob);
            // link.download = 'custom_flapy_teste.csv';
            // link.click();
        }
    });
}

function checkAlFlapyProcess() {
    console.log("start updateAlFlapyProcessList")
    spansALFlapyErrorsLen = 0;
    spansALFlapyLen = 0;
    $("#compare-similar-al-list-messages>.content").html("")
    let url = `ws://${window.location.host}/ws/check-al-flapy-process/`
    if (ALFlapychatSocket) {
        ALFlapychatSocket.close()
        stopProcessAL()
    }
    ALFlapychatSocket = new WebSocket(url)

    ALFlapychatSocket.onmessage = function (e) {
        let data = JSON.parse(e.data)

        console.log("recieved message from web socket ", data)

        if (data['message'] === 'started_socket_sucessefuly') {
            ALFlapychatSocket.send(JSON.stringify({
                'message': "start_processing_al"
            }))
        }
        let new_span_message = $('<span />').addClass(`message-${data['type']}`).html(data['message']);
        if (data['type'] === 'error') {
            spansALFlapyErrorsLen += 1;
        }
        $("#compare-similar-al-list-messages>.content").append(new_span_message)
        spansALFlapyLen += 1;
        $("#comparing-al-list-span-len").html(`Qtd links processados ${spansALFlapyLen}`)
        $("#comparing-al-list-error-len").html(`Qtd links processados com erro ${spansALFlapyErrorsLen}`)

        // }
    }
}
//
// function stopCompareSimilarAL() {
//     console.log("stop stopCompareAL")
//     ALFlapychatSocket.send(JSON.stringify({
//         'message': "stop_processing_al"
//     }))
// }


