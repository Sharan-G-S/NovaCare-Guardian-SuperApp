document.addEventListener('DOMContentLoaded', () => {
    const btnSimulate = document.getElementById('btn-simulate');
    const tempDisplay = document.getElementById('temp-display');
    const transitDisplay = document.getElementById('transit-display');
    const transcriptBox = document.getElementById('transcript-box');
    const spinner = document.getElementById('loading-spinner');
    const aiResponseBox = document.getElementById('ai-response-box');
    const aiSummary = document.getElementById('ai-summary');
    const aiAction = document.getElementById('ai-action');
    const targetBed = document.getElementById('target-bed');
    const terminalLogs = document.getElementById('terminal-logs');
    const authList = document.getElementById('auth-list');

    // Chart.js Setup
    const ctx = document.getElementById('telemetryChart').getContext('2d');
    
    // Gradient for chart fill
    const gradient = ctx.createLinearGradient(0, 0, 0, 250);
    gradient.addColorStop(0, 'rgba(14, 165, 233, 0.5)');
    gradient.addColorStop(1, 'rgba(14, 165, 233, 0.0)');

    const warningGradient = ctx.createLinearGradient(0, 0, 0, 250);
    warningGradient.addColorStop(0, 'rgba(244, 63, 94, 0.6)');
    warningGradient.addColorStop(1, 'rgba(244, 63, 94, 0.05)');

    // Generate initial flat-ish data
    let initialData = [];
    let initialLabels = [];
    for(let i=0; i<30; i++) {
        initialLabels.push(i + "s");
        // Random float between 2.2 and 2.5
        initialData.push(2.2 + Math.random() * 0.3);
    }

    const telemetryChart = new Chart(ctx, {
        type: 'line',
        data: {
            labels: initialLabels,
            datasets: [{
                label: 'Core Cargo Temperature (°C)',
                data: initialData,
                borderColor: '#0ea5e9',
                backgroundColor: gradient,
                borderWidth: 2,
                pointRadius: 0,
                tension: 0.4,
                fill: true
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: { labels: { color: '#94a3b8' } }
            },
            scales: {
                y: {
                    min: 0,
                    max: 12,
                    grid: { color: 'rgba(255,255,255,0.05)' },
                    ticks: { color: '#64748b' }
                },
                x: {
                    grid: { display: false },
                    ticks: { color: '#64748b', maxTicksLimit: 6 }
                }
            },
            animation: {
                duration: 500
            }
        }
    });

    // Animate normal scrolling telemetry
    let chartInterval = setInterval(() => {
        if(btnSimulate.disabled) return; // Stop randomizing if simulation started
        
        telemetryChart.data.labels.push(""); 
        telemetryChart.data.datasets[0].data.push(2.2 + Math.random() * 0.3);
        
        // Remove oldest data point to keep array length at 30
        telemetryChart.data.labels.shift();
        telemetryChart.data.datasets[0].data.shift();
        
        telemetryChart.update();
        
        // Slightly update text to match trailing end
        let endVal = telemetryChart.data.datasets[0].data[29];
        tempDisplay.textContent = endVal.toFixed(1) + '°C';
    }, 1000);

    function logToTerminal(message, type = '') {
        const p = document.createElement('p');
        p.textContent = `> ${message}`;
        if (type) p.className = type;
        terminalLogs.appendChild(p);
        terminalLogs.scrollTop = terminalLogs.scrollHeight;
    }

    btnSimulate.addEventListener('click', async () => {
        // UI Reset & Loading State
        btnSimulate.disabled = true;
        spinner.classList.remove('hidden');
        aiResponseBox.classList.add('hidden');
        
        logToTerminal('Initiating Amazon Nova simulation...', 'highlight');
        logToTerminal('Ingesting telemetry & voice transcripts...', 'highlight');

        // Chart Spike Animation Array
        const spikeData = [3.1, 4.5, 6.2, 7.8, 8.9, 9.4, 9.6, 9.5];
        let spikeIndex = 0;

        let spikeInterval = setInterval(() => {
            if(spikeIndex >= spikeData.length) {
                clearInterval(spikeInterval);
                return;
            }
            
            let val = spikeData[spikeIndex];
            telemetryChart.data.labels.push(""); 
            telemetryChart.data.datasets[0].data.push(val);
            telemetryChart.data.labels.shift();
            telemetryChart.data.datasets[0].data.shift();

            if(val > 8.0) {
                telemetryChart.data.datasets[0].borderColor = '#f43f5e';
                telemetryChart.data.datasets[0].backgroundColor = warningGradient;
                tempDisplay.textContent = val.toFixed(1) + '°C';
                tempDisplay.classList.add('warning');
            } else {
                tempDisplay.textContent = val.toFixed(1) + '°C';
            }

            telemetryChart.update();
            spikeIndex++;
        }, 300);

        // Simulate real-time UI changes before API returns
        setTimeout(() => {
            transitDisplay.textContent = 'Compromised Route (Rerouting...)';
            transitDisplay.style.color = '#f43f5e';
            transcriptBox.style.borderColor = '#f59e0b';
            transcriptBox.innerHTML = `
                <p style="color:#ef4444; margin-bottom:8px;">[AUDIO TRANSCRIPT] "Control, the auxiliary AC compressor failed on the primary asset. Temp rising fast."</p>
                <p style="color:#f59e0b;">[VISUAL AUDIT] Nova Analysis: Image scan from depot confirms compromised door seal.</p>
            `;
        }, 1500);

        try {
            // Call the backend API
            const response = await fetch('/simulate', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' }
            });
            const data = await response.json();

            // Handle API Response
            spinner.classList.add('hidden');
            aiResponseBox.classList.remove('hidden');
            
            aiSummary.textContent = data.incident_summary;
            aiAction.textContent = "Action executed: " + data.recommended_action;
            btnSimulate.textContent = "Incident Handled Successfully";
            btnSimulate.style.background = 'var(--status-green)';

            // Orchestrate Cross-Logistics Action
            logToTerminal('Local Transport Reroute calculated by ColdChain Agent.', 'success');
            logToTerminal('Activating Hospital Administration Mesh-Network...', 'warning');
            
            setTimeout(() => {
                logToTerminal('BedManager Agent Activating on remote node...', 'highlight');
                targetBed.className = 'bed-cube reserved';
                targetBed.innerHTML = '104 (Reserved<br>Target Intake)';
                logToTerminal('Room 104 secured globally for inbound emergent patient.', 'success');
            }, 1200);

            setTimeout(() => {
                logToTerminal('PreAuth Agent executing autonomous claims bypass...', 'highlight');
                const li = document.createElement('li');
                li.innerHTML = '<span class="status-dot green" style="box-shadow:0 0 10px #10b981;"></span> Pt. Emergent - Bypass Auth Approved';
                li.style.border = '1px solid rgba(16, 185, 129, 0.4)';
                authList.prepend(li);
                logToTerminal('Insurance Bypass authorized via Nova compliance engine rules.', 'success');
            }, 2500);


        } catch (error) {
            console.error('Simulation Failed:', error);
            spinner.classList.add('hidden');
            btnSimulate.disabled = false;
            logToTerminal('System Error: Connection Refused', 'warning');
        }
    });
});
