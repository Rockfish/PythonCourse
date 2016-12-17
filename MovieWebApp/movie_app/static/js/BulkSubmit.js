
var needsSaving = false;

window.onbeforeunload = function () {
    try {
        if (needsSaving) {
            return "There are unsaved changes. If you leave the page without saving, the changes will be lost.";
        }
    }
    catch (e) { /* ignore errors */ }
};

function onAdd() {
    var requestId = $("#requestId").val();
    var type = $("#newIdentifierType").val();
    var values = $("#newIdentifiers").val();
    var billable = $("#newBillable").attr('checked');
    var delim = $("#newDelim").val();

    var request = $.ajax({
        type: "POST",
        url: "../Identifiers",
        data: {
            action: "add",
            requestId: requestId,
            type: type,
            billable: billable,
            delim: delim,
            values: values
        },
        failure: function () {
            alert("Error");
        },
        cache: false
    });

    request.done(function (data) {
        $("#identifiersTable").html(data);
    });
}

function onErase(row) {
    var requestId = $("#requestId").val();
    $.ajax({
        type: "POST",
        url: "../Identifiers",
        data: {
            action: "erase",
            requestId: requestId,
            row: row
        },
        success: function (data) {
            $("#identifiersTable").html(data);
        },
        failure: function () {
            alert("Error");
        },
        cache: false
    });
}

function onPageLoad() {
    $.ajax({
        type: "POST",
        url: "../Identifiers",
        data: {
            action: "refresh"
        },
        success: function (data) {
            $("#identifiersTable").html(data);
        },
        failure: function () {
            alert("Error");
        },
        cache: false
    });
}

function onClear() {
    var requestId = $("#requestId").val();
    $.ajax({
        type: "POST",
        url: "../Identifiers",
        data: {
            action: "clear",
            requestId: requestId
        },
        success: function (data) {
            $("#identifiersTable").html(data);
        },
        failure: function () {
            alert("Error");
        },
        cache: false
    });
}

function onSubmit() {
    var requestId = $("#requestId").val();

    var request = $.ajax({
        type: "POST",
        url: "../Identifiers",
        data: {
            action: "submit",
            requestId: requestId
        },
        failure: function () {
            alert("Error");
        },
        cache: false
    });

    request.done(function (data) {
        $("#identifiersTable").html(data);
    });
}

function onClose() {
    var requestId = $("#requestId").val();

    var request = $.ajax({
        type: "POST",
        url: "../CloseRequest",
        data: {
            action: "close",
            requestId: requestId
        },
        failure: function () {
            alert("Error");
        },
        cache: false
    });

    request.done(function (data) {
        window.location.href = "../Start";
    });
}

function onCancel() {
    //Todo: Confirm first
    onClose();
}

function onPreview(requestId) {
    window.open("../Preview/" + requestId);
}

onPageLoad();
