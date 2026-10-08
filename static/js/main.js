let tempChart, vibChart, statusChart;

document.getElementById("analyzeBtn").addEventListener("click", async () => {
  const load = document.getElementById("load").value;
  const vibrations = Array.from(document.querySelectorAll("#vibrationInputs input")).map(i => i.value);

  if (!load || vibrations.some(v => v === "")) {
    alert("Please enter load and all 5 vibration values.");
    return;
  }

  const res = await fetch("/predict", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ load, vibrations })
  });

  const data = await res.json();
  const resultsDiv = document.getElementById("results");
  resultsDiv.innerHTML = "";

  data.predictions.forEach(p => {
    const statusColor =
      p.status === "Normal" ? "text-green-600" :
      p.status === "Warning" ? "text-yellow-600" :
      "text-red-600";

    const card = `
      <div class="p-4 bg-gray-50 border rounded-xl shadow-sm hover:shadow-md transition">
        <h3 class="font-semibold text-gray-700">Bearing ${p.bearing}</h3>
        <p class="text-sm text-gray-600 mt-1">Speed: <span class="font-medium text-gray-800">${p.speed} RPM</span></p>
        <p class="text-sm text-gray-600">Temperature: <span class="font-medium text-gray-800">${p.temperature} °C</span></p>
        <p class="text-sm mt-1 ${statusColor} font-medium">Status: ${p.status}</p>
      </div>`;
    resultsDiv.innerHTML += card;
  });

  const temps = data.predictions.map(p => p.temperature);
  const vibs = vibrations.map(v => parseFloat(v));

  const statusCounts = {
    Normal: data.predictions.filter(p => p.status === "Normal").length,
    Warning: data.predictions.filter(p => p.status === "Warning").length,
    Critical: data.predictions.filter(p => p.status === "Critical").length
  };

  if (tempChart) tempChart.destroy();
  if (vibChart) vibChart.destroy();
  if (statusChart) statusChart.destroy();

  tempChart = new Chart(document.getElementById("tempChart"), {
    type: "bar",
    data: {
      labels: ["B1", "B2", "B3", "B4", "B5"],
      datasets: [{
        label: "Temperature (°C)",
        data: temps
      }]
    },
    options: { maintainAspectRatio: false }
  });

  vibChart = new Chart(document.getElementById("vibChart"), {
    type: "bar",
    data: {
      labels: ["B1", "B2", "B3", "B4", "B5"],
      datasets: [{
        label: "Vibration (mm/s)",
        data: vibs
      }]
    },
    options: { maintainAspectRatio: false }
  });

  statusChart = new Chart(document.getElementById("statusChart"), {
    type: "pie",
    data: {
      labels: ["Normal", "Warning", "Critical"],
      datasets: [{
        data: [
          statusCounts.Normal,
          statusCounts.Warning,
          statusCounts.Critical
        ]
      }]
    },
    options: { maintainAspectRatio: false }
  });
});
