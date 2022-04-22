// For the Sign-out menu
const storage = window.localStorage
google.charts.load('current', {'packages':['bar']});
google.charts.load('current', {'packages':['corechart']});
google.charts.load('current', {'packages':['table']});
let countries = [];

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

//Signup
$( function() {
    $("#country-input").autocomplete({
        source: countries
    });
});


// Graphs
function visitsChart() {
    const data = google.visualization.arrayToDataTable(visits)

    const options = {
        width: 500,
        height: 500,
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
        width: 500,
        height: 500,
        title: 'Downloads by country'
    };

    const chart = new google.visualization.PieChart(document.getElementById('downloadChart'));

    chart.draw(data, options);
}

function horizontalBars (level, levelNumber) {
    var data = new google.visualization.arrayToDataTable(JSON.parse(level.values));

    var options = {
        width: 500,
        height: 500,
        legend: { position: 'none' },
        chart: {
            title: level.title ,
        },
        bars: 'horizontal',
            axes: {
            x: {
                0: { side: 'top', label: 'Time (s)'}
            }
        },
        bar: { groupWidth: "90%" }
    };

    var chart = new google.charts.Bar(document.getElementById(`level${levelNumber}`));
    chart.draw(data, options);
}

function table () {
    var data = new google.visualization.arrayToDataTable(topscores);

    var table = new google.visualization.Table(document.getElementById('table_div'));

    table.draw(data, {showRowNumber: true, width: '100%', height: '100%'});
}

function lineChart () {
    var data = google.visualization.arrayToDataTable(sessions);

    var options = {
        width: 500,
        height: 500,
        title: 'Session Times',
        curveType: 'function',
        legend: { position: 'none' }
    };

    var chart = new google.visualization.LineChart(document.getElementById('curve_chart'));

    chart.draw(data, options);
}