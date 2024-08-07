let ALFlapySocket = null;
let spansALFlapyLen = 0;
let spansALFlapyErrorsLen = 0;

$(document).ready(function () {

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


    $("#get-repositories-commit-hash-code").click(function () {
        getRepositoriesCommitHashCode()
    });

    $("#stop-comparing-similar-al-list").click(function () {
        stopCompareSimilarAL()
    });

});

function downloadALFlapyCSV() {
    let url = $("#download-al-flapy-csv").data("url");
    $.ajax({
        url: url,  // Substitua pela URL da sua view Django
        type: 'GET',
    });
}
function checkAlFlapyProcessByLog() {
    let url = $("#check-al-flapy-process-by-log").data("url");
    $.ajax({
        url: url,  // Substitua pela URL da sua view Django
        type: 'GET',
    });
}


function checkAlFlapyProcessByLog400() {
    let url = $("#check-al-flapy-process-by-log-400").data("url");
    $.ajax({
        url: url,  // Substitua pela URL da sua view Django
        type: 'GET',
    });
}

function generateCSVAlFlapyProcessByLog400() {
    let url = $("#generate-csv-al-flapy-process-by-log-400").data("url");
    $.ajax({
        url: url,  // Substitua pela URL da sua view Django
        type: 'GET',
    });
}


function getRepositoriesCommitHashCode() {
    let url = $("#get-repositories-commit-hash-code").data("url");
    $.ajax({
        url: url,  // Substitua pela URL da sua view Django
        type: 'GET',
    });
}

function checkAlFlapyProcess() {
    spansALFlapyErrorsLen = 0;
    spansALFlapyLen = 0;
    $("#compare-similar-al-list-messages>.messages-content").html("")
    let url = `ws://${window.location.host}/ws/check-al-flapy-process/`
    if (ALFlapySocket) {
        ALFlapySocket.close()
        stopProcessAL()
    }
    ALFlapySocket = new WebSocket(url)

    ALFlapySocket.onmessage = function (e) {
        let data = JSON.parse(e.data)

        if (data['message'] === 'started_socket_sucessefuly') {
            ALFlapySocket.send(JSON.stringify({
                'message': "start_processing_al"
            }))
        }
        let new_span_message = $('<span />').addClass(`message-${data['type']}`).html(data['message']);
        if (data['type'] === 'error') {
            spansALFlapyErrorsLen += 1;
        }
        $("#compare-similar-al-list-messages>.messages-content").append(new_span_message)
        spansALFlapyLen += 1;
        $("#comparing-al-list-span-len").html(`Awsome Python List URLs equivalents with FlaPy URLs: ${spansALFlapyLen}`)
        $("#comparing-al-list-error-len").html(`Awsome Python List URLs NOT equivalents with FlaPy URLs ${spansALFlapyErrorsLen}`)

    }
}

function stopCompareSimilarAL() {
    ALFlapySocket.send(JSON.stringify({
        'message': "stop_processing_al"
    }))
}


