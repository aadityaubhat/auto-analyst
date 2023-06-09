// Initialize clipboard for all current and future copy buttons
let clipboard = new ClipboardJS('.btn');

clipboard.on('success', function (e) {
    console.log(e);
    alert('Copied to clipboard!');
});

clipboard.on('error', function (e) {
    console.log(e);
    alert('Failed to copy.');
});

function addToChat(sender, message, isQuery = false, data = null) {
    let messageItem = $('<div>');
    messageItem.addClass('message');
    messageItem.addClass(sender.toLowerCase());

    let senderElement = $('<strong>').text(sender);
    let senderLine = $('<div>').append(senderElement);
    senderLine.addClass('d-flex justify-content-between align-items-center');

    let copyButton;
    if (sender.toLowerCase() === 'autoanalyst' && (isQuery || data)) {
        // Create the copy to clipboard button and append it to the sender line
        copyButton = $('<button>');
        copyButton.addClass('btn btn-small btn-outline-secondary ml-2');  // Add Bootstrap classes
        copyButton.html('❐');
        copyButton.attr('data-clipboard-text', isQuery ? message : JSON.stringify(data));
        senderLine.append(copyButton);
    }

    let messageContent;

    if (isQuery) {
        messageContent = $('<pre>').append($('<code>').addClass('sql').text(message));
        messageContent.addClass('query-content'); // Add the query-content class for query messages
        hljs.highlightBlock(messageContent[0]);
    } else {
        messageContent = typeof message === 'string' ? $('<div>').text(message) : message;
    }


    messageItem.append(senderLine);
    messageItem.append(messageContent);

    $('#chatWindow').append(messageItem);
    scrollToBottom();

    if (copyButton) {
        new ClipboardJS(copyButton[0]);
    }
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
        success: function (response) {
            let result = response;
            console.log(result);
            loadingMessage.remove(); // Remove loading animation
            if (result.analysis_type === "data") {
                // Get column names dynamically from result_data
                let colNames = Object.keys(result.result_data[0]);

                // Create colModel dynamically
                let colModel = colNames.map(function (name) {
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
                    rowNum: 10,
                    rowList: [10, 20, 30],
                    pager: pagerElement,
                    viewrecords: true,
                    caption: "Analysis Results"
                });

                // Add gridContainer as a new message to the chat
                addToChat('AutoAnalyst', gridContainer, false, result.result_data);
            }
            else if (result.analysis_type === "plot") {
                let plotContainer = $('<div>');
                let plotElement = $('<div id="plotDiv"></div>');
                plotContainer.append(plotElement);

                // Add plotContainer as a new message to the chat
                addToChat('AutoAnalyst', plotContainer);
                console.log(result.result_plot);

                if (result.result_plot) {  // Check if result.result_plot is defined
                    setTimeout(function () {
                        let plotData = JSON.parse(result.result_plot);
                        Plotly.newPlot(plotElement[0], plotData.data, plotData.layout);
                    }, 0);
                }
            }

            else if (result.analysis_type === "query") {
                addToChat('AutoAnalyst', result.query, true);
            }

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

function scrollToBottom() {
    let chatWindow = $('#chatWindow');
    chatWindow.scrollTop(chatWindow.prop("scrollHeight"));
}
