function navigateByHash() {
    const hash = window.location.hash;
    hash && $('ul.nav.nav-tabs a[href="' + hash + '"]').tab('show');
    $('ul.nav.nav-tabs a').click(function (e) {
        $(this).tab('show');
        $('body').scrollTop();
        window.location.hash = this.hash;
    });
}

$(window).on('hashchange', navigateByHash);
$(window).on('load', navigateByHash);

$(document).ready(function() {
    $(".result-delete-button").click(function () {
        const resultID = $(this).attr("data-resultid");

        $.ajax({
            method: "POST",
            url: "/questioning/results/delete/" + resultID,
            data: {
                taskID: resultID,
            },
            success: function (response) {
                console.log("Result deleted!");
                $(".result-block[data-resultid=" + resultID + "]").remove();
                if (!$(".result-card").length) {
                    $("#empty-history-message").removeClass("d-none");
                }
            },
            error: function (response) {
                console.log(response.statusText);
            }
        });
        return false;
    });

    $("#profile-update-form").change(function () {
        $("#profile-update-submit-btn")
            .removeClass("disabled")
            .removeClass("btn-secondary")
            .addClass("btn-primary");
    })
});
