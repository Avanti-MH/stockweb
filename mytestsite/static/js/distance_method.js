$.ajaxSetup({
    data: {
        csrfmiddlewaretoken : "{{ csrf_token }}",
    },
  });

function access_by_id(id){       
    //console.log(document.querySelector('#stock_1').value)
    return $(id).val()
}

function original_log(
    dates,
    stock_1,
    stock_2,
){
    var obj = {

        chart: {
            type: 'line'
        },
        title: {
            text: 'Stock Price in log'
        },
        xAxis: {
            
            type: 'category'
            
        },
        yAxis: {
            title: {
                text: 'Stock Price (USD) in log'
            }
        },
        series: [{
            name: $('#stock_1').val(),
            data: stock_1 = dates.map((date ,index) => [new Date(date).getTime(), stock_1[index]]),

            },
            {
            name: $('#stock_2').val(),
            data: stock_2 = dates.map((date ,index) => [new Date(date).getTime(), stock_2[index]]),

            }
        ]
    }
    var x = document.getElementById("container_log");
    if (x.hidden === true) {
        x.hidden = !x.hidden;
    }
    // Create the chart
    Highcharts.stockChart('container_log', obj);
}

function bollinger_band(
    dates,
    spread,
    upper_line,
    rolling_mean,
    lower_line,
    short,
    long
){
    var obj = {

        chart: {
            type: 'line'
        },
        title: {
            text: 'Stock Price'
        },
        xAxis: {
            type: 'category',
        },
        yAxis: {
            title: {
                text: 'Stock Price (USD)'
            }
        },
        series: [
            {
            name: 'spread',
            data: spread = dates.map((date ,index) => [new Date(date).getTime(), spread[index]])
            },
            {
            name: 'upper_line',
            data: upper_line = dates.map((date ,index) => [new Date(date).getTime(), upper_line[index]])
            },
            {
            name: 'rolling_mean',
            data: rolling_mean = dates.map((date ,index) => [new Date(date).getTime(), rolling_mean[index]])
            },
            {
            name: 'lower_line',
            data: lower_line = dates.map((date ,index) => [new Date(date).getTime(), lower_line[index]])
            },
            {
            type: 'scatter',
            data: short = dates.map((date ,index) => [new Date(date).getTime(), short[index]]),
            name: 'Short',
            marker: {
                name: "sell",
                symbol: 'triangle-down',
                fillColor: 'red',
                lineColor: 'red',
                lineWidth: 2,
                enabled: true,
                radius: 6,
            },
            visible: true,
            },
            {
            type: 'scatter',
            data: long = dates.map((date ,index) => [new Date(date).getTime(), long[index]]),
            name: 'Long',
            marker: {
                name: "buy",
                symbol: 'triangle',
                fillColor: 'green',
                lineColor: 'green',
                lineWidth: 2,
                enabled: true,
                radius: 6,
            },
            visible: true,
            },
        ], 
    }
    var x = document.getElementById("container_bollinger_band");
    if (x.hidden === true) {
        x.hidden = !x.hidden;
    }
    // Create the chart
    Highcharts.stockChart('container_bollinger_band', obj);
}

function profits(
    dates,
    cash,
    daily,
){
    var obj = {
        chart: {
            type: 'line'
        },
        title: {
            text: 'profits'
        },
        xAxis: {
            categories: dates
        },
        yAxis: {
            title: {
                text: 'profits'
            }
        },
        series: [{
            name: 'cash',
            data: cash = dates.map((date ,index) => [new Date(date).getTime(), cash[index]])
            },
            {
            name: 'daily_value',
            data: daily = dates.map((date ,index) => [new Date(date).getTime(), daily[index]])
            }
        ]
    }
    var x = document.getElementById("container_profits");
    if (x.hidden === true) {
        x.hidden = !x.hidden;
    }
    // Create the chart
    Highcharts.stockChart('container_profits', obj);
}
function trading_table(trade1, trade2) {
    const dataset = [];
    for (const i in trade1) {
        dataset.push([
            i,                                  // Date
            trade1[i]['status'],                // Type
            trade1[i]['op'],                    // Action of Stock 1
            trade1[i]['price'].toFixed(2),      // Stock 1 Price
            trade2[i]['op'],                    // Action of Stock 2
            trade2[i]['price'].toFixed(2),      // Stock 2 Price
        ]);
    }
    var x = document.getElementById("container_Table");
    if (x.hidden === true) {
        x.hidden = !x.hidden;
    }

    // Destroy existing DataTable instance before reinitializing
    if ($.fn.DataTable.isDataTable('#container_Table')) {
        $('#container_Table').DataTable().destroy();
    }

    $('#container_Table').DataTable({
        data: dataset,
        columns: [
            { title: "Date" },
            { title: "Type" },
            { title: "Action Stock 1" },
            { title: "Stock 1 Price" },
            { title: "Action Stock 2" },
            { title: "Stock 2 Price" },
        ],
    });
}
// click action
$(document).ready(
    function() {
        $("#click_action").click(
            function() {
                var stock_1     = $('#stock_1').val()
                var stock_2     = $('#stock_2').val()
                var start_date  = $('#start_date').val()
                var end_date    = $('#end_date').val()
                var window      = $('#window').val()
                var n_std       = $('#n_std').val()
                
                var data_config = new FormData();
                data_config.append("stock1", stock_1);
                data_config.append("stock2", stock_2);
                data_config.append("start_date", start_date);
                data_config.append("end_date", end_date);
                data_config.append("window_size", window);
                data_config.append("n_std", n_std);
                /*
                for (elem of data_config.entries()) {
                    console.log(elem[0], elem[1])
                }
                */
                $.ajax(
                    {
                        headers: { "X-CSRFToken": csrf_token  },
                        type: "POST", // what type of Request (GET or POST)
                        url: "http://127.0.0.1:8001/api/strategies/distance_method/run/",
                        dataType: "json",
                        data: data_config,
                        processData: false,
                        contentType: false,
                        success: function(xhr){
                            console.log("success")
                            console.log(xhr)
                            original_log(
                                xhr['dates'],
                                xhr['stock1'],
                                xhr['stock2']
                            )
                            //buf = document.getElementById("container_log")
                            //buf.style.display = "block"
                            bollinger_band(
                                xhr['dates'],
                                xhr['spread'],
                                xhr['upper_line'],
                                xhr['rolling_mean'],
                                xhr['lower_line'],
                                xhr['short'],
                                xhr['long']
                            )
                            profits(
                                xhr['dates'],
                                xhr['profits_cash'],
                                xhr['profits_daily'],)
                            trading_table(
                                xhr['stock1_trade'],xhr['stock2_trade']
                            )
                        },
                        error: function(xhr, status, error){
                            console.log(error)
                        },
                    }
                )
            }
        )
    }
)