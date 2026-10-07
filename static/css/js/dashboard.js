// ===============================
// Monthly Performance Chart
// ===============================

const chartArea = document.getElementById("monthlyChart");

if (chartArea) {

    new Chart(chartArea, {

        type: "bar",

        data: {

            labels: [
                "Orders",
                "Revenue",
                "Customers",
                "Avg Order Value"
            ],

            datasets: [

                {
                    label: "Last Month",

                    data: [
                        dashboardData.last_orders,
                        dashboardData.last_revenue,
                        dashboardData.last_customers,
                        dashboardData.last_aov
                    ]
                },

                {
                    label: "This Month",

                    data: [
                        dashboardData.this_orders,
                        dashboardData.this_revenue,
                        dashboardData.this_customers,
                        dashboardData.this_aov
                    ]
                }

            ]
        },

        options: {

            responsive: true,

            maintainAspectRatio: false,

            plugins: {

                legend: {
                    position: "top"
                }

            },

            scales: {

                y: {
                    beginAtZero: true
                }

            }

        }

    });

}


// ===============================
// Category-wise Buying Behavior
// ===============================

const categoryChartArea = document.getElementById("categoryChart");

if (categoryChartArea) {

    new Chart(categoryChartArea, {

        type: "doughnut",

        data: {

            labels: dashboardData.category_names,

            datasets: [{

                label: "Category Revenue",

                data: dashboardData.category_values

            }]

        },

        options: {

            responsive: true,

            maintainAspectRatio: false,

            plugins: {

                legend: {
                    position: "right"
                }

            }

        }

    });

}


// ===============================
// Customer Segmentation Chart
// ===============================

const segmentChartArea = document.getElementById("segmentChart");

if (segmentChartArea) {

    new Chart(segmentChartArea, {

        type: "doughnut",

        data: {

            labels: dashboardData.segment_names,

            datasets: [{

                label: "Customers",

                data: dashboardData.segment_values

            }]

        },

        options: {

            responsive: true,

            maintainAspectRatio: false,

            plugins: {

                legend: {
                    position: "right"
                }

            }

        }

    });

}


// ===============================
// Demand Prediction Chart
// ===============================

const demandChartArea = document.getElementById("demandChart");

if (demandChartArea) {

    new Chart(demandChartArea, {

        type: "bar",

        data: {

            labels: dashboardData.demand_categories,

            datasets: [{

                label: "Predicted Next Month Demand",

                data: dashboardData.predicted_demand

            }]

        },

        options: {

            responsive: true,

            maintainAspectRatio: false,

            plugins: {

                legend: {
                    position: "top"
                }

            },

            scales: {

                y: {
                    beginAtZero: true
                }

            }

        }

    });

}