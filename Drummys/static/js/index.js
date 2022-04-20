// For the Sign-out menu
const storage = window.localStorage
google.charts.load('current', {'packages':['bar']});
google.charts.load('current', {'packages':['corechart']});
google.charts.setOnLoadCallback(visitsChart);
google.charts.setOnLoadCallback(downloadChart);
visitsChart();
downloadChart();

console.log(visitas, downloads)

$(document).ready(() => {
    $("#save-button").hide();
})

const showSignOutButton = () => {
    const signout = document.getElementById("sign-out");
    if(storage.clicked === 'false'){
        signout.style.visibility = 'visible';
        storage['clicked'] = 'true';
    } else {
        signout.style.visibility = 'hidden';
        storage['clicked'] = 'false';
    }
}

const editUsername = () => {
    localStorage['username'] = $("#username-text").text();
    $("#edit-button").hide();
    $("#username-text").hide();
    $("#save-button").show();
    $("#username-text-div").append(`<input value=${localStorage.username} id="username-input" onchange="handleInputChange()"/>`)
    $("#username-text-div").append('<button id="save-button" class="button-filled-green" onclick="saveUsername()">Save</button>')
}

const saveUsername = () => {
    $("#username-input").remove();
    $("#save-button").remove();
    $("#username-text").text(localStorage.username)
    $("#username-text").show();
    $("#edit-button").show();
}

const handleInputChange = () => {
    localStorage['username'] = $("#username-input").val();
}

function visitsChart() {
    const data = google.visualization.arrayToDataTable(visitas);

    const options = {
        chart: {
            title: 'Visits',
            subtitle: 'Last 10 visits',
        },
        legend: {
            position: 'none',
        },
    };

    const chart = new google.charts.Bar(document.getElementById('visitsChart'));
    chart.draw(data, google.charts.Bar.convertOptions(options));
}

function downloadChart() {
    const data = google.visualization.arrayToDataTable(downloads)

    const options = {
        title: 'Downloads by country'
    };

    const chart = new google.visualization.PieChart(document.getElementById('downloadChart'));
    chart.draw(data, options);
}
