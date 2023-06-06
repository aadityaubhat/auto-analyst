function addToChat(sender, message, isQuery = false) {
    let messageItem = $('<div>');
    messageItem.addClass('message');
    messageItem.addClass(sender.toLowerCase());

    let senderElement = $('<strong>').text(sender);
    let senderLine = $('<div>').append(senderElement);

    let messageContent;

    if (isQuery) {
        messageContent = $('<pre>').append($('<code>').addClass('sql').text(message));
        hljs.highlightBlock(messageContent[0]);
    } else {
        messageContent = typeof message === 'string' ? $('<div>').text(message) : message;
    } 

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
            if (result.analysis_type === "data") {
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
                    // sortname: colNames[0],  // use the first column name as the sortname
                    viewrecords: true,
                    sortorder: "desc",
                    caption:"Analysis Results"
                });

                // Add gridContainer as a new message to the chat
                addToChat('AutoAnalyst', gridContainer);
            }
            else if (result.analysis_type === "plot") {
                let plotContainer = $('<div>');
                let plotElement = $('<div id="plotDiv"></div>');
                plotContainer.append(plotElement);

                // Add plotContainer as a new message to the chat
                addToChat('AutoAnalyst', plotContainer);
                console.log(result.result_plot);
                setTimeout(function() {
                    let plotData = JSON.parse(result.result_plot);
                    Plotly.newPlot(plotElement[0], plotData.data, plotData.layout);
                }, 0);
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