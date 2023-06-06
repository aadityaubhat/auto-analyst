function addToChat(sender, message) {
    let messageItem = $('<div>');
    messageItem.addClass('message');
    messageItem.addClass(sender.toLowerCase());

    let senderElement = $('<strong>').text(sender);
    let senderLine = $('<div>').append(senderElement);

    let messageText = $('<div>').text(message);

    messageItem.append(senderLine);
    messageItem.append(messageText);

    $('#chatWindow').append(messageItem);
}

function sendMessage() {
    let message = $("#messageInput").val();
    if (message.trim() === '') return;

    addToChat('You', message); // Add message to chat before making the call
    $("#messageInput").val(''); // Clear the message input

    // Show loading animation
    let loadingMessage = $('<li class="spin">');
    loadingMessage.text('AutoAnalyst is thinking...');
    $('#chatWindow').append(loadingMessage);

    $.ajax({
        url: '/analyze',
        type: 'POST',
        data: JSON.stringify({ question: message }),
        contentType: 'application/json',
        dataType: 'json',
        headers: { "X-CSRFToken": csrf_token },
        success: function
            (response) {
            let result = response;
            console.log(result);
            loadingMessage.remove(); // Remove loading animation
            let formattedResult = `Analysis Type: ${result.analysis_type}\nMetadata: ${JSON.stringify(result.metadata, null, 2)}\nQuery: ${result.query}\nResult Data: ${JSON.stringify(result.result_data, null, 2)}\nResult Plot: ${result.result_plot}`;
            console.log(formattedResult);
            addToChat('AutoAnalyst', formattedResult);
            $('#error').hide();  // hide the error message on success
        },
        error: function (xhr, status, error) {
            loadingMessage.remove(); // Remove loading animation
            let errorMessage = null;
            if (xhr.status === 400 || xhr.status === 500) {
                let response = JSON.parse(xhr.responseText);
                errorMessage = response.error;
            } else {
                errorMessage = "An unexpected error occurred.";
            }
            $('#error').html(errorMessage);
            $('#error').show();
        }
    });
}

$('#messageForm').submit(function (e) {
    e.preventDefault();
    sendMessage();
});