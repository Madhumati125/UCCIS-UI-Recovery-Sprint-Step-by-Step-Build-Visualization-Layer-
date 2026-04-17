// ---------------- MAP ----------------
let map = L.map('map').setView([19.0760, 72.8777], 10);

L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png')
.addTo(map);

let markers = [];

// ---------------- LOAD ZONES ----------------
function loadZones() {
    fetch("/zones")
    .then(res => res.json())
    .then(data => {

        document.getElementById("zoneSelect").innerHTML = "";

        let counts = {Green:0, Yellow:0, Red:0};

        markers.forEach(m => map.removeLayer(m));
        markers = [];

        data.zones.forEach(z => {

            counts[z.status]++;

            let lat = 19 + Math.random();
            let lng = 72 + Math.random();

            let marker = L.marker([lat, lng])
                .addTo(map)
                .bindPopup(`${z.name} - ${z.status} - Risk: ${z.risk}`);

            markers.push(marker);

            document.getElementById("zoneSelect").innerHTML +=
                `<option>${z.name}</option>`;
        });

        updateChart(counts);
    });
}

// ---------------- CHART ----------------
let chart;

function updateChart(counts) {
    if(chart) chart.destroy();

    chart = new Chart(document.getElementById("chart"), {
        type: 'bar',
        data: {
            labels: ["Green","Yellow","Red"],
            datasets: [{
                data: [counts.Green, counts.Yellow, counts.Red]
            }]
        }
    });
}

// ---------------- ACTION ----------------
function triggerAction(action) {
    let zone = document.getElementById("zoneSelect").value;

    fetch("/action", {
        method: "POST",
        headers: {"Content-Type":"application/json"},
        body: JSON.stringify({zone, action})
    })
    .then(res => res.json())
    .then(() => {
        loadZones();
        loadAlerts();
    });
}

// ---------------- ALERTS ----------------
function loadAlerts() {
    fetch("/alerts")
    .then(res => res.json())
    .then(data => {
        let html = "";

        data.forEach(a => {
            html += `<p>${a.zone} | ${a.action} | ${a.severity} | ${a.time}</p>`;
        });

        document.getElementById("alerts").innerHTML = html;
    });
}

// ---------------- MODE ----------------
function setMode(mode) {
    fetch("/mode", {
        method: "POST",
        headers: {"Content-Type":"application/json"},
        body: JSON.stringify({mode})
    });
}

// ---------------- AUTO REFRESH ----------------
setInterval(() => {
    loadZones();
    loadAlerts();
}, 3000);

// ✅ INITIAL LOAD
loadZones();
loadAlerts();