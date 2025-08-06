// CodeLitmus Frontend JavaScript
const API_BASE_URL = 'http://127.0.0.1:8000';

function switchTab(tabName) {
    // Hide all tab contents
    const contents = document.querySelectorAll('.tab-content');
    contents.forEach(content => content.classList.remove('active'));
    
    // Remove active class from all tabs
    const tabs = document.querySelectorAll('.tab');
    tabs.forEach(tab => tab.classList.remove('active'));
    
    // Show selected tab content
    document.getElementById(tabName).classList.add('active');
    
    // Add active class to clicked tab
    event.target.classList.add('active');
}

async function analyzeCode() {
    const file = document.getElementById('codeFile').files[0];
    if (!file) {
        document.getElementById("result").innerHTML = '<p class="error">Please select a file first.</p>';
        return;
    }
    
    const formData = new FormData();
    formData.append("file", file);
    
    try {
        document.getElementById("result").innerHTML = '<p style="text-align: center;">Analyzing...</p>';
        
        const res = await fetch(`${API_BASE_URL}/analyze/`, {
            method: "POST",
            body: formData
        });
        
        const data = await res.json();
        
        if (res.ok) {
            const verdictColor = data.verdict === 'Basic' ? 'green' : 
                               data.verdict === 'Neutral' ? 'orange' : 'red';
            
            document.getElementById("result").innerHTML = `
                <h2>Verdict: <span style="color:${verdictColor}">${data.verdict}</span></h2>
                <p><strong>Score:</strong> ${data.score}</p>
                <p><strong>Feedback:</strong></p>
                <ul>${data.feedback.map(f => `<li>• ${f}</li>`).join('')}</ul>
            `;
        } else {
            document.getElementById("result").innerHTML = `<p class="error">Error: ${data.error}</p>`;
        }
    } catch (error) {
        document.getElementById("result").innerHTML = `<p class="error">Error: ${error.message}</p>`;
    }
}