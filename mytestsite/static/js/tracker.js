
function res_sup_series (
    candle_data,
    res, 
    sup, 
    ma, 
    higher, 
    lower,
) 
{
    const 
          buy_scatter = [],
          sell_scatter = [];
    for (let h of higher) {
        buf = [new Date(h[0]).getTime(), h[1]];
        sell_scatter.push(buf);
    }
    for (let l of lower) {
        buf = [new Date(l[0]).getTime(), l[1]];
        buy_scatter.push(buf);
    }

    s = [{
        name: 'res',
        type: 'line', // Specify the type as line
        data: candle_data.date.map((d ,index) => [new Date(d).getTime(), res[index]]),
        color: '#35d2d5', // Line color
        tooltip: {
            valueDecimals: 2
        }
    }, {
        name: 'ma',
        type: 'line', // Specify the type as line
        data: candle_data.date.map((d ,index) => [new Date(d).getTime(), ma[index]]),
        color: '#2f4f4f', // Line color
        tooltip: {
            valueDecimals: 2
        }
    }, {
        name: 'sup',
        type: 'line', // Specify the type as line
        data: candle_data.date.map((d ,index) => [new Date(d).getTime(), sup[index]]),
        color: '#ff3333', // Line color
        tooltip: {
            valueDecimals: 2
        }
    }, {
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
    }, {
        type: 'scatter',
        data: sell_scatter,
        name: 'sell',
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
    }]
    return s
}
function KD_series (
    candle_data,
    K, 
    D,  
    sells, 
    buys,
) 
{
    const 
          buy_scatter = [],
          sell_scatter = [];
    for (let h of sells) {
        buf = [new Date(h[0]).getTime(), h[1]];
        sell_scatter.push(buf);
    }
    for (let l of buys) {
        buf = [new Date(l[0]).getTime(), l[1]];
        buy_scatter.push(buf);
    }

    s = [{
        name: 'K',
        yAxis: 2,
        type: 'line', // Specify the type as line
        data: candle_data.date.map((d ,index) => [new Date(d).getTime(), K[index]]),
        color: '#35d2d5', // Line color
        tooltip: {
            valueDecimals: 2
        }
    }, {
        name: 'D',
        yAxis: 2,
        type: 'line', // Specify the type as line
        data: candle_data.date.map((d ,index) => [new Date(d).getTime(), D[index]]),
        color: '#ff3333', // Line color
        tooltip: {
            valueDecimals: 2
        }
    }, {
        type: 'scatter',
        data: buy_scatter,
        name: 'order',
        //yAxis: 1,
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
    }, {
        type: 'scatter',
        data: sell_scatter,
        name: 'cover',
        //yAxis: 1,
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
    }]
    return s
}

// TODO: please finish the remained series
function MACD_series(candle_data, macd, signal, histogram,  
    sells, 
    buys,) {
    
    const 
    buy_scatter = buys,
    sell_scatter = sells;

    return [{
        name: 'MACD',
        yAxis: 2,
        type: 'line',
        data: candle_data.date.map((d, index) => [new Date(d).getTime(), macd[index]]),
        color: '#1f77b4',
        tooltip: { valueDecimals: 2 }
    }, {
        name: 'Signal',
        yAxis: 2,
        type: 'line',
        data: candle_data.date.map((d, index) => [new Date(d).getTime(), signal[index]]),
        color: '#ff7f0e',
        tooltip: { valueDecimals: 2 }
    }, {
        name: 'Histogram',
        yAxis: 2,
        type: 'column',
        data: candle_data.date.map((d, index) => ({
            x: new Date(d).getTime(),
            y: histogram[index],
            color: histogram[index] >= 0 ? '#2ca02c' : '#d62728' // Green for positive, red for negative
        })),
        tooltip: { valueDecimals: 2 }
    }, {
        type: 'scatter',
        data: buy_scatter,
        name: 'order',
        //yAxis: 1,
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
    }, {
        type: 'scatter',
        data: sell_scatter,
        name: 'cover',
        //yAxis: 1,
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
    }];
}

function Bollinger_series(candle_data, upper, middle, lower,  
    sells, 
    buys,) {
    
    const 
    buy_scatter = buys,
    sell_scatter = sells;

    return [{
        name: 'Upper Band',
        yAxis: 0,
        type: 'line',
        data: candle_data.date.map((d, index) => [new Date(d).getTime(), upper[index]]),
        color: '#17becf',
        tooltip: { valueDecimals: 2 }
    }, {
        name: 'Middle Band',
        yAxis: 0,
        type: 'line',
        data: candle_data.date.map((d, index) => [new Date(d).getTime(), middle[index]]),
        color: '#7f7f7f',
        tooltip: { valueDecimals: 2 }
    }, {
        name: 'Lower Band',
        yAxis: 0,
        type: 'line',
        data: candle_data.date.map((d, index) => [new Date(d).getTime(), lower[index]]),
        color: '#bcbd22',
        tooltip: { valueDecimals: 2 }
    }, {
        type: 'scatter',
        data: buy_scatter,
        name: 'order',
        //yAxis: 1,
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
    }, {
        type: 'scatter',
        data: sell_scatter,
        name: 'cover',
        //yAxis: 1,
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
    }];
}

function RSI_series(candle_data, rsi,  
    sells, 
    buys,) {
    
    const 
    buy_scatter = buys,
    sell_scatter = sells;
    return [{
        name: 'RSI',
        yAxis: 2,
        type: 'line',
        data: candle_data.date.map((d, index) => [new Date(d).getTime(), rsi[index]]),
        color: '#9467bd',
        tooltip: { valueDecimals: 2 }
    }, {
        type: 'scatter',
        data: buy_scatter,
        name: 'order',
        //yAxis: 1,
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
    }, {
        type: 'scatter',
        data: sell_scatter,
        name: 'cover',
        //yAxis: 1,
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
    }];
}

function ADX_series(candle_data, adx, plus_di, minus_di,  
    sells, 
    buys,) {
    
    const 
    buy_scatter = buys,
    sell_scatter = sells;
    return [{
        name: 'ADX',
        yAxis: 2,
        type: 'line',
        data: candle_data.date.map((d, index) => [new Date(d).getTime(), adx[index]]),
        color: '#8c564b',
        tooltip: { valueDecimals: 2 }
    }, {
        name: '+DI',
        yAxis: 2,
        type: 'line',
        data: candle_data.date.map((d, index) => [new Date(d).getTime(), plus_di[index]]),
        color: '#2ca02c',
        tooltip: { valueDecimals: 2 }
    }, {
        name: '-DI',
        yAxis: 2,
        type: 'line',
        data: candle_data.date.map((d, index) => [new Date(d).getTime(), minus_di[index]]),
        color: '#d62728',
        tooltip: { valueDecimals: 2 }
    }, {
        type: 'scatter',
        data: buy_scatter,
        name: 'order',
        //yAxis: 1,
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
    }, {
        type: 'scatter',
        data: sell_scatter,
        name: 'cover',
        //yAxis: 1,
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
    }];
}

function DMI_series(candle_data, dmi_positive, dmi_negative) {
    return [{
        name: '+DMI',
        yAxis: 2,
        type: 'line',
        data: candle_data.date.map((d, index) => [new Date(d).getTime(), dmi_positive[index]]),
        color: '#2ca02c',
        tooltip: { valueDecimals: 2 }
    }, {
        name: '-DMI',
        yAxis: 2,
        type: 'line',
        data: candle_data.date.map((d, index) => [new Date(d).getTime(), dmi_negative[index]]),
        color: '#d62728',
        tooltip: { valueDecimals: 2 }
    }];
}
function CDL_series(candle_data,  
    sells, 
    buys,) {
    
    const 
    buy_scatter = buys,
    sell_scatter = sells;
    return [{
        type: 'scatter',
        data: buy_scatter,
        name: 'order',
        //yAxis: 1,
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
    }, {
        type: 'scatter',
        data: sell_scatter,
        name: 'cover',
        //yAxis: 1,
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
    }];
}
// TODO: please finish the remained series

function candle_chart_v2(
    stock_code, 
    tracker_name, 
    candle_data, 
    other_series = [], y = []) {

    const ohlc = [],
          volumeSeriesData = [];
          
    for (let i = 0; i < candle_data.date.length; i += 1) {
        
        ohlc.push([
            new Date(candle_data.date[i]).getTime(),
            candle_data.Open[i],
            candle_data.High[i],
            candle_data.Low[i],
            candle_data.Close[i]
        ]);
        volumeSeriesData.push([
            candle_data.date[i],
            candle_data.Volume[i]
        ]);
    }

    if (y.length === 0) {
        top_set = '80%'
        height_set = '20%'
    } else if (y.length === 1) {
        top_set = '60%'
        height_set = '20%'
    } else {
        top_set = '60%'
        height_set = '20%'
    }

    base_y = [{
        labels: {
            align: 'left'
        },
        height: top_set,
        resize: {
            enabled: true
        }
    }, {
        labels: {
            align: 'left'
        },
        top: top_set,
        height: height_set,
        offset: 0
    }, ]

    base_series = [{
        type: 'candlestick',
        id: stock_code + '-candlestick',
        name: stock_code + ' Corp Stock Price',
        data: ohlc,
        dataGrouping: {
            groupPixelWidth: 20
        }
    }, {
        type: 'column',
        id: stock_code+'-volume',
        name: stock_code + ' Volume',
        data: volumeSeriesData,
        yAxis: 1
    },]

    complete_series = base_series.concat(other_series)
    complete_y      = base_y.concat(y)

    obj = {
        title: {
            text: stock_code + ' ' + tracker_name
        },
        yAxis: complete_y,
        rangeSelector: {
            selected: 4
        },
        tooltip: {
            shape: 'square',
            headerShape: 'callout',
            borderWidth: 0,
            shadow: false,
            positioner: function (width, height, point) {
                const chart = this.chart;

                if (point.formatPrefix === 'point') {
                    return {
                        x: point.series.chart.plotLeft,
                        y: point.series.yAxis.top - chart.plotTop
                    };
                }

                return {
                    x: Math.max(
                        // Left side limit
                        chart.plotLeft,
                        Math.min(
                            point.plotX + chart.plotLeft - width / 2,
                            // Right side limit
                            chart.chartWidth - width - chart.marginRight
                        )
                    ),
                    y: point.plotY
                };
            }, 

        },
        series: complete_series,
        responsive: {
            rules: [{
                condition: {
                    maxWidth: 800
                },
                chartOptions: {
                    rangeSelector: {
                        inputEnabled: false
                    }
                }
            }]
        }
    }
    var x = document.getElementById('container_'+tracker_name, obj);
    
    if (x.hidden === true) {
        x.hidden = !x.hidden;
    }
    Highcharts.stockChart('container_'+tracker_name, obj);
}

// click action
$(document).ready(
    function() {
        $("#submit_action").click(
            function() {
                var stock_code     = $('#stock_code').val();
                var start_date     = $('#start_date').val();
                var method         = $('#method').val();

                var data_config = new FormData();
                data_config.append("stock_code", stock_code);
                data_config.append("start_date", start_date);
                data_config.append("method", method);

                // Collect all possible parameters regardless of method
                data_config.append("ma_length_res_sup", $('#ma_length_res_sup').val());
                data_config.append("ma_mode_res_sup", $('#ma_mode_res_sup').val());
                data_config.append("method_res_sup", $('#method_res_sup').val());
                data_config.append("ma_length_kd", $('#ma_length_kd').val());
                data_config.append("fastperiod_macd", $('#fastperiod_macd').val());
                data_config.append("slowperiod_macd", $('#slowperiod_macd').val());
                data_config.append("signalperiod_macd", $('#signalperiod_macd').val());
                data_config.append("ma_length_bollinger", $('#ma_length_bollinger').val());
                data_config.append("timeperiod_rsi", $('#timeperiod_rsi').val());
                data_config.append("timeperiod_adx", $('#timeperiod_adx').val());
                data_config.append("timeperiod_dmi", $('#timeperiod_dmi').val());
                data_config.append("pattern_kline", $('#pattern_kline').val());

                /*
                for (elem of data_config.entries()) {
                    console.log(elem[0], elem[1]);
                }
                */
                $.ajax(
                    {
                        headers: { "X-CSRFToken": csrf_token },
                        type: "POST", // what type of Request (GET or POST)
                        url: "http://127.0.0.1:8001/api/strategies/tracker/run/",
                        dataType: "json",
                        data: data_config,
                        processData: false,
                        contentType: false,
                        success: function(xhr){
                            console.log("success");
                            console.log(xhr);
                            // res_sup_chart(
                            //     stock_code,
                            //     'res_sup',
                            //     xhr['candle_data'],
                            //     xhr['res_line'],
                            //     xhr['sup_line'],
                            //     xhr['ma_result'],
                            //     xhr['higher_than_res'],
                            //     xhr['less_than_sup']
                            // )
                            candle_chart_v2(
                                stock_code,
                                'res_sup',
                                xhr.res_sup['candle_data'],
                                res_sup_series(
                                    xhr.res_sup['candle_data'],
                                    xhr.res_sup['res_line'],
                                    xhr.res_sup['sup_line'],
                                    xhr.res_sup['ma_result'],
                                    xhr.res_sup['higher_than_res'],
                                    xhr.res_sup['less_than_sup']
                                )
                            );
                            candle_chart_v2(
                                stock_code,
                                'kd',
                                xhr.res_sup['candle_data'],
                                KD_series(
                                    xhr.res_sup['candle_data'],
                                    xhr.kd['K'],
                                    xhr.kd['D'],
                                    xhr.kd['sell_kd'],
                                    xhr.kd['buy_kd']
                                ),
                                {
                                    labels: {
                                        align: 'left'
                                    },
                                    top: '80%',
                                    height: '20%',
                                    offset: 0
                                }
                            );
                            // TODO: please finish the remained candle_chart_v2
                            candle_chart_v2(
                                stock_code,
                                'macd',
                                xhr.res_sup['candle_data'],
                                MACD_series(
                                    xhr.res_sup['candle_data'],
                                    xhr.macd['macd'],
                                    xhr.macd['macdsignal'],
                                    xhr.macd['macdhist'],
                                    xhr.signals.MACD.sell,
                                    xhr.signals.MACD.buy
                                ),
                                {
                                    labels: { align: 'left' },
                                    top: '80%',
                                    height: '20%',
                                    offset: 0
                                }
                            );
                        
                            candle_chart_v2(
                                stock_code,
                                'bollinger',
                                xhr.res_sup['candle_data'],
                                Bollinger_series(
                                    xhr.res_sup['candle_data'],
                                    xhr.bollinger['upper'],
                                    xhr.bollinger['middle'],
                                    xhr.bollinger['lower'],
                                    xhr.signals.Bollinger.sell,
                                    xhr.signals.Bollinger.buy
                                )
                            );
                        
                            candle_chart_v2(
                                stock_code,
                                'rsi',
                                xhr.res_sup['candle_data'],
                                RSI_series(
                                    xhr.res_sup['candle_data'],
                                    xhr.rsi['rsi'],
                                    xhr.signals.RSI.sell,
                                    xhr.signals.RSI.buy
                                ),
                                [{
                                    labels: { align: 'left' },
                                    top: '80%',
                                    height: '20%',
                                    offset: 0
                                }]
                            );
                        
                            candle_chart_v2(
                                stock_code,
                                'adx',
                                xhr.res_sup['candle_data'],
                                ADX_series(
                                    xhr.res_sup['candle_data'],
                                    xhr.adx['adx'],
                                    xhr.dmi['plus_di'],
                                    xhr.dmi['minus_di'],
                                    xhr.signals.ADX.sell,
                                    xhr.signals.ADX.buy
                                ),
                                [{
                                    labels: { align: 'left' },
                                    top: '80%',
                                    height: '20%',
                                    offset: 0
                                }]
                            );
                        
                            candle_chart_v2(
                                stock_code,
                                'dmi',
                                xhr.res_sup['candle_data'],
                                DMI_series(
                                    xhr.res_sup['candle_data'],
                                    xhr.dmi['plus_di'],
                                    xhr.dmi['minus_di']
                                ),
                                [{
                                    labels: { align: 'left' },
                                    top: '80%',
                                    height: '20%',
                                    offset: 0
                                }]
                                
                            );
                            candle_chart_v2(
                                stock_code,
                                'kline_status',
                                xhr.res_sup['candle_data'],
                                CDL_series(
                                    xhr.res_sup['candle_data'],
                                    xhr.signals['K-Line'].sell,
                                    xhr.signals['K-Line'].buy
                                ),
                                
                            );
                            // TODO: please finish the remained candle_chart_v2

                        },
                        error: function(xhr, status, error){
                            console.log(error);
                        },
                    }
                );
            }
        );
    }
);

// click action
$(document).ready(
    function() {
        $("#subscribe_action").click(
            function() {
                var stock_code     = $('#stock_code').val();
                var start_date     = $('#start_date').val();
                var method         = $('#method').val();

                var data_config = new FormData();
                data_config.append("stock_code", stock_code);
                data_config.append("start_date", start_date);
                data_config.append("method", method);

                // Collect all possible parameters regardless of method
                data_config.append("ma_length_res_sup", $('#ma_length_res_sup').val());
                data_config.append("ma_mode_res_sup", $('#ma_mode_res_sup').val());
                data_config.append("method_res_sup", $('#method_res_sup').val());
                data_config.append("ma_length_kd", $('#ma_length_kd').val());
                data_config.append("fastperiod_macd", $('#fastperiod_macd').val());
                data_config.append("slowperiod_macd", $('#slowperiod_macd').val());
                data_config.append("signalperiod_macd", $('#signalperiod_macd').val());
                data_config.append("ma_length_bollinger", $('#ma_length_bollinger').val());
                data_config.append("timeperiod_rsi", $('#timeperiod_rsi').val());
                data_config.append("timeperiod_adx", $('#timeperiod_adx').val());
                data_config.append("timeperiod_dmi", $('#timeperiod_dmi').val());
                data_config.append("pattern_kline", $('#pattern_kline').val());

                /*
                for (elem of data_config.entries()) {
                    console.log(elem[0], elem[1]);
                }
                */
                $.ajax(
                    {
                        headers: { "X-CSRFToken": csrf_token },
                        type: "POST", // what type of Request (GET or POST)
                        url: "http://127.0.0.1:8000/stockapp/subscription",
                        dataType: "json",
                        data: data_config,
                        processData: false,
                        contentType: false,
                        success: function(xhr){
                            console.log(xhr)
                        },
                        error: function(xhr, status, error){
                            console.log(error);
                        },
                    }
                );
            }
        );
    }
);