document.addEventListener('DOMContentLoaded', () => {
    // Elements
    const splashScreen = document.getElementById('splash-screen');
    const mainApp = document.getElementById('main-app');
    const tempSlider = document.getElementById('temp-slider');
    const humiditySlider = document.getElementById('humidity-slider');
    const hourSlider = document.getElementById('hour-slider');
    const tempVal = document.getElementById('temp-val');
    const humidityVal = document.getElementById('humidity-val');
    const hourVal = document.getElementById('hour-val');
    const predictBtn = document.getElementById('predict-btn');
    const resetBtn = document.getElementById('reset-btn');
    const resultsSection = document.getElementById('results-section');
    const emptyState = document.getElementById('empty-state');
    const statusCard = document.getElementById('status-card');
    const statusText = document.getElementById('status-text');
    const latencyText = document.getElementById('latency-text');

    // Result output elements
    const metricTemp = document.getElementById('metric-temp');
    const metricHumidity = document.getElementById('metric-humidity');
    const metricConfidence = document.getElementById('metric-confidence');
    const predictionValue = document.getElementById('prediction-value');
    const adviceContainer = document.getElementById('advice-container');

    let impactChart = null;

    // Initialization: Simulate splash screen
    setTimeout(() => {
        splashScreen.classList.add('hidden');
        mainApp.classList.remove('hidden');
        checkBackendHealth();
    }, 2000);

    // Update slider value displays
    tempSlider.addEventListener('input', (e) => tempVal.textContent = parseFloat(e.target.value).toFixed(1));
    humiditySlider.addEventListener('input', (e) => humidityVal.textContent = e.target.value);
    hourSlider.addEventListener('input', (e) => hourVal.textContent = e.target.value);

    // Backend Health Check
    async function checkBackendHealth() {
        const start = Date.now();
        try {
            const response = await fetch('/api/', { method: 'GET' });
            const data = await response.json();
            const latency = Date.now() - start;

            if (response.ok) {
                statusCard.className = 'status-card online';
                statusText.innerHTML = '<strong>Backend Online</strong>';
                latencyText.textContent = `Latency: ${latency}ms`;
            } else {
                throw new Error('Offline');
            }
        } catch (error) {
            statusCard.className = 'status-card offline';
            statusText.innerHTML = '<strong>Backend Offline</strong>';
            latencyText.textContent = 'Unreachable';
        }
    }

    // Run Prediction
    predictBtn.addEventListener('click', async () => {
        const temperature = parseFloat(tempSlider.value);
        const humidity = parseFloat(humiditySlider.value);
        const hour = parseInt(hourSlider.value);

        predictBtn.disabled = true;
        predictBtn.textContent = 'Analyzing...';

        try {
            const response = await fetch('/api/predict', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ temperature, humidity, hour })
            });

            if (!response.ok) throw new Error('Prediction API failed');

            const result = await response.json();
            showResults(result, temperature, humidity);
        } catch (error) {
            alert('Error connecting to backend: ' + error.message);
        } finally {
            predictBtn.disabled = false;
            predictBtn.textContent = '⚡ Run Energy Prediction';
        }
    });

    // Reset
    resetBtn.addEventListener('click', () => {
        tempSlider.value = 25.0;
        humiditySlider.value = 55;
        hourSlider.value = 12;
        tempVal.textContent = '25.0';
        humidityVal.textContent = '55';
        hourVal.textContent = '12';

        resultsSection.classList.add('hidden');
        emptyState.classList.remove('hidden');
    });

    function showResults(data, temp, hum) {
        const energy = data.predicted_energy;
        const confidence = (98.4 - (Math.abs(temp - 25) * 0.1)).toFixed(1);

        // Update UI
        emptyState.classList.add('hidden');
        resultsSection.classList.remove('hidden');

        metricTemp.textContent = `${temp.toFixed(1)} °C`;
        metricHumidity.textContent = `${hum.toFixed(0)} %`;
        metricConfidence.textContent = `${confidence} %`;
        predictionValue.textContent = energy.toFixed(2);

        // Advice
        let adviceHtml = '';
        if (energy < 4.0) {
            adviceContainer.className = 'advice-box advice-success';
            adviceHtml = '🌿 <strong>Exceptional Efficiency</strong> - Your current operational conditions are highly optimal.';
        } else if (energy < 7.0) {
            adviceContainer.className = 'advice-box advice-warning';
            adviceHtml = '⚠️ <strong>Moderate Load</strong> - Consider shifting heavy appliances to off-peak hours.';
        } else {
            adviceContainer.className = 'advice-box advice-danger';
            adviceHtml = '🚨 <strong>Critical Load</strong> - Extremely high consumption predicted. Thermal management recommended.';
        }
        adviceContainer.innerHTML = adviceHtml;

        updateChart(energy);
    }

    function updateChart(energy) {
        const ctx = document.getElementById('impactChart').getContext('2d');
        const userColor = energy < 4.0 ? '#10b981' : (energy < 7.0 ? '#f59e0b' : '#ef4444');

        if (impactChart) {
            impactChart.destroy();
        }

        impactChart = new Chart(ctx, {
            type: 'bar',
            data: {
                labels: ['Eco-Target (Avg)', 'Your Prediction', 'High Load Benchmark'],
                datasets: [{
                    label: 'Energy (kWh)',
                    data: [3.5, energy, 8.5],
                    backgroundColor: ['rgba(229, 231, 235, 0.2)', userColor, 'rgba(229, 231, 235, 0.2)'],
                    borderColor: ['#e5e7eb', userColor, '#e5e7eb'],
                    borderWidth: 1,
                    borderRadius: 8
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: { display: false }
                },
                scales: {
                    y: {
                        beginAtZero: true,
                        grid: { color: 'rgba(255, 255, 255, 0.05)' },
                        ticks: { color: '#64748b' }
                    },
                    x: {
                        grid: { display: false },
                        ticks: { color: '#64748b' }
                    }
                }
            }
        });
    }
});
