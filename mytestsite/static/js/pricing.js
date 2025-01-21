function river_chart(stock_code, candle_data, river_data) {
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
    obj = {
        yAxis: [{
            labels: {
                align: 'left'
            },
            height: '80%',
            resize: {
                enabled: true
            }
        }, {
            labels: {
                align: 'left'
            },
            top: '80%',
            height: '20%',
            offset: 0
        }],
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
            }
        },
        series: [{
            type: 'candlestick',
            id: stock_code + '-candlestick',
            name: stock_code + ' Corp Stock Price',
            data: ohlc,
            dataGrouping: {
                groupPixelWidth: 20
            }
        }, {
            type: 'column',
            id: 'nvidia-volume',
            name: stock_code + ' Volume',
            data: volumeSeriesData,
            yAxis: 1
        }, {
            name: '',
            type: 'line', // Specify the type as line
            data: candle_data.date.map((d ,index) => [new Date(d).getTime(), river_data[0][index]]),
            color: '#35d2d5', // Line color
            tooltip: {
                valueDecimals: 2
            }
        }, {
            name: '',
            type: 'line', // Specify the type as line
            data: candle_data.date.map((d ,index) => [new Date(d).getTime(), river_data[1][index]]),
            color: '#20d173', // Line color
            tooltip: {
                valueDecimals: 2
            }
        }, {
            name: '',
            type: 'line', // Specify the type as line
            data: candle_data.date.map((d ,index) => [new Date(d).getTime(), river_data[2][index]]),
            color: '#8ed120', // Line color
            tooltip: {
                valueDecimals: 2
            }
        }, {
            name: '',
            type: 'line', // Specify the type as line
            data: candle_data.date.map((d ,index) => [new Date(d).getTime(), river_data[3][index]]),
            color: '#fcce22', // Line color
            tooltip: {
                valueDecimals: 2
            }
        }, {
            name: '',
            type: 'line', // Specify the type as line
            data: candle_data.date.map((d ,index) => [new Date(d).getTime(), river_data[4][index]]),
            color: '#ff9933', // Line color
            tooltip: {
                valueDecimals: 2
            }
        }, {
            name: '',
            type: 'line', // Specify the type as line
            data: candle_data.date.map((d ,index) => [new Date(d).getTime(), river_data[5][index]]),
            color: '#ff3333', // Line color
            tooltip: {
                valueDecimals: 2
            }
        }],
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

    Highcharts.stockChart('river_candle_container', obj);
}

function speadometer(
    mathod_name,
    stock_code,
    low_price,
    avg_price,
    high_price,
    current_price,
) {
    low_price = Math.round(low_price)
    avg_price = Math.round(avg_price)
    high_price = Math.round(high_price)
    var end_price
    if (current_price > high_price * 2) {
        end_price = current_price + 10;
    } else {
        end_price = high_price * 2;
    }
    if (stock_code.includes('TW')) {
        unit = 'NTD';
    } else {
        unit = 'USD';
    }
    obj =  {

        chart: {
            type: 'gauge',
            plotBackgroundColor: null,
            plotBackgroundImage: null,
            plotBorderWidth: 0,
            plotShadow: false,
            height: '80%'
        },
    
        title: {
            text: mathod_name + ': ' + stock_code,
            style: {
                fontSize: '14px', // Set the title font size here
                fontWeight: 'bold', // Optional: Set the font weight
                color: '#333333' // Optional: Set the font color
            }
        },
    
        pane: {
            startAngle: -90,
            endAngle: 89.9,
            background: null,
            center: ['50%', '75%'],
            size: '110%'
        },
    
        // the value axis
        yAxis: {
            min: 0,
            max: end_price,
            tickPixelInterval: 72,
            tickPosition: 'inside',
            tickColor: Highcharts.defaultOptions.chart.backgroundColor || '#FFFFFF',
            tickLength: 10,
            tickWidth: 2,
            minorTickInterval: null,
            labels: {
                distance: 10,
                style: {
                    fontSize: '14px'
                }
            },
            lineWidth: 0,
            plotBands: [{
                from: 0,
                to: low_price,
                color: '#4fff33', // green
                thickness: 10,
                borderRadius: '50%',
                label: {
                    text: 'Low: ' + String(0) + ' - ' + String(low_price),
                    style: {
                        color: '#000000',
                        fontWeight: 'bold',
                        fontSize: '9px'
                    },
                    verticalAlign: 'middle',
                    align: 'center',
                    y: -30 // Adjust vertical position
                }
            }, {
                from: low_price,
                to: avg_price,
                color: '#ffbe33', // yellow
                thickness: 10,
                borderRadius: '50%',
                label: {
                    text: 'Resonable: ' + String(low_price) + ' - ' + String(avg_price),
                    style: {
                        color: '#000000',
                        fontWeight: 'bold',
                        fontSize: '9px'
                    },
                    verticalAlign: 'middle',
                    align: 'center',
                    y: -30 // Adjust vertical position
                }
            }, {
                from: avg_price,
                to: high_price,
                color: '#ff9933', // red
                thickness: 10,
                borderRadius: '50%',
                label: {
                    text: 'High: ' + String(avg_price) + ' - ' + String(high_price),
                    style: {
                        color: '#000000',
                        fontWeight: 'bold',
                        fontSize: '9px'
                    },
                    verticalAlign: 'middle',
                    align: 'center',
                    y: -30 // Adjust vertical position
                }
            }, {
                from: high_price,
                to:  end_price,
                color: '#ff3333', // red
                thickness: 10,
                borderRadius: '50%',
                label: {
                    text: 'EX High: ' + String(high_price) + ' - ' + String(end_price),
                    style: {
                        color: '#000000',
                        fontWeight: 'bold',
                        fontSize: '9px'
                    },
                    verticalAlign: 'middle',
                    align: 'center',
                    y: -30 // Adjust vertical position
                }
            },]
        },
    
        series: [{
            name: 'Speed',
            data: [current_price],
            tooltip: {
                valueSuffix: ' ' + unit
            },
            dataLabels: {
                format: '{y} ' + unit,
                borderWidth: 0,
                color: (
                    Highcharts.defaultOptions.title &&
                    Highcharts.defaultOptions.title.style &&
                    Highcharts.defaultOptions.title.style.color
                ) || '#333333',
                style: {
                    fontSize: '12px'
                }
            },
            dial: {
                radius: '80%',
                backgroundColor: 'gray',
                baseWidth: 12,
                baseLength: '0%',
                rearLength: '0%'
            },
            pivot: {
                backgroundColor: 'gray',
                radius: 6
            }
    
        }]
    
    }

    // Create the chart
    //Highcharts.chart('container_'+mathod_name, param);
    Highcharts.chart('container_'+mathod_name, obj);
}

// click action
$(document).ready(
    function() {
        $("#submit_action").click(
            function() {
                var stock_code     = $('#stock_code').val()
                var start_date     = $('#start_date').val()
                var end_date       = $('#end_date').val()
                var time_frame   = $('#time_frame').val()


                var data_config = new FormData();
                data_config.append("stock_code", stock_code);
                data_config.append("start_date", start_date);
                data_config.append("end_date", end_date);
                data_config.append("time_frame", time_frame);

                /*
                for (elem of data_config.entries()) {
                    console.log(elem[0], elem[1])
                }
                */
                $.ajax(
                    {
                        headers: { "X-CSRFToken": csrf_token  },
                        type: "POST", // what type of Request (GET or POST)
                        url: "http://127.0.0.1:8001/api/strategies/pricing/run/",
                        dataType: "json",
                        data: data_config,
                        processData: false,
                        contentType: false,
                        success: function(xhr){
                            console.log("success")
                            console.log(xhr)
                            console.log(xhr['dividend'].low_price)
                            var x = document.getElementById("grid_container");
                            console.log(x.hidden)
                            if (x.hidden === true) {
                                x.hidden = !x.hidden;
                            }
                            speadometer(
                                'dividend_price_method',
                                stock_code,
                                xhr['dividend'].low_price,
                                xhr['dividend'].avg_price,
                                xhr['dividend'].high_price,
                                xhr['current_price'],
                            )
                            speadometer(
                                'high_low_price_method',
                                stock_code,
                                xhr['high_low'].low_price,
                                xhr['high_low'].avg_price,
                                xhr['high_low'].high_price,
                                xhr['current_price'],
                            )
                            speadometer(
                                'pb_method',
                                stock_code,
                                xhr['pb'].lowest_pb_price,
                                xhr['pb'].avg_pb_price,
                                xhr['pb'].highest_pb_price,
                                xhr['current_price'],
                            )
                            speadometer(
                                'pe_method',
                                stock_code,
                                xhr['pe'].lowest_pe_price,
                                xhr['pe'].avg_pe_price,
                                xhr['pe'].highest_pe_price,
                                xhr['current_price'],
                            )
                            river_chart(
                                stock_code,
                                xhr['candle_data'],
                                xhr['river_lines']
                            )
                            speadometer(
                                'river_chart_method',
                                stock_code,
                                xhr['river'].lowest_price,
                                xhr['river'].avg_price,
                                xhr['river'].highest_price,
                                xhr['current_price'],
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