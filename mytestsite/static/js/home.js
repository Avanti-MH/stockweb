// Mocked API response
const apiResponse = {
    subscriptions: {
        "2330.TW": {
            parameters: {
                start_date: "2021-01-01",
                ma_length_res_sup: 20,
                ma_mode_res_sup: "SMA",
                method_res_sup: 1,
                ma_length_kd: 20,
                fastperiod_macd: 12,
                slowperiod_macd: 26,
                signalperiod_macd: 9,
                ma_length_bollinger: 20,
                timeperiod_rsi: 14,
                timeperiod_adx: 14,
                timeperiod_dmi: 14
            },
            signals: [
                { date: "2025-01-15", price: 500, buy: true, sell: false },
                { date: "2025-01-16", price: 510, buy: false, sell: true }
            ],
            created_at: "2025-01-15 07:34:37"
        },
        "1303.TW": {
            parameters: {
                start_date: "2022-02-01",
                ma_length_res_sup: 30,
                ma_mode_res_sup: "EMA",
                method_res_sup: 2,
                ma_length_kd: 14,
                fastperiod_macd: 10,
                slowperiod_macd: 20,
                signalperiod_macd: 7,
                ma_length_bollinger: 25,
                timeperiod_rsi: 12,
                timeperiod_adx: 18,
                timeperiod_dmi: 15
            },
            signals: [
                { date: "2025-01-14", price: 300, buy: false, sell: true },
                { date: "2025-01-15", price: 310, buy: true, sell: false }
            ],
            created_at: "2025-01-14 08:22:45"
        },
        "2454.TW": {
            parameters: {
                start_date: "2023-03-15",
                ma_length_res_sup: 50,
                ma_mode_res_sup: "WMA",
                method_res_sup: 3,
                ma_length_kd: 10,
                fastperiod_macd: 15,
                slowperiod_macd: 30,
                signalperiod_macd: 10,
                ma_length_bollinger: 22,
                timeperiod_rsi: 16,
                timeperiod_adx: 20,
                timeperiod_dmi: 18
            },
            signals: [
                { date: "2025-01-13", price: 700, buy: false, sell: true },
                { date: "2025-01-15", price: 710, buy: true, sell: false }
            ],
            created_at: "2025-01-13 09:10:12"
        },
        "3008.TW": {
            parameters: {
                start_date: "2020-01-01",
                ma_length_res_sup: 40,
                ma_mode_res_sup: "SMA",
                method_res_sup: 4,
                ma_length_kd: 15,
                fastperiod_macd: 11,
                slowperiod_macd: 22,
                signalperiod_macd: 8,
                ma_length_bollinger: 28,
                timeperiod_rsi: 10,
                timeperiod_adx: 12,
                timeperiod_dmi: 12
            },
            signals: [
                { date: "2025-01-12", price: 1500, buy: true, sell: false },
                { date: "2025-01-14", price: 1520, buy: false, sell: true }
            ],
            created_at: "2025-01-12 06:55:00"
        }
    }
};
$(document).ready(function () {
    const tableBody = $("#subscriptions-table tbody");
    const detailContainer = $("#detail-container");
    let apiResponse = {};

    function fetchSubscriptions() {
        $.ajax({
            type: "GET",
            url: "http://127.0.0.1:8000/stockapp/",
            dataType: "json",
            success: function (response) {
                console.log(response)
                apiResponse = response;
                renderTable();
            },
            error: function (xhr) {
                console.error("Error fetching data:", xhr.responseText);
                tableBody.html(`<tr><td colspan="3" class="text-center">No data found.</td></tr>`);
            },
        });
    }

    function renderTable() {
        tableBody.empty();
        if (!apiResponse.subscriptions || Object.keys(apiResponse.subscriptions).length === 0) {
            tableBody.html(`<tr><td colspan="3" class="text-center">No subscriptions available.</td></tr>`);
            return;
        }
        Object.entries(apiResponse.subscriptions).forEach(([stock, details]) => {
            const row = `<tr>
                <td>${stock}</td>
                <td>${details.created_at}</td>
                <td>
                    <button class="detail-btn btn btn-primary btn-sm" data-stock="${stock}">Detail</button>
                    <button class="delete-btn btn btn-danger btn-sm" data-stock="${stock}">Delete</button>
                </td>
            </tr>`;
            tableBody.append(row);
        });
    }

    function renderDetailTable(stock, details) {
        detailContainer.empty();
        const { parameters, signals } = details;
    
        // 渲染參數表格
        let parameterInfo = `<h3>Parameters for ${stock}</h3>
            <table class="table table-bordered">
                <thead>
                    <tr>
                        <th>Parameter</th>
                        <th>Value</th>
                    </tr>
                </thead>
                <tbody>
                    ${Object.entries(parameters).map(([key, value]) => `
                        <tr>
                            <td>${key}</td>
                            <td>${value !== null ? value : "N/A"}</td>
                        </tr>`).join('')}
                </tbody>
            </table>`;
    
        // 渲染信號表格
        let signalInfo = "<h3>Signals</h3>";
        const signalEntries = Object.entries(signals);
    
        if (signalEntries.length > 0) {
            signalInfo += `<table class="table table-bordered">
                <thead>
                    <tr>
                        <th>Date</th>
                        <th>Price</th>
                        <th>Res_Sup_line</th>
                        <th>KD_line</th>
                        <th>MACD</th>
                        <th>RSI</th>
                        <th>Bollinger</th>
                        <th>ADX</th>
                        <th>K-Line</th>
                    </tr>
                </thead>
                <tbody>
                    ${signalEntries.map(([date, signal]) => `
                        <tr>
                            <td>${date}</td>
                            <td>${signal.price !== null ? signal.price.toFixed(2) : "N/A"}</td>
                            <td>${signal.Res_Sup_line !== null ? signal.Res_Sup_line : "N/A"}</td>
                            <td>${signal.KD_line !== null ? signal.KD_line : "N/A"}</td>
                            <td>${signal.MACD !== null ? signal.MACD : "N/A"}</td>
                            <td>${signal.RSI !== null ? signal.RSI : "N/A"}</td>
                            <td>${signal.Bollinger !== null ? signal.Bollinger : "N/A"}</td>
                            <td>${signal.ADX !== null ? signal.ADX : "N/A"}</td>
                            <td>${signal["K-Line"] !== null ? signal["K-Line"] : "N/A"}</td>
                        </tr>`).join('')}
                </tbody>
            </table>`;
        } else {
            signalInfo += `<p>No signals available for ${stock}</p>`;
        }
    
        // 將表格插入容器
        detailContainer.append(parameterInfo);
        detailContainer.append(signalInfo);
    }

    // Fetch data and initialize table on page load
    fetchSubscriptions();

    // Handle detail and delete button clicks
    tableBody.on("click", ".detail-btn", function () {
        const stock = $(this).data("stock");
        const details = apiResponse.subscriptions[stock];
        renderDetailTable(stock, details);
    });

    tableBody.on("click", ".delete-btn", function () {
        const stock = $(this).data("stock");
        delete apiResponse.subscriptions[stock];
        renderTable();
        detailContainer.empty();
        alert(`Stock ${stock} deleted.`);
        var data_config = new FormData();
        data_config.append("stock_code", stock);
                $.ajax(
                    {
                        headers: { "X-CSRFToken": csrf_token  },
                        type: "POST", // what type of Request (GET or POST)
                        url: "/stockapp/delete",
                        dataType: "json",
                        data: data_config,
                        processData: false,
                        contentType: false,
                        success: function(xhr){
                            console.log("success")
                        },
                        error: function(xhr, status, error){
                            console.log(error)
                        },
                    }
                )

    });
});

// Call this function on page load
//fetchSubscriptions();



// 

// $(document).ready(function () {
//     const tableBody = $("#subscriptions-table tbody");
//     const detailContainer = $("#detail-container");

//     function renderTable() {
//         tableBody.empty();
//         Object.entries(apiResponse.subscriptions).forEach(([stock, details]) => {
//             const row = `<tr>
//                 <td>${stock}</td>
//                 <td>${details.created_at}</td>
//                 <td>
//                     <button class="detail-btn btn btn-primary btn-sm" data-stock="${stock}">Detail</button>
//                     <button class="delete-btn btn btn-danger btn-sm" data-stock="${stock}">Delete</button>
//                 </td>
//             </tr>`;
//             tableBody.append(row);
//         });
//     }

//     function renderDetailTable(stock, details) {
//         detailContainer.empty();
//         const { parameters, signals } = details;

//         let parameterInfo = `<h3>Parameters for ${stock}</h3>
//             <table class="table table-bordered">
//                 <thead>
//                     <tr>
//                         <th>Parameter</th>
//                         <th>Value</th>
//                     </tr>
//                 </thead>
//                 <tbody>
//                     ${Object.entries(parameters).map(([key, value]) => `
//                         <tr>
//                             <td>${key}</td>
//                             <td>${value}</td>
//                         </tr>`).join('')}
//                 </tbody>
//             </table>`;

//         let signalInfo = "<h3>Signals</h3>";
//         if (signals.length > 0) {
//             signalInfo += `<table class="table table-bordered">
//                 <thead>
//                     <tr>
//                         <th>Date</th>
//                         <th>Price</th>
//                         <th>Buy</th>
//                         <th>Sell</th>
//                     </tr>
//                 </thead>
//                 <tbody>
//                     ${signals.map(signal => `
//                         <tr>
//                             <td>${signal.date}</td>
//                             <td>${signal.price}</td>
//                             <td>${signal.buy}</td>
//                             <td>${signal.sell}</td>
//                         </tr>`).join('')}
//                 </tbody>
//             </table>`;
//         } else {
//             signalInfo += `<p>No signals available for ${stock}</p>`;
//         }

//         detailContainer.append(parameterInfo);
//         detailContainer.append(signalInfo);
//     }

//     renderTable();

//     tableBody.on("click", ".detail-btn", function () {
//         const stock = $(this).data("stock");
//         const details = apiResponse.subscriptions[stock];
//         renderDetailTable(stock, details);
//     });

//     tableBody.on("click", ".delete-btn", function () {
//         const stock = $(this).data("stock");
//         delete apiResponse.subscriptions[stock];
//         renderTable();
//         detailContainer.empty();
//         alert(`Stock ${stock} deleted.`);
//     });
// });