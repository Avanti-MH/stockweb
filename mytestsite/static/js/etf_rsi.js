function original_profit(
    dates,
    profit,
    mdd,
){
    var obj = {

        chart: {
            type: 'line'
        },
        title: {
            text: 'backtest'
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
            name: 'profit',
            data: profit = dates.map((date ,index) => [new Date(date).getTime(), profit[index]]),

            },
            {
            name: 'mdd',
            data: mdd = dates.map((date ,index) => [new Date(date).getTime(), mdd[index]]),

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
function candle_plot(
    dates,
    data, 
    trade
){
    const   ohlc = [],
            volume = [],
            buy_scatter = [],
            sell_scatter = [],
            dataLength = data.length,
    // set the allowed units for data grouping
    groupingUnits = [[
        'week',                         // unit name
        [1]                             // allowed multiples
    ], [
        'month',
        [1, 2, 3, 4, 6]
    ]];
    
    for (let date of dates) {
        //console.log(date)
        buf = [
            new Date(date).getTime(), 
            data['open'][date],
            data['high'][date],
            data['low'][date],
            data['close'][date],
        ]
        ohlc.push(buf);
        buf = [
            new Date(date).getTime(), 
            data['volume'][date],
        ]
        volume.push(buf);
    }
    for (let [k,date] of Object.entries(trade[2])) {
        buf = [new Date(date).getTime(), data['volume'][date]];
        buy_scatter.push(buf);
    }
    for (let [k,date] of Object.entries(trade[4])) {
        buf = [new Date(date).getTime(), data['volume'][date]];
        sell_scatter.push(buf);
    }
    var obj = {

        rangeSelector: {
            selected: 4
        },

        title: {
            text: $('#stock').val() + ' Historical'
        },

        yAxis: [{
            labels: {
                align: 'right',
                x: -3
            },
            title: {
                text: 'OHLC'
            },
            height: '60%',
            lineWidth: 2,
            resize: {
                enabled: true
            }
        }, {

            title: {
                text: 'Volume'
            },
            top: '65%',
            height: '35%',
            offset: 0,
            lineWidth: 2
        }],

        tooltip: {
            split: true
        },

        series: [{
            type: 'candlestick',
            name: $('#stock').val(),
            data: ohlc,
            color: '#FF7F7F',
            upColor: '#90EE90',
            dataGrouping: {
                units: groupingUnits
            }
        }, {
            type: 'column',
            name: 'Volume',
            data: volume,
            yAxis: 1,
            dataGrouping: {
                units: groupingUnits
            }
        },
        {
            type: 'scatter',
            data: buy_scatter,
            name: 'order',
            yAxis: 1,
            marker: {
                name: "buy",
                fillColor: 'transparent',
                lineColor: 'green',
                lineWidth: 1,
                enabled: true,
                radius: 2,
            },
            dataLabels: {
                enabled: true,
                formatter: function() {
                    return 'B'; // This will display 'B' next to each data point
                },
                style: {
                    color: 'white', // Customize the label color
                    textOutline: '1px green' // Optional: add outline for better visibility
                },
            visible: true,
            }
        },
        {
            type: 'scatter',
            data: sell_scatter,
            name: 'cover',
            yAxis: 1,
            marker: {
                name: "sell",
                fillColor: 'transparent',
                lineColor: 'red',
                lineWidth: 1,
                enabled: true,
                radius: 2,
            },
            dataLabels: {
                enabled: true,
                formatter: function() {
                    return 'S'; // This will display 'B' next to each data point
                },
                style: {
                    color: 'white', // Customize the label color
                    textOutline: '1px red' // Optional: add outline for better visibility
                },
            visible: true,
            }
        }
        ]
    }
    var x = document.getElementById("container_candle");
    if (x.hidden === true) {
        x.hidden = !x.hidden;
    }
    // Create the chart
    Highcharts.stockChart('container_candle', obj);
}

function trading_table(trade) {
    const dataset = [];
    let buf = 0;

    // Prepare the dataset
    for (const i in trade['0']) {
        const pro = trade[5][i] - trade[3][i];
        buf += pro;
        dataset.push([
            trade[1][i],                   // Trade ID
            trade[2][i].slice(0, 10),      // Start Date
            trade[3][i].toFixed(2),        // Start Price
            trade[4][i].slice(0, 10),      // End Date
            trade[5][i].toFixed(2),        // End Price
            trade[6][i],                   // Status
            pro.toFixed(2),                // Profit
            buf.toFixed(2)                 // Cumulative Profit
        ]);
    }

    const tableId = '#container_Table';
    const tableContainer = document.getElementById("container_Table");

    // Show the table if hidden
    if (tableContainer.hidden === true) {
        tableContainer.hidden = false;
    }

    // Destroy the DataTable instance if it exists
    if ($.fn.DataTable.isDataTable(tableId)) {
        $(tableId).DataTable().clear().destroy(); // Clear data and destroy instance
    }

    // Reinitialize DataTable with new data
    $(tableId).DataTable({
        data: dataset,
        columns: [
            { title: "Trade ID" },
            { title: "Start Date" },
            { title: "Start Price" },
            { title: "End Date" },
            { title: "End Price" },
            { title: "Status" },
            { title: "Profit" },
            { title: "Cumulative Profit" }
        ],
    });
}

$(document).ready(
    function() {
        $("#click_action").click(
            function() {
                var stock       = $('#stock').val()
                var strategy    = $('#strategy').val()
                var start_date  = $('#start_date').val()
                var end_date    = $('#end_date').val()
                var ShortRSI    = $('#ShortRSI').val()
                var LongRSI     = $('#LongRSI').val()
                
                var data_config = new FormData();
                data_config.append("stock", stock);
                data_config.append("strategy", strategy);
                data_config.append("start_date", start_date);
                data_config.append("end_date", end_date);
                data_config.append("LongRSI", LongRSI);
                data_config.append("ShortRSI", ShortRSI);
                /*
                for (elem of data_config.entries()) {
                    console.log(elem[0], elem[1])
                }
                */
                $.ajax(
                    {
                        headers: { "X-CSRFToken": csrf_token  },
                        type: "POST", // what type of Request (GET or POST)
                        url: "/stockapp/etf_rsi",
                        dataType: "json",
                        data: data_config,
                        processData: false,
                        contentType: false,
                        success: function(xhr){
                            console.log("success")
                            console.log(xhr)
                            dates = Object.keys(xhr['data']['close'])
                           original_profit(
                                dates,
                                xhr['result']['acc_ret'],
                                xhr['result']['dd'],
                            )
                            
                            candle_plot(
                                dates,
                                xhr['data'], 
                                xhr['trade']
                            )
                            trading_table(xhr['trade'])
/*                             //buf = document.getElementById("container_log")
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
                                xhr['profits_daily'],)*/
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