$(document).ready(function () {
    $("#submit_action").click(function () {
        const strategy = $('#strategy').val();
        const payload = {
            ticker: $('#stock_code').val(),
            start_date: $('#start_date').val(),
            end_date: $('#end_date').val(),
            cash: parseFloat($('#initial_cash').val()),
        };

        if (strategy === 'rsi') {
            payload.rsi_period = parseInt($('#rsi_period').val());
            payload.overbought = parseInt($('#overbought').val());
            payload.oversold = parseInt($('#oversold').val());
        } else if (strategy === 'sma') {
            payload.fast_period = parseInt($('#fast_period').val());
            payload.slow_period = parseInt($('#slow_period').val());
        }

        $.ajax({
            type: "POST",
            url: "http://127.0.0.1:8001/api/strategies/backtrader/run/",
            contentType: "application/json",
            data: JSON.stringify(payload),
            success: function (response) {
                if (response.plot_image && response.initial_cash && response.final_cash) {
                    $('#results').show();
                    $('#result-data').html(`
                        <p><strong>Initial Cash:</strong> $${response.initial_cash.toFixed(2)}</p>
                        <p><strong>Final Cash:</strong> $${response.final_cash.toFixed(2)}</p>
                    `);
                    $('#result-image').html(`
                        <img src="data:image/png;base64,${response.plot_image}" class="img-fluid" alt="Backtest Result">
                    `);
                } else {
                    alert("Invalid response received from the server.");
                }
            },
            error: function (xhr, status, error) {
                console.error("Error:", error);
                alert("An error occurred: " + xhr.responseText);
            },
        });
    });
});
