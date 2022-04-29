// For the Sign-out menu
const storage = window.localStorage
google.charts.load('current', {'packages':['bar']});
google.charts.load('current', {'packages':['corechart']});
google.charts.load('current', {'packages':['table']});
let countries = [];
let usernames = [];
let topscores
let sessions
let level1
let level2
let level3
let downloads
let visits

function onDownload () {
    const request = new XMLHttpRequest();
    request.open("GET", "/api/download", true);
    request.send()
}

function logout () {
    const request = new XMLHttpRequest();
    request.open("GET", "/user/logout", true);
    request.send()
}

function checkSamePassword () {
    const password = document.getElementById("signup-password").value
    const confirmPassword = document.getElementById("confirm-password").value
    if(password === confirmPassword){
        $("#error-msg").remove();
        document.getElementById("signup-submit").disabled = false;
    } else {
        $("#signup form").append("<p id='error-msg' class='error'>The password doesn't match</p>")
    }
}

function checkUsernameAvailable () {
    const username = document.getElementById("signup-username").value
    const exists = usernames.some((el) => el === username)
    if(exists){
        $("#signup-username-div").append("<p id='error-msg' class='error'>The user already exists</p>")
    } else {
        $("#error-msg").remove()
    }
}

function removeOnChange () {
    document.getElementById("signup-username").removeEventListener('change', checkUsernameAvailable)
    document.getElementById("confirm-password").removeEventListener('change', checkSamePassword)
}

$(document).ready(() => {
    $("#save-button").hide();
    document.getElementById("signup-submit").disabled = true;
    document.getElementById("confirm-password").addEventListener('change', checkSamePassword)
    document.getElementById("signup-username").addEventListener('change', checkUsernameAvailable)
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

function editUsername () {
    localStorage['username'] = $("#username-text").text();
    $("#edit-button").hide();
    $("#username-text").hide();
    $("#save-button").show();
    $("#username-text-div").append(`<input value="${localStorage.username}" id="username-input" onchange="handleInputChange()"/>`)
    $("#username-text-div").append('<button id="save-button" class="button-filled-green" onclick="saveUsername()">Save</button>')
}

function saveUsername () {
    $("#username-input").remove();
    $("#save-button").remove();
    $("#username-text").text(localStorage.username)
    $("#username-text").show();
    $("#edit-button").show();
    var xhttp = new XMLHttpRequest();
    form = new FormData();
    form.append( 'username', localStorage.username );
    xhttp.open('POST', "user/updateUser", true);
    xhttp.send(form);
}

function handleInputChange () {
    localStorage['username'] = $("#username-input").val();
}

//Signup
$(function() {
    $("#country-input").autocomplete({
        source: countries
    });
});

// Graphs
function visitsChart() {
    const data = google.visualization.arrayToDataTable(visits);

    const options = {
        width: 500,
        height: 500,
        chart: {
            title: 'Visits',
            subtitle: 'All visits to the web page from the last 10 days',
        },
        legend: {
            position: 'none',
        },
        vAxis: {
          title: 'Number of visits',

        }
    };

    const chart = new google.charts.Bar(document.getElementById('visitsChart'));

    chart.draw(data, google.charts.Bar.convertOptions(options));
}

function downloadChart() {
    const data = google.visualization.arrayToDataTable(downloads)

    const options = {
        width: 500,
        height: 500,
        title: 'All our downloads by country'

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
        bar: { groupWidth: "90%" },
        //Se supone que esto cambia el rango max y min que quieres que se vea en la gráfica
        // como es horizontal, pues es el eje h
        hAxis: {
          viewWindow:{
              max:600,
              min:0
          }
        }

    };

    var chart = new google.charts.Bar(document.getElementById(`level${levelNumber}`));
    chart.draw(data, options);
}

function table () {
    var data = new google.visualization.arrayToDataTable(topscores);

    var table = new google.visualization.Table(document.getElementById('table_div'));
    table.draw(data, {showRowNumber: true, width: '500px', height: '500px'});
}

function lineChart () {
    var data = google.visualization.arrayToDataTable(sessions);

    var options = {
        width: 500,
        height: 500,
        title: 'Sessions duration  (s)',
        curveType: 'function',
        legend: { position: 'none' },
        vAxis: {
          title: 'Time spent in session (s)',
        }
    };

    var chart = new google.visualization.LineChart(document.getElementById('curve_chart'));

    chart.draw(data, options);
}