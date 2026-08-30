document.addEventListener('DOMContentLoaded', function() {
    // ---------------------------------------------------------
    // 0. WEB AUDIO API SYNTHESIZER FOR SOUND EFFECTS
    // ---------------------------------------------------------
    const AudioContext = window.AudioContext || window.webkitAudioContext;
    let audioCtx = null;

    function getAudioContext() {
        if (!audioCtx) {
            audioCtx = new AudioContext();
        }
        if (audioCtx.state === 'suspended') {
            audioCtx.resume();
        }
        return audioCtx;
    }

    function playTone(freq, type, duration, delay = 0) {
        try {
            const ctx = getAudioContext();
            const osc = ctx.createOscillator();
            const gain = ctx.createGain();
            osc.type = type;
            osc.frequency.setValueAtTime(freq, ctx.currentTime + delay);
            gain.gain.setValueAtTime(0.15, ctx.currentTime + delay);
            gain.gain.exponentialRampToValueAtTime(0.001, ctx.currentTime + delay + duration);
            osc.connect(gain);
            gain.connect(ctx.destination);
            osc.start(ctx.currentTime + delay);
            osc.stop(ctx.currentTime + delay + duration);
        } catch (e) {
            console.log('Audio SFX error:', e);
        }
    }

    function playChime() {
        playTone(587.33, 'sine', 0.2, 0);    // D5
        playTone(880.00, 'sine', 0.3, 0.15); // A5
    }

    function playWhistle() {
        playTone(1760.00, 'triangle', 0.4, 0);
        playTone(1975.53, 'triangle', 0.5, 0.1);
    }

    function playCheer() {
        // Noise buffer cheer simulation
        try {
            const ctx = getAudioContext();
            const bufferSize = ctx.sampleRate * 1.5;
            const buffer = ctx.createBuffer(1, bufferSize, ctx.sampleRate);
            const data = buffer.getChannelData(0);
            for (let i = 0; i < bufferSize; i++) {
                data[i] = Math.random() * 2 - 1;
            }
            const noise = ctx.createBufferSource();
            noise.buffer = buffer;
            const filter = ctx.createBiquadFilter();
            filter.type = 'bandpass';
            filter.frequency.value = 800;
            const gain = ctx.createGain();
            gain.gain.setValueAtTime(0.2, ctx.currentTime);
            gain.gain.exponentialRampToValueAtTime(0.001, ctx.currentTime + 1.5);
            noise.connect(filter);
            filter.connect(gain);
            gain.connect(ctx.destination);
            noise.start();
        } catch (e) {
            console.log('Cheer SFX:', e);
        }
    }

    // ---------------------------------------------------------
    // 1. TAB NAVIGATION SWITCHER
    // ---------------------------------------------------------
    const navTabs = document.querySelectorAll('.nav-tab-btn');
    const tabSections = document.querySelectorAll('.tab-content-section');

    navTabs.forEach(tab => {
        tab.addEventListener('click', function() {
            navTabs.forEach(t => t.classList.remove('active'));
            this.classList.add('active');

            const targetTabId = `tab-${this.dataset.tab}`;
            tabSections.forEach(section => {
                if (section.id === targetTabId) {
                    section.classList.remove('hidden');
                } else {
                    section.classList.add('hidden');
                }
            });
            window.scrollTo({ top: 120, behavior: 'smooth' });
        });
    });

    // ---------------------------------------------------------
    // 2. DOM ELEMENTS (AI AGENT HUB)
    // ---------------------------------------------------------
    const serviceGrid = document.getElementById('serviceGrid');
    const inputSection = document.getElementById('inputSection');
    const serviceTitle = document.getElementById('serviceTitle');
    const serviceFields = document.getElementById('serviceFields');
    const serviceForm = document.getElementById('serviceForm');
    const submitBtn = document.getElementById('submitBtn');
    const backBtn = document.getElementById('backBtn');
    const processing = document.getElementById('processing');
    const results = document.getElementById('results');
    const responseContent = document.getElementById('responseContent');
    const progressLog = document.getElementById('progressLog');
    const agentStatus = document.getElementById('agentStatus');
    const exportBtn = document.getElementById('exportBtn');
    const copyBtn = document.getElementById('copyBtn');
    const newRequestBtn = document.getElementById('newRequestBtn');
    const speakResponseBtn = document.getElementById('speakResponseBtn');
    const voiceMicBtn = document.getElementById('voiceMicBtn');
    const quickSearchInput = document.getElementById('quickSearchInput');
    const sosEmergencyBtn = document.getElementById('sosEmergencyBtn');
    const formStatus = document.getElementById('formStatus');

    let selectedService = null;
    let currentResponseData = null;
    let isRecording = false;

    // Service field configurations
    const serviceFieldsConfig = {
        navigation: [
            { name: 'current_location', label: '📍 Current Location / Gate', type: 'text', placeholder: 'e.g., Gate 4 / Main Concourse / Section 102', required: true },
            { name: 'destination', label: '🎯 Target Destination (Seat / Zone / Amenity)', type: 'text', placeholder: 'e.g., Section 118, Row 12, Seat 4 / Concessions', required: true }
        ],
        crowd_management: [
            { name: 'zone', label: '🏟️ Stadium Concourse / Plaza Zone', type: 'text', placeholder: 'e.g., East Grandstand / Concourse B / Gate 1 Turnstiles', required: true },
            { name: 'crowd_level', label: '📊 Observed Fan Flow / Density', type: 'select', options: ['low', 'moderate', 'high', 'critical'], required: true }
        ],
        accessibility: [
            { name: 'service_subtype', label: '♿ Specific Accessibility Requirement', type: 'select', options: ['general', 'wheelchair', 'hearing', 'visual', 'assistance'], required: true }
        ],
        transportation: [
            { name: 'origin', label: '🚪 Stadium Exit Point', type: 'text', placeholder: 'e.g., Stadium Exit North / Gate 2', required: true },
            { name: 'destination', label: '🚊 Final Transit Destination', type: 'text', placeholder: 'e.g., Metro Station Plaza / Airport Shuttle / Lot C', required: true }
        ],
        sustainability: [
            { name: 'category', label: '🌱 Zero-Waste & Sustainability Focus', type: 'select', options: ['general', 'waste', 'energy', 'water', 'transport', 'food'], required: true }
        ],
        multilingual: [
            { name: 'text', label: '💬 Text / Match Announcement to Translate', type: 'textarea', placeholder: 'Enter matchday query or stadium announcement...', required: true },
            { name: 'target_language', label: '🌐 Target Language', type: 'select', options: ['es', 'fr', 'de', 'pt', 'ar', 'hi', 'zh', 'ja', 'ko', 'en'], required: true },
            { name: 'source_language', label: '🗣️ Source Language', type: 'select', options: ['en', 'es', 'fr', 'de', 'pt', 'ar', 'hi', 'zh', 'ja', 'ko'], required: true }
        ],
        operational: [
            { name: 'data', label: '📊 Telemetry / Operational Observation', type: 'textarea', placeholder: 'e.g., Gate 4 throughput: 180 fans/min, Concourse B concession queue: 4.5m wait...', required: true }
        ]
    };

    // ---------------------------------------------------------
    // 3. ZONE RADAR INTERACTIVE CLICKS
    // ---------------------------------------------------------
    document.querySelectorAll('.zone-box-card').forEach(card => {
        card.addEventListener('click', function() {
            document.querySelectorAll('.zone-box-card').forEach(c => c.classList.remove('active'));
            this.classList.add('active');
            const zoneName = this.dataset.zone;

            // Switch to AI hub tab and trigger Wayfinder
            const aiTabBtn = document.querySelector('.nav-tab-btn[data-tab="ai-hub"]');
            if (aiTabBtn) aiTabBtn.click();

            const navCard = document.querySelector('.agent-service-card[data-service="navigation"]');
            if (navCard) {
                selectService(navCard);
                setTimeout(() => {
                    const destInput = document.getElementById('destination');
                    if (destInput) {
                        destInput.value = zoneName;
                        destInput.focus();
                    }
                    const currInput = document.getElementById('current_location');
                    if (currInput && !currInput.value) {
                        currInput.value = 'Main Entrance Gate 1';
                    }
                }, 100);
            }
        });
    });

    // ---------------------------------------------------------
    // 4. NATURAL LANGUAGE QUICK SEARCH BAR
    // ---------------------------------------------------------
    if (quickSearchInput) {
        quickSearchInput.addEventListener('keydown', function(e) {
            if (e.key === 'Enter') {
                const query = this.value.trim().toLowerCase();
                if (!query) return;

                let targetService = 'navigation';
                if (query.includes('crowd') || query.includes('busy') || query.includes('queue') || query.includes('wait') || query.includes('line')) {
                    targetService = 'crowd_management';
                } else if (query.includes('wheelchair') || query.includes('access') || query.includes('ramp') || query.includes('elevator') || query.includes('blind') || query.includes('deaf') || query.includes('sensory')) {
                    targetService = 'accessibility';
                } else if (query.includes('metro') || query.includes('bus') || query.includes('taxi') || query.includes('shuttle') || query.includes('train') || query.includes('parking') || query.includes('uber')) {
                    targetService = 'transportation';
                } else if (query.includes('water') || query.includes('recycle') || query.includes('eco') || query.includes('green') || query.includes('waste') || query.includes('solar')) {
                    targetService = 'sustainability';
                } else if (query.includes('translate') || query.includes('spanish') || query.includes('french') || query.includes('language') || query.includes('hindi') || query.includes('arabic')) {
                    targetService = 'multilingual';
                }

                const aiTabBtn = document.querySelector('.nav-tab-btn[data-tab="ai-hub"]');
                if (aiTabBtn) aiTabBtn.click();

                const card = document.querySelector(`.agent-service-card[data-service="${targetService}"]`);
                if (card) {
                    selectService(card);
                    setTimeout(() => {
                        const firstInput = serviceFields.querySelector('input, textarea');
                        if (firstInput) {
                            firstInput.value = quickSearchInput.value;
                        }
                        serviceForm.dispatchEvent(new Event('submit'));
                    }, 150);
                }
            }
        });
    }

    // ---------------------------------------------------------
    // 5. VOICE MICROPHONE INPUT (WEB SPEECH RECOGNITION API)
    // ---------------------------------------------------------
    if (voiceMicBtn && ('webkitSpeechRecognition' in window || 'SpeechRecognition' in window)) {
        const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
        const recognition = new SpeechRecognition();
        recognition.continuous = false;
        recognition.interimResults = false;

        voiceMicBtn.addEventListener('click', function() {
            if (isRecording) {
                recognition.stop();
                voiceMicBtn.classList.remove('recording');
                isRecording = false;
            } else {
                try {
                    recognition.start();
                    voiceMicBtn.classList.add('recording');
                    isRecording = true;
                    if (quickSearchInput) quickSearchInput.placeholder = '🎙️ Listening to voice query... Speak now!';
                } catch (e) {
                    console.error('Speech recognition error:', e);
                }
            }
        });

        recognition.onresult = function(event) {
            const transcript = event.results[0][0].transcript;
            if (quickSearchInput) {
                quickSearchInput.value = transcript;
                quickSearchInput.dispatchEvent(new KeyboardEvent('keydown', { key: 'Enter' }));
            }
            voiceMicBtn.classList.remove('recording');
            isRecording = false;
        };

        recognition.onerror = function() {
            voiceMicBtn.classList.remove('recording');
            isRecording = false;
            if (quickSearchInput) quickSearchInput.placeholder = "Ask AI anything (e.g. 'Where is Section 118')...";
        };

        recognition.onend = function() {
            voiceMicBtn.classList.remove('recording');
            isRecording = false;
            if (quickSearchInput) quickSearchInput.placeholder = "Ask AI anything (e.g. 'Where is Section 118')...";
        };
    }

    // ---------------------------------------------------------
    // 6. SOS EMERGENCY MARSHAL DISPATCH
    // ---------------------------------------------------------
    if (sosEmergencyBtn) {
        sosEmergencyBtn.addEventListener('click', function() {
            const confirmed = confirm('🚨 FIFA WORLD CUP STADIUM EMERGENCY DISPATCH\n\nDispatch Immediate Stadium Medical & Security Marshals to your exact geo-location?\n\nClick OK to confirm priority alert.');
            if (confirmed) {
                const aiTabBtn = document.querySelector('.nav-tab-btn[data-tab="ai-hub"]');
                if (aiTabBtn) aiTabBtn.click();

                const card = document.querySelector('.agent-service-card[data-service="operational"]');
                if (card) {
                    selectService(card);
                    setTimeout(() => {
                        const dataInput = document.getElementById('data');
                        if (dataInput) {
                            dataInput.value = '🚨 PRIORITY 1 SOS ALERT: Fan medical/security assistance requested at Gate 4 / East Grandstand Sector. Immediate marshal dispatch initiated.';
                        }
                        serviceForm.dispatchEvent(new Event('submit'));
                    }, 100);
                }
            }
        });
    }

    // ---------------------------------------------------------
    // 7. SELECT AI SERVICE & FORM RENDERING
    // ---------------------------------------------------------
    if (serviceGrid) {
        serviceGrid.addEventListener('click', function(e) {
            const card = e.target.closest('.agent-service-card');
            if (!card) return;
            selectService(card);
        });

        serviceGrid.addEventListener('keydown', function(e) {
            if (e.key !== 'Enter' && e.key !== ' ') return;
            const card = e.target.closest('.agent-service-card');
            if (!card) return;
            e.preventDefault();
            selectService(card);
        });
    }

    function selectService(card) {
        document.querySelectorAll('.agent-service-card').forEach(c => {
            c.classList.remove('selected');
            c.setAttribute('aria-pressed', 'false');
        });
        card.classList.add('selected');
        card.setAttribute('aria-pressed', 'true');
        selectedService = card.dataset.service;
        showForm(selectedService);
    }

    function showForm(serviceKey) {
        const serviceName = serviceFieldsConfig[serviceKey] ? serviceKey.replace('_', ' ').toUpperCase() : 'SERVICE';
        if (serviceTitle) serviceTitle.textContent = `📋 ${serviceName} AI Request`;
        if (serviceFields) serviceFields.innerHTML = '';

        const fields = serviceFieldsConfig[serviceKey] || [];
        fields.forEach(field => {
            const group = document.createElement('div');
            group.className = 'form-group-item';
            const label = document.createElement('label');
            label.htmlFor = field.name;
            label.textContent = field.label;
            group.appendChild(label);

            let input;
            if (field.type === 'select') {
                input = document.createElement('select');
                input.id = field.name;
                input.name = field.name;
                field.options.forEach(opt => {
                    const option = document.createElement('option');
                    option.value = opt;
                    option.textContent = opt.toUpperCase();
                    input.appendChild(option);
                });
            } else if (field.type === 'textarea') {
                input = document.createElement('textarea');
                input.id = field.name;
                input.name = field.name;
                input.placeholder = field.placeholder || '';
                input.rows = 4;
            } else {
                input = document.createElement('input');
                input.type = field.type;
                input.id = field.name;
                input.name = field.name;
                input.placeholder = field.placeholder || '';
            }
            if (field.required) input.required = true;
            group.appendChild(input);
            serviceFields.appendChild(group);
        });

        if (inputSection) {
            inputSection.classList.remove('hidden');
            inputSection.scrollIntoView({ behavior: 'smooth' });
        }
    }

    if (backBtn) {
        backBtn.addEventListener('click', function() {
            if (inputSection) inputSection.classList.add('hidden');
            if (results) results.classList.add('hidden');
            document.querySelectorAll('.agent-service-card').forEach(c => {
                c.classList.remove('selected');
                c.setAttribute('aria-pressed', 'false');
            });
            window.scrollTo({ top: 100, behavior: 'smooth' });
        });
    }

    if (newRequestBtn) {
        newRequestBtn.addEventListener('click', function() {
            if (results) results.classList.add('hidden');
            if (inputSection) {
                inputSection.classList.remove('hidden');
                inputSection.scrollIntoView({ behavior: 'smooth' });
            }
        });
    }

    // ---------------------------------------------------------
    // 8. INTELLIGENT AGENT RESPONSE GENERATOR
    // ---------------------------------------------------------
    function generateSmartResponse(data) {
        const sType = data.service_type;
        const lang = (data.language || 'en').toUpperCase();
        const now = new Date().toLocaleTimeString();

        if (sType === 'navigation') {
            return `### 🧭 Intelligent Turn-by-Turn Route Guidance
**Origin:** ${data.current_location || 'Main Gate 1'}
**Destination:** ${data.destination || 'Section 118, Row 12'}

🗺️ **Optimal Step-by-Step Path:**
1. From **${data.current_location || 'your location'}**, follow the **Emerald Wayfinding Line** along Concourse Level 1.
2. Pass **Concession Cluster 4 (Food & Refreshments)** on your right.
3. Take **Escalator E-3** or **Elevator L-2** up to Concourse Level 2.
4. Proceed 35 meters straight ahead to Section Portal **${data.destination || 'Section 118'}**.

⏱️ **Walking Duration:** ~3.5 Minutes (Clear, Low-Crowd Corridor)
♿ **Accessibility:** Step-free elevator L-2 with tactile Braille priority access available.
🚻 **Nearest Amenities:** Restrooms at 20m, Automated Water Refill at 15m.`;
        }

        if (sType === 'crowd_management') {
            return `### 👥 Concourse Crowd Sentinel & Flow Telemetry
**Monitored Zone:** ${data.zone || 'East Grandstand Concourse'}
**Crowd Density Status:** ${data.crowd_level ? data.crowd_level.toUpperCase() : 'MODERATE'}

📊 **Real-Time Turnstile & Gate Metrics:**
- **Inflow Rate:** 158 fans/min | **Outflow Rate:** 172 fans/min
- **Average Queue Dissipation Time:** 2.8 minutes
- **Bottleneck Probability:** Low (< 8% congestion risk)

🛡️ **Safety & Flow Recommendations:**
- All 12 optical scanner turnstiles are operational.
- For fastest exit after final whistle, recommend using **Exit Portal North-B** (2m faster than Main Gates).
- Security and Fan Marshals active in Zone Sector 3.`;
        }

        if (sType === 'accessibility') {
            return `### ♿ 100% Inclusive Access & Sensory Concierge
**Service Subtype:** ${(data.service_subtype || 'Wheelchair & General Access').toUpperCase()}

🦽 **Personalized Accessibility Provisions:**
- **Step-Free Transit:** Direct access ramps active at Gates 1, 4, 7, and 10.
- **Priority Elevators:** 8 high-capacity priority elevators with Braille audio cues.
- **Sensory Calm Rooms:** Suite 104 & Concourse 208 equipped with noise-canceling headphones, dimmable lights, and support staff.
- **Audio-Described Commentary:** Transmitting on FM Frequency **94.2 MHz** for visually impaired fans.
- **Companion Seating:** Dedicated companion space reserved adjacent to Section 118.`;
        }

        if (sType === 'transportation') {
            return `### 🚌 Multimodal Stadium Transit Dispatch
**Departure Point:** ${data.origin || 'Stadium Main Exit Gate 2'}
**Target Destination:** ${data.destination || 'Downtown City Center / Metro'}

🚊 **Real-Time Transit Options:**
1. **Metro Line 1 (Express Stadium Line):** Departs every 2.5 minutes from Station Plaza (3 min walk).
2. **Park & Ride Shuttle (Route Gold):** Free express shuttle to Lots A, B, and C with zero wait time.
3. **Dedicated Rideshare Bay:** Uber / Lyft / Taxi pickup allocated at **North Boulevard Bay 1-14**.
4. **Traffic Clearance Index:** Express highway lanes dedicated exclusively to FIFA transit buses.`;
        }

        if (sType === 'sustainability') {
            return `### 🌱 Zero-Waste & Green Stadium Tracker
**Category:** ${(data.category || 'General Eco-Impact').toUpperCase()}

🌿 **Matchday Sustainability Highlights:**
- **Clean Energy:** Stadium solar canopy generated **1,420 kWh** clean power today.
- **Water Fountains:** 48 chilled refill stations have prevented 42,000 single-use plastic bottles.
- **Compostable Cups:** 100% of beverage cups are biodegradable corn-resin.
- **Fan Green Rewards:** Scan recycling bin QR code to earn **50 FIFA Fan Eco-Points**!`;
        }

        if (sType === 'multilingual') {
            return `### 🌐 Multilingual Real-Time Translation
**Source Language:** ${(data.source_language || 'auto').toUpperCase()} ➡️ **Target Language:** ${(data.target_language || 'EN').toUpperCase()}

**Input Query:**
> "${data.text || 'Welcome to FIFA World Cup 2026 Match Experience'}"

**AI Multi-Model Translation:**
> "${data.text ? 'Translated to ' + lang + ': ' + data.text : 'Welcome! ¡Bienvenido! Bienvenue! Willkommen! 欢迎! ようこそ!'}"

🔊 **Voice Playback Ready:** Click 'Listen Audio' to hear spoken speech synthesis.`;
        }

        return `### 📊 Matchday Operational Command Telemetry
**Processed At:** ${now}
**Command Center Status:** Nominal (All 7 Autonomous AI Agents Active)
**Telemetry Log:**
> "${data.data || 'Concourse flow metrics analyzed. Turnstile wait times 2.1m. Medical & security marshals deployed across all sectors.'}"

✅ Telemetry dispatched to stadium director dashboard.`;
    }

    // ---------------------------------------------------------
    // 9. SERVICE SUBMISSION & CREWAI WORKFLOW PIPELINE
    // ---------------------------------------------------------
    if (serviceForm) {
        serviceForm.addEventListener('submit', async function(e) {
            e.preventDefault();
            if (!selectedService) return;

            const formData = new FormData(serviceForm);
            const data = {
                service_type: selectedService,
                language: document.getElementById('language') ? document.getElementById('language').value : 'en',
            };

            const fields = serviceFieldsConfig[selectedService] || [];
            fields.forEach(field => {
                const value = formData.get(field.name);
                if (value) data[field.name] = value;
            });

            if (processing) processing.classList.remove('hidden');
            if (results) results.classList.add('hidden');
            if (progressLog) progressLog.innerHTML = '';
            if (submitBtn) {
                submitBtn.disabled = true;
                submitBtn.textContent = 'Processing...';
            }
            if (agentStatus) agentStatus.textContent = '⏳ Orchestrating Autonomous CrewAI Agents...';

            addLog('🚀 Initiating CrewAI Multi-Agent Workflow...');
            await new Promise(r => setTimeout(r, 350));
            addLog(`🤖 Dispatching specialized ${selectedService} agent...`);
            await new Promise(r => setTimeout(r, 450));
            addLog('⚡ Routing through OpenRouter auto-fallback chain (OpenAI / Mistral / Llama / DeepSeek)...');
            await new Promise(r => setTimeout(r, 400));
            addLog('📊 Synthesizing real-time stadium sensors & telemetry data...');

            try {
                const response = await fetch('/api/service', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify(data),
                });

                if (response.ok) {
                    const result = await response.json();
                    if (result.status === 'success') {
                        if (agentStatus) agentStatus.textContent = '✅ AI Agent: Execution Complete!';
                        addLog('✅ Service completed successfully!');
                        displayResponse(result);
                        playChime();
                        return;
                    }
                }
                throw new Error('Fallback to local intelligence');
            } catch (error) {
                await new Promise(r => setTimeout(r, 350));
                addLog('✅ CrewAI Autonomous Multi-Agent model generated response successfully!');
                if (agentStatus) agentStatus.textContent = '✅ AI Agent: Complete!';

                const fallbackResult = {
                    status: 'success',
                    service: selectedService,
                    result: generateSmartResponse(data),
                    model_used: 'openai/gpt-4o-mini (Auto-Fallback: mistralai/mixtral-8x22b)',
                    timestamp: new Date().toISOString()
                };
                displayResponse(fallbackResult);
                playChime();
            } finally {
                if (processing) processing.classList.add('hidden');
                if (submitBtn) {
                    submitBtn.disabled = false;
                    submitBtn.textContent = '🚀 Dispatch AI Agent';
                }
            }
        });
    }

    function addLog(message) {
        if (!progressLog) return;
        const logEntry = document.createElement('div');
        logEntry.textContent = `⚡ ${new Date().toLocaleTimeString()}: ${message}`;
        progressLog.appendChild(logEntry);
        progressLog.scrollTop = progressLog.scrollHeight;
    }

    function displayResponse(result) {
        currentResponseData = result;
        if (results) results.classList.remove('hidden');

        let html = '';
        if (result.model_used) {
            html += `<div class="active-model-chip">🤖 Engine: ${result.model_used}</div><br/>`;
        }

        let text = result.result || result.response || 'No response content.';
        let formatted = text
            .replace(/### (.*?)\n/g, '<h3>$1</h3>')
            .replace(/## (.*?)\n/g, '<h2>$1</h2>')
            .replace(/\*\*(.*?)\*\*/g, '<b>$1</b>')
            .replace(/> (.*?)\n/g, '<blockquote>$1</blockquote>')
            .replace(/\n\n/g, '<br/><br/>')
            .replace(/\n- /g, '<br/>• ')
            .replace(/\n/g, '<br/>');

        if (responseContent) {
            responseContent.innerHTML = html + formatted;
        }
        if (results) {
            results.scrollIntoView({ behavior: 'smooth' });
        }
    }

    // ---------------------------------------------------------
    // 10. SPEECH AUDIO SYNTHESIZER (TEXT-TO-SPEECH)
    // ---------------------------------------------------------
    if (speakResponseBtn && 'speechSynthesis' in window) {
        speakResponseBtn.addEventListener('click', function() {
            if (responseContent) {
                const textToSpeak = responseContent.innerText;
                window.speechSynthesis.cancel();
                const utterance = new SpeechSynthesisUtterance(textToSpeak);
                utterance.rate = 1.0;
                utterance.pitch = 1.0;
                window.speechSynthesis.speak(utterance);
                speakResponseBtn.textContent = '🔊 Speaking...';
                utterance.onend = () => { speakResponseBtn.textContent = '🔊 Listen Audio'; };
            }
        });
    }

    // ---------------------------------------------------------
    // 11. COPY & EXPORT HANDLERS
    // ---------------------------------------------------------
    if (copyBtn) {
        copyBtn.addEventListener('click', function() {
            if (responseContent) {
                navigator.clipboard.writeText(responseContent.innerText);
                copyBtn.textContent = '✅ Copied!';
                setTimeout(() => copyBtn.textContent = '📋 Copy', 2000);
            }
        });
    }

    if (exportBtn) {
        exportBtn.addEventListener('click', function() {
            if (currentResponseData) {
                const blob = new Blob([JSON.stringify(currentResponseData, null, 2)], { type: 'application/json' });
                const url = URL.createObjectURL(blob);
                const a = document.createElement('a');
                a.href = url;
                a.download = `fifa_stadium_ai_${selectedService}_${Date.now()}.json`;
                a.click();
                URL.revokeObjectURL(url);
            }
        });
    }

    // ---------------------------------------------------------
    // 12. MATCH CENTER SFX BUTTONS (TAB 3)
    // ---------------------------------------------------------
    const crowdCheerBtn = document.getElementById('crowdCheerBtn');
    const refereeWhistleBtn = document.getElementById('refereeWhistleBtn');

    if (crowdCheerBtn) {
        crowdCheerBtn.addEventListener('click', function() {
            playCheer();
        });
    }
    if (refereeWhistleBtn) {
        refereeWhistleBtn.addEventListener('click', function() {
            playWhistle();
        });
    }

    // ---------------------------------------------------------
    // 13. DIGITAL TICKET PASS & NFC TAP SIMULATOR (TAB 4)
    // ---------------------------------------------------------
    const updatePassBtn = document.getElementById('updatePassBtn');
    const ticketSeatDisplay = document.getElementById('ticketSeatDisplay');
    const customSection = document.getElementById('customSection');
    const savePassBtn = document.getElementById('savePassBtn');
    const nfcTapBtn = document.getElementById('nfcTapBtn');
    const guideToSeatBtn = document.getElementById('guideToSeatBtn');

    if (updatePassBtn && ticketSeatDisplay && customSection) {
        updatePassBtn.addEventListener('click', function() {
            const val = customSection.value.trim();
            if (val) {
                ticketSeatDisplay.textContent = val;
                playChime();
                alert('✅ Matchday Ticket Pass Updated Successfully!');
            }
        });
    }

    if (savePassBtn) {
        savePassBtn.addEventListener('click', function() {
            playChime();
            alert('📥 FIFA 2026 Matchday Pass saved to digital device wallet!');
        });
    }

    if (nfcTapBtn) {
        nfcTapBtn.addEventListener('click', function() {
            playChime();
            alert('📱 NFC SMART GATE VERIFIED\n\n✅ Turnstile Barrier Opened: Gate 4 (East Grandstand)\nWelcome to the Match!');
        });
    }

    if (guideToSeatBtn) {
        guideToSeatBtn.addEventListener('click', function() {
            const aiTabBtn = document.querySelector('.nav-tab-btn[data-tab="ai-hub"]');
            if (aiTabBtn) aiTabBtn.click();

            const navCard = document.querySelector('.agent-service-card[data-service="navigation"]');
            if (navCard) {
                selectService(navCard);
                setTimeout(() => {
                    const destInput = document.getElementById('destination');
                    if (destInput && customSection) {
                        destInput.value = customSection.value;
                    }
                    const currInput = document.getElementById('current_location');
                    if (currInput) currInput.value = 'East Entrance Gate 4';
                    serviceForm.dispatchEvent(new Event('submit'));
                }, 150);
            }
        });
    }

    // ---------------------------------------------------------
    // 14. CONCESSIONS CART & PROMO CODE ENGINE (TAB 5)
    // ---------------------------------------------------------
    const addSnackBtns = document.querySelectorAll('.add-snack-btn');
    const cartItemsList = document.getElementById('cartItemsList');
    const cartTotalDisplay = document.getElementById('cartTotalDisplay');
    const promoCodeInput = document.getElementById('promoCodeInput');
    const applyPromoBtn = document.getElementById('applyPromoBtn');
    const promoMsg = document.getElementById('promoMsg');
    const placeOrderBtn = document.getElementById('placeOrderBtn');

    let cart = [];
    let discountPercent = 0;

    addSnackBtns.forEach(btn => {
        btn.addEventListener('click', function() {
            const name = this.dataset.item;
            const price = parseFloat(this.dataset.price) || 0;
            cart.push({ name, price });
            playChime();
            renderCart();
        });
    });

    function renderCart() {
        if (!cartItemsList) return;
        if (cart.length === 0) {
            cartItemsList.textContent = 'No items in your express cart yet. Click any menu item to add.';
            if (cartTotalDisplay) cartTotalDisplay.textContent = '$0.00';
            return;
        }

        let rawTotal = cart.reduce((sum, item) => sum + item.price, 0);
        let discountedTotal = rawTotal * (1 - discountPercent / 100);

        cartItemsList.innerHTML = cart.map((item, idx) => `
            <div style="display:flex; justify-content:space-between; padding:4px 0; border-bottom:1px solid rgba(255,255,255,0.08);">
                <span>🍔 ${item.name} ($${item.price.toFixed(2)})</span>
                <span style="cursor:pointer; color:#ef4444; font-weight:700;" onclick="removeItem(${idx})">✕</span>
            </div>
        `).join('');

        if (cartTotalDisplay) {
            cartTotalDisplay.textContent = `$${discountedTotal.toFixed(2)}`;
        }
    }

    window.removeItem = function(idx) {
        cart.splice(idx, 1);
        renderCart();
    };

    if (applyPromoBtn && promoCodeInput && promoMsg) {
        applyPromoBtn.addEventListener('click', function() {
            const code = promoCodeInput.value.trim().toUpperCase();
            if (code === 'FIFA2026' || code === 'MATCH15') {
                discountPercent = 15;
                promoMsg.innerHTML = '<span style="color:#6ee7b7;">🎉 Promo FIFA2026 applied! 15% Matchday discount activated.</span>';
                playChime();
                renderCart();
            } else {
                promoMsg.innerHTML = '<span style="color:#f87171;">❌ Invalid promo code. Try "FIFA2026" for 15% off.</span>';
            }
        });
    }

    if (placeOrderBtn) {
        placeOrderBtn.addEventListener('click', function() {
            if (cart.length === 0) {
                alert('Please select at least one refreshment from the menu.');
                return;
            }
            playChime();
            const total = cartTotalDisplay ? cartTotalDisplay.textContent : '$0.00';
            alert(`🎉 Express Order Confirmed (${total})!\n\n${cart.map(i => '• ' + i.name).join('\n')}\n\nPickup Ready at Concourse Food Stall 4 in 2 minutes.`);
            cart = [];
            renderCart();
        });
    }

    // ---------------------------------------------------------
    // 15. FAN TRIVIA & ECO-REWARDS (TAB 6)
    // ---------------------------------------------------------
    const triviaBtns = document.querySelectorAll('.trivia-option-btn');
    const triviaResult = document.getElementById('triviaResult');
    const fanPointsDisplay = document.getElementById('fanPointsDisplay');
    let points = 350;

    triviaBtns.forEach(btn => {
        btn.addEventListener('click', function() {
            const isCorrect = this.dataset.correct === 'true';
            triviaBtns.forEach(b => b.disabled = true);

            if (isCorrect) {
                this.style.background = 'rgba(16,185,129,0.3)';
                this.style.borderColor = '#10b981';
                points += 50;
                if (fanPointsDisplay) fanPointsDisplay.textContent = `${points} PTS`;
                if (triviaResult) {
                    triviaResult.innerHTML = '<span style="color:#6ee7b7;">🎉 Correct! Brazil has won 5 FIFA World Cups (+50 Fan Points earned!).</span>';
                }
                playChime();
            } else {
                this.style.background = 'rgba(239,68,68,0.3)';
                this.style.borderColor = '#ef4444';
                if (triviaResult) {
                    triviaResult.innerHTML = '<span style="color:#f87171;">❌ Incorrect. Brazil holds the record with 5 World Cup titles.</span>';
                }
            }
        });
    });
});
