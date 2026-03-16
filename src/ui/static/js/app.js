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
        terminalLogs.innerHTML = '';
        
        logToTerminal('Initiating Amazon Nova simulation...');
        logToTerminal('Ingesting telemetry & voice transcripts...', 'highlight');

        // Simulate real-time UI changes before API returns
        setTimeout(() => {
            tempDisplay.textContent = '8.9°C';
            tempDisplay.classList.add('warning');
            transitDisplay.textContent = 'Compromised Route';
            transitDisplay.style.color = '#ef4444';
            transcriptBox.innerHTML = `
                <p style="color:#ef4444;">[VOICE] "The AC compressor failed on the primary truck. Temp rising fast."</p>
                <p style="color:#fbbf24;">[VISUAL] Image scan shows compromised door seal.</p>
            `;
        }, 1000);

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
            aiAction.textContent = "Action: " + data.recommended_action;
            btnSimulate.textContent = "Incident Handled";

            // Orchestrate Cross-Logistics Action
            logToTerminal('Macro-Logistics incident resolved. Triggering Micro-Logistics handoff...', 'highlight');
            
            setTimeout(() => {
                logToTerminal('BedManager Agent Activating...', 'highlight');
                targetBed.className = 'bed-cube reserved';
                targetBed.innerHTML = 'Bed 4 (Reserved<br>Emergency Intake)';
                logToTerminal('Bed 4 secured for emergency patient intake.', 'success');
            }, 800);

            setTimeout(() => {
                logToTerminal('PreAuth Agent Activating...', 'highlight');
                const li = document.createElement('li');
                li.innerHTML = '<span class="status-dot green"></span> Emergency Bypass - Auth Approved';
                authList.prepend(li);
                logToTerminal('Insurance Bypass authorized due to cold-chain reroute.', 'success');
            }, 1600);


        } catch (error) {
            console.error('Simulation Failed:', error);
            spinner.classList.add('hidden');
            btnSimulate.disabled = false;
            logToTerminal('System Error: Connection Refused', 'warning');
        }
    });
});
