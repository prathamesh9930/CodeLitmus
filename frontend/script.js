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
            
            let goodPointsHtml = '';
            if (data.detailed_feedback.good_points.length > 0) {
                goodPointsHtml = `
                    <div style="background: rgba(39, 174, 96, 0.1); padding: 15px; border-radius: 8px; margin: 15px 0; border-left: 4px solid #27ae60;">
                        <h3 style="color: #27ae60; margin-top: 0;">✅ Strengths of Your Code</h3>
                        <ul>${data.detailed_feedback.good_points.map(point => `<li style="color: #2ecc71;">• ${point}</li>`).join('')}</ul>
                    </div>
                `;
            }
            
            let improvementHtml = '';
            if (data.detailed_feedback.areas_for_improvement.length > 0) {
                improvementHtml = `
                    <div style="background: rgba(231, 76, 60, 0.1); padding: 15px; border-radius: 8px; margin: 15px 0; border-left: 4px solid #e74c3c;">
                        <h3 style="color: #e74c3c; margin-top: 0;">🔧 Areas for Improvement</h3>
                        <ul>${data.detailed_feedback.areas_for_improvement.map(point => `<li style="color: #e67e22;">• ${point}</li>`).join('')}</ul>
                    </div>
                `;
            }
            
            let metricsHtml = '';
            if (data.detailed_feedback.metrics_explanation) {
                metricsHtml = `
                    <div style="background: rgba(52, 152, 219, 0.1); padding: 15px; border-radius: 8px; margin: 15px 0; border-left: 4px solid #3498db;">
                        <h3 style="color: #3498db; margin-top: 0;">📊 Detailed Metrics Analysis</h3>
                        <div style="margin-bottom: 15px; line-height: 1.6;"><strong>🔄 Complexity:</strong> ${data.detailed_feedback.metrics_explanation.complexity}</div>
                        <div style="margin-bottom: 15px; line-height: 1.6;"><strong>🔧 Maintainability:</strong> ${data.detailed_feedback.metrics_explanation.maintainability}</div>
                        <div style="line-height: 1.6;"><strong>💬 Comments:</strong> ${data.detailed_feedback.metrics_explanation.comments}</div>
                    </div>
                `;
            }
            
            document.getElementById("result").innerHTML = `
                <h2>Verdict: <span style="color:${verdictColor}">${data.verdict}</span></h2>
                <p style="text-align: center; font-style: italic; color: #bdc3c7;">${data.verdict_explanation}</p>
                <p><strong>Overall Score:</strong> ${data.score}/3</p>
                
                ${goodPointsHtml}
                ${improvementHtml}
                ${metricsHtml}
                
                <div style="background: rgba(255, 255, 255, 0.05); padding: 15px; border-radius: 8px; margin: 15px 0;">
                    <h3 style="color: #f39c12; margin-top: 0;">📋 Quick Summary</h3>
                    <ul>${data.feedback.map(f => `<li>• ${f}</li>`).join('')}</ul>
                </div>
            `;
        } else {
            document.getElementById("result").innerHTML = `<p class="error">Error: ${data.error}</p>`;
        }
    } catch (error) {
        document.getElementById("result").innerHTML = `<p class="error">Error: ${error.message}</p>`;
    }
}