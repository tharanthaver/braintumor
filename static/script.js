document.addEventListener("DOMContentLoaded", function() {
    const fileInput = document.getElementById('fileInput');
    const previewImg = document.getElementById('previewImg');
    const imagePreview = document.getElementById('imagePreview');
    const fileName = document.getElementById('fileName');
    const analyzeBtn = document.getElementById('analyzeBtn');
    const loading = document.getElementById('loading');
    const resultsSection = document.getElementById('results');
    const noTumorResult = document.getElementById('noTumorResult');
    const tumorResult = document.getElementById('tumorResult');
    const noTumorConfidence = document.getElementById('noTumorConfidence');
    const noTumorConfidenceText = document.getElementById('noTumorConfidenceText');
    const tumorType = document.getElementById('tumorType');
    const tumorConfidence = document.getElementById('tumorConfidence');
    const tumorConfidenceText = document.getElementById('tumorConfidenceText');
    const currentSize = document.getElementById('currentSize');
    const predictedSize = document.getElementById('predictedSize');
    const growthRate = document.getElementById('growthRate');
    const currentSymptoms = document.getElementById('currentSymptoms');
    const futureSymptoms = document.getElementById('futureSymptoms');
    const tumorDescription = document.getElementById('tumorDescription');
    const recommendations = document.getElementById('recommendations');
    const probabilityBars = document.getElementById('probabilityBars');

    fileInput.addEventListener('change', function() {
        const file = this.files[0];
        if (file) {
            const reader = new FileReader();
            reader.onload = function(e) {
                previewImg.src = e.target.result;
                imagePreview.style.display = 'block';
                fileName.textContent = file.name;
            }
            reader.readAsDataURL(file);
        }
    });

    analyzeBtn.addEventListener('click', function() {
        const file = fileInput.files[0];
        if (!file) {
            alert("Please upload an MRI image.");
            return;
        }

        const formData = new FormData();
        formData.append('file', file);

        // Display loading
        imagePreview.style.display = 'none';
        loading.style.display = 'flex';

        fetch('http://localhost:8000/predict', {
            method: 'POST',
            body: formData
        })
        .then(response => response.json())
        .then(data => {
            loading.style.display = 'none';
            resultsSection.style.display = 'block';
            
            if (!data.tumor_detected) {
                // No tumor detected
                noTumorResult.style.display = 'block';
                tumorResult.style.display = 'none';
                noTumorConfidenceText.textContent = (data.confidence * 100).toFixed(2) + '%';
                noTumorConfidence.style.width = (data.confidence * 100).toFixed(2) + '%';
            } else {
                // Tumor detected
                noTumorResult.style.display = 'none';
                tumorResult.style.display = 'block';

                tumorType.textContent = data.tumor_type;
                tumorConfidenceText.textContent = (data.confidence * 100).toFixed(2) + '%';
                tumorConfidence.style.width = (data.confidence * 100).toFixed(2) + '%';

                currentSize.textContent = data.current_size_cm2.toFixed(2);
                predictedSize.textContent = data.predicted_size_after_3_months.toFixed(2);
                growthRate.textContent = (data.growth_rate_cm2_per_month).toFixed(2);

                currentSymptoms.innerHTML = data.current_expected_symptoms.map(symptom => `<li>${symptom}</li>`).join('');
                futureSymptoms.innerHTML = data.future_expected_symptoms.map(symptom => `<li>${symptom}</li>`).join('');

                tumorDescription.innerHTML = `<p><strong>Size Estimation:</strong> ${data.analysis_notes.size_estimation}</p>` +
                                            `<p><strong>Growth Model:</strong> ${data.analysis_notes.growth_model}</p>` +
                                            `<p><strong>Symptoms Basis:</strong> ${data.analysis_notes.symptoms}</p>`;
                
                recommendations.innerHTML = `<p>1. Consult with a neurologist for further evaluation.</p>` +
                                            `<p>2. Consider regular follow-up MRI scans for monitoring.</p>` +
                                            `<p>3. Discuss potential symptoms with a healthcare provider.</p>`;
                
                // Detailed probabilities
                probabilityBars.innerHTML = '';
                for (const [category, prob] of Object.entries(data.all_probabilities)) {
                    const probabilityFillWidth = (prob * 100).toFixed(2) + '%';
                    probabilityBars.innerHTML += `<div class="probability-bar"><div class="probability-label">
                                                    <span>${category}</span><span>${probabilityFillWidth}</span></div>
                                                    <div class="probability-fill" style="width: ${probabilityFillWidth}"></div></div>`;
                }
            }
        })
        .catch(error => {
            loading.style.display = 'none';
            alert('An error occurred while analyzing the image. Please try again.\nError: ' + error.message);
        });
    });

});

function resetAnalysis() {
    document.getElementById('fileInput').value = "";
    document.getElementById('imagePreview').style.display = 'none';
    document.getElementById('results').style.display = 'none';
}

function downloadReport() {
    // Dummy implementation - to be expanded with actual report generation logic
    alert('Download functionality not implemented yet.');
}
