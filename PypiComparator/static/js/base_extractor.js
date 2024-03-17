$(document).ready(function () {
    $("#process-pypi-index-file").click(function () {
        let url = $("#process-pypi-index-file").data("url")
        console.log("url ",url)
        let csrftoken = $("[name=csrfmiddlewaretoken]").val();

        $.ajax({
            url: url,
            processData: false,
            contentType: false,
            type: 'GET',
            data: {},
            beforeSend: function (xhr, settings) {
                // Insert CSRFToken in request
                xhr.setRequestHeader("X-CSRFToken", csrftoken);
            },
            success: function (data) {
                // // Add success text and color and show the alert message
                // $("#alert-message").removeClass("alert-danger").addClass("alert-success");
                // $("#alert-message p").text(successMessage);
                // $("#alert-message").show();
                // $("#alert-message").delay(5000).fadeOut('slow');
                //
                // // Hide the modal
                // $("#modal-import").modal("hide");
            },
            error: function (e) {
                // if (e?.responseJSON?.redirect) {
                //     window.location.replace(e.responseJSON.location + window.location.pathname);
                // }
                // else {
                //     // Add error text and color and show the alert message
                //     $("#alert-message").removeClass("alert-success").addClass("alert-danger");
                //     if (e.readyState == 0) {
                //         $("#alert-message p").text(gettext("CLEM4"));
                //     }
                //     else {
                //         $("#alert-message p").html(e.responseJSON);
                //     }
                //     $("#alert-message").show();
                //     $("#alert-message").delay(DEFAULT_DELAY).fadeOut('slow');
                //
                //     // Hide the modal
                //     $("#modal-import").modal("hide");
                // }
            }
        })
    });

});