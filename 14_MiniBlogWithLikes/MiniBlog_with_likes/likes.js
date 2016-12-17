// Ajax call
// Posts data object to the server.
// When the server replies it runs the success function
// which updates the likes for the message.
function increment_likes(message_id) {
    $.ajax({
        type: "POST",
        url: "/like",
        data: {
            id: message_id
        },
        success: function (likesNumber) {
        	// Update the likes
        	like_id = "#likes_" + message_id
            $(like_id).html(likesNumber)
        },
        failure: function () {
            alert("Error");
        },
        cache: false
    });
}

// Called by the onclick event attached to the Like button.
function like_click(buttonid){

	// parse the button id to get the id number
    var index = buttonid.lastIndexOf("_");
    message_id = buttonid.substring(index + 1);

    // Call the Ajax message to increment the likes.
    increment_likes(message_id);
}
