document.addEventListener('DOMContentLoaded', function() {
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

    let selectedService = null;

    // Service field configurations
    const serviceFieldsConfig = {
        navigation: [
            { name: 'current_location', label: 'Current Location', type: 'text', placeholder: 'e.g., Main Entrance', required: true },
            { name: 'destination', label: 'Destination', type: 'text', placeholder: 'e.g., Section A, Row 10', required: true }
        ],
        crowd_management: [
            { name: 'zone', label: 'Zone', type: 'text', placeholder: 'e.g., Main Concourse', required: true },
            { name: 'crowd_level', label: 'Crowd Level', type: 'select', options: ['low', 'moderate', 'high', 'critical'], required: true }
        ],
        accessibility: [
            { name: 'service_subtype', label: 'Service Type', type: 'select', options: ['general', 'wheelchair', 'hearing', 'visual', 'assistance'], required: true }
        ],
        transportation: [
            { name: 'origin', label: 'Origin', type: 'text', placeholder: 'e.g., Stadium', required: true },
            { name: 'destination', label: 'Destination', type: 'text', placeholder: 'e.g., City Center', required: true }
        ],
        sustainability: [
            { name: 'category', label: 'Category', type: 'select', options: ['general', 'waste', 'energy', 'water', 'transport', 'food'], required: true }
        ],
        multilingual: [
            { name: 'text', label: 'Text to Translate', type: 'textarea', placeholder: 'Enter text to translate...', required: true },
            { name: 'target_language', label: 'Target Language', type: 'select', options: ['es', 'fr', 'de', 'pt', 'ar', 'hi', 'zh', 'ja', 'ko'], required: true },
            { name: 'source_language', label: 'Source Language', type: 'select', options: ['en', 'es', 'fr', 'de', 'pt', 'ar', 'hi', 'zh', 'ja', 'ko'], required: true }
        ],
        operational: [
            { name: 'data', label: 'Data to Analyze', type: 'textarea', placeholder: 'e.g., Crowd flow patterns, resource utilization...', required: true }
        ]
    };

    // Load models
    async function loadModels() {
        try {
            const response = await fetch('/api/models');
            const data = await response.json();
            
            const modelList = document.getElementById('modelList');
            modelList.innerHTML = '';
            
            if (data.status === 'success') {
                const models = data.models;
                const allModels = [models.primary, ...models.fallbacks];
                
                allModels.forEach(model => {
                    if (model && model.trim()) {
                        const div = document.createElement('div');
                        div.className = 'model-item';
                        const isAvailable = models.available.includes(model);
                        if (!isAvailable) {
                            div.classList.add('unavailable');
                        }
                        div.textContent = `${model} ${isAvailable ? '✅' : '❌'}`;
                        modelList.appendChild(div);
                    }
                });
            }
        } catch (error) {
            console.error('Error loading models:', error);
            document.getElementById('modelList').innerHTML = '⚠️ Failed to load models';
        }
    }

    // Service card click
    serviceGrid.addEventListener('click', function(e) {
        const card = e.target.closest('.service-card');
        if (!card) return;
        
        const service = card.dataset.service;
        selectedService = service;
        
        // Highlight selected card
        document.querySelectorAll('.service-card').forEach(c => c.classList.remove('active'));
        card.classList.add('active');
        
        // Show input section
        inputSection.classList.remove('hidden');
        serviceTitle.textContent = `${card.querySelector('.service-icon').textContent} ${card.querySelector('h3').textContent}`;
        
        // Generate fields
        generateFields(service);
        
        // Scroll to input
        inputSection.scrollIntoView({ behavior: 'smooth' });
    });

    // Generate fields for service
    function generateFields(service) {
        const fields = serviceFieldsConfig[service] || [];
        serviceFields.innerHTML = '';
        
        fields.forEach(field => {
            const div = document.createElement('div');
            div.className = 'form-group';
            
            const label = document.createElement('label');
            label.textContent = field.label;
            label.htmlFor = field.name;
            
            let input;
            if (field.type === 'select') {
                input = document.createElement('select');
                input.id = field.name;
                input.name = field.name;
                field.options.forEach(opt => {
                    const option = document.createElement('option');
                    option.value = opt;
                    option.textContent = opt.charAt(0).toUpperCase() + opt.slice(1);
                    input.appendChild(option);
                });
            } else if (field.type === 'textarea') {
                input = document.createElement('textarea');
                input.id = field.name;
                input.name = field.name;
                input.placeholder = field.placeholder || '';
                input.rows = 3;
            } else {
                input = document.createElement('input');
                input.type = field.type;
                input.id = field.name;
                input.name = field.name;
                input.placeholder = field.placeholder || '';
            }
            
            if (field.required) {
                input.required = true;
            }
            
            div.appendChild(label);
            div.appendChild(input);
            serviceFields.appendChild(div);
        });
    }

    // Back button
    backBtn.addEventListener('click', function() {
        inputSection.classList.add('hidden');
        results.classList.add('hidden');
        processing.classList.add('hidden');
        document.querySelectorAll('.service-card').forEach(c => c.classList.remove('active'));
        selectedService = null;
    });

    // Form submission
    serviceForm.addEventListener('submit', async function(e) {
        e.preventDefault();
        
        if (!selectedService) return;
        
        // Collect form data
        const formData = new FormData(serviceForm);
        const data = {
            service_type: selectedService,
            language: document.getElementById('language').value
        };
        
        // Add field values
        const fields = serviceFieldsConfig[selectedService] || [];
        fields.forEach(field => {
            const value = formData.get(field.name);
            if (value) {
                data[field.name] = value;
            }
        });
        
        // Show processing
        processing.classList.remove('hidden');
        results.classList.add('hidden');
        progressLog.innerHTML = '';
        submitBtn.disabled = true;
        submitBtn.textContent = 'Processing...';
        agentStatus.textContent = '⏳ AI Agent: Starting...';
        
        try {
            agentStatus.textContent = '🤖 AI Agent: Analyzing request...';
            addLog('📤 Sending request to AI agents...');
            
            const response = await fetch('/api/service', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(data)
            });

            const result = await response.json();

            if (response.ok && result.status === 'success') {
                agentStatus.textContent = '✅ AI Agent: Complete!';
                addLog('✅ Service completed successfully!');
                displayResponse(result);
            } else {
                agentStatus.textContent = '❌ AI Agent: Error';
                addLog(`❌ Error: ${result.error || 'Unknown error'}`);
                alert(`Error: ${result.error || 'Failed to process request'}`);
            }
        } catch (error) {
            console.error('Error:', error);
            agentStatus.textContent = '❌ AI Agent: Network Error';
            addLog(`❌ Network error: ${error.message}`);
            alert('Error processing request. Please try again.');
        } finally {
            processing.classList.add('hidden');
            submitBtn.disabled = false;
            submitBtn.textContent = '🚀 Get Assistance';
        }
    });

    function addLog(message) {
        const logEntry = document.createElement('div');
        logEntry.textContent = `🔄 ${new Date().toLocaleTimeString()}: ${message}`;
        progressLog.appendChild(logEntry);
        progressLog.scrollTop = progressLog.scrollHeight;
    }

    function displayResponse(result) {
        results.classList.remove('hidden');
        
        let html = '';
        const responseData = result.result;
        
        if (responseData.result) {
            html = formatContent(responseData.result);
        } else {
            html = formatContent(JSON.stringify(responseData, null, 2));
        }
        
        responseContent.innerHTML = html;
        results.scrollIntoView({ behavior: 'smooth' });
    }

    function formatContent(text) {
        if (!text) return '';
        
        let html = text
            .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')
            .replace(/\*(.*?)\*/g, '<em>$1</em>')
            .replace(/^# (.*$)/gm, '<h1>$1</h1>')
            .replace(/^## (.*$)/gm, '<h2>$1</h2>')
            .replace(/^### (.*$)/gm, '<h3>$1</h3>')
            .replace(/^#### (.*$)/gm, '<h4>$1</h4>')
            .replace(/^\* (.*$)/gm, '<li>$1</li>')
            .replace(/^- (.*$)/gm, '<li>$1</li>')
            .replace(/\n/g, '<br>');
        
        html = html.replace(/(<li>.*<\/li>)/gs, '<ul>$1</ul>');
        
        return html;
    }

    // Export
    exportBtn.addEventListener('click', function() {
        const content = responseContent.textContent;
        const blob = new Blob([content], { type: 'text/plain' });
        const url = window.URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = `stadium_ai_response_${new Date().toISOString().slice(0,10)}.txt`;
        document.body.appendChild(a);
        a.click();
        document.body.removeChild(a);
        window.URL.revokeObjectURL(url);
    });

    // Copy
    copyBtn.addEventListener('click', function() {
        const text = responseContent.textContent;
        navigator.clipboard.writeText(text).then(() => {
            const original = this.textContent;
            this.textContent = '✅ Copied!';
            setTimeout(() => {
                this.textContent = original;
            }, 2000);
        }).catch(() => {
            const range = document.createRange();
            range.selectNode(responseContent);
            window.getSelection().removeAllRanges();
            window.getSelection().addRange(range);
            document.execCommand('copy');
            const original = this.textContent;
            this.textContent = '✅ Copied!';
            setTimeout(() => {
                this.textContent = original;
            }, 2000);
        });
    });

    // New request
    newRequestBtn.addEventListener('click', function() {
        results.classList.add('hidden');
        inputSection.scrollIntoView({ behavior: 'smooth' });
    });

    // Initialize
    loadModels();
    console.log('🏟️ FIFA World Cup 2026 - AI Stadium Assistant loaded successfully!');
});