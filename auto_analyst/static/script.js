function addToChat(sender, message) {
    let messageItem = $('<div>');
    messageItem.addClass('message');
    messageItem.addClass(sender.toLowerCase());

    let senderElement = $('<strong>').text(sender);
    let senderLine = $('<div>').append(senderElement);

    let messageContent = typeof message === 'string' ? $('<div>').text(message) : message;

    messageItem.append(senderLine);
    messageItem.append(messageContent);

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
        success: function(response) {
            let result = response;
            console.log(result);
            loadingMessage.remove(); // Remove loading animation
            
            // Get column names dynamically from result_data
            let colNames = Object.keys(result.result_data[0]);
            
            // Create colModel dynamically
            let colModel = colNames.map(function(name) {
                return {
                    name: name,
                    index: name,
                    width: 100
                };
            });
        
            // Create new div element to host the jqGrid
            let gridContainer = $('<div>');
            let gridElement = $('<table id="myGrid"></table>');
            let pagerElement = $('<div id="pager"></div>');
            gridContainer.append(gridElement);
            gridContainer.append(pagerElement);
        
            gridElement.jqGrid({
                datatype: "local",
                data: result.result_data,
                colNames: colNames,
                colModel: colModel,
                rowNum:10,
                rowList:[10,20,30],
                pager: pagerElement,
                sortname: colNames[0],  // use the first column name as the sortname
                viewrecords: true,
                sortorder: "desc",
                caption:"Analysis Results"
            });
        
            // Add gridContainer as a new message to the chat
            addToChat('AutoAnalyst', gridContainer);
        
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