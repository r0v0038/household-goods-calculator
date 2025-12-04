// Bulk Upload Calculator - Client-side JavaScript
// Handles file upload, validation, processing, and results display

let currentFile = null;
let currentResults = null;

const uploadArea = document.getElementById('uploadArea');
const fileInput = document.getElementById('fileInput');
const fileInfo = document.getElementById('fileInfo');
const fileName = document.getElementById('fileName');
const validationResults = document.getElementById('validationResults');
const processSection = document.getElementById('processSection');
const errorMessage = document.getElementById('errorMessage');
const progressSection = document.getElementById('progressSection');
const resultsSection = document.getElementById('resultsSection');

// File upload interactions
uploadArea.addEventListener('click', () => fileInput.click());
uploadArea.addEventListener('keypress', (e) => {
    if (e.key === 'Enter' || e.key === ' ') {
        e.preventDefault();
        fileInput.click();
    }
});

// Drag and drop handlers
uploadArea.addEventListener('dragover', (e) => {
    e.preventDefault();
    uploadArea.classList.add('drag-over');
});

uploadArea.addEventListener('dragleave', () => {
    uploadArea.classList.remove('drag-over');
});

uploadArea.addEventListener('drop', (e) => {
    e.preventDefault();
    uploadArea.classList.remove('drag-over');
    
    const files = e.dataTransfer.files;
    if (files.length > 0) {
        handleFileSelection(files[0]);
    }
});

// File input change handler
fileInput.addEventListener('change', (e) => {
    if (e.target.files.length > 0) {
        handleFileSelection(e.target.files[0]);
    }
});

function handleFileSelection(file) {
    // Validate file type
    if (!file.name.endsWith('.xlsx') && !file.name.endsWith('.xls')) {
        showError('Invalid file type. Please select an Excel file (.xlsx or .xls)');
        return;
    }
    
    // Validate file size (16MB limit)
    if (file.size > 16 * 1024 * 1024) {
        showError('File too large. Maximum size is 16MB');
        return;
    }
    
    currentFile = file;
    
    // Show file info
    fileName.textContent = file.name;
    fileInfo.style.display = 'block';
    uploadArea.style.display = 'none';
    
    // Clear previous results
    hideError();
    validationResults.style.display = 'none';
    processSection.style.display = 'none';
    resultsSection.style.display = 'none';
    
    // Validate file
    validateFile(file);
}

function clearFile() {
    currentFile = null;
    fileInput.value = '';
    fileInfo.style.display = 'none';
    uploadArea.style.display = 'flex';
    validationResults.style.display = 'none';
    processSection.style.display = 'none';
    resultsSection.style.display = 'none';
    hideError();
}

async function validateFile(file) {
    try {
        const formData = new FormData();
        formData.append('file', file);
        
        const response = await fetch('/bulk/validate', {
            method: 'POST',
            body: formData
        });
        
        const data = await response.json();
        
        if (data.success && data.validation) {
            displayValidationResults(data.validation);
        } else {
            showError(data.error || 'Validation failed');
        }
        
    } catch (error) {
        showError('Network error during validation: ' + error.message);
    }
}

function displayValidationResults(validation) {
    let html = '';
    
    if (validation.valid) {
        html = `
            <div class="validation-success">
                <div class="validation-icon">✅</div>
                <div>
                    <strong>File is valid and ready to process!</strong>
                    <p>Found ${validation.row_count} row(s) of data</p>
                </div>
            </div>
        `;
        
        if (validation.warnings && validation.warnings.length > 0) {
            html += '<div class="validation-warnings">';
            html += '<strong>⚠️ Warnings:</strong><ul>';
            validation.warnings.forEach(warning => {
                html += `<li>${warning}</li>`;
            });
            html += '</ul></div>';
        }
        
        processSection.style.display = 'block';
    } else {
        html = `
            <div class="validation-error">
                <div class="validation-icon">❌</div>
                <div>
                    <strong>File validation failed</strong>
                    <ul>
        `;
        validation.errors.forEach(error => {
            html += `<li>${error}</li>`;
        });
        html += '</ul></div></div>';
        
        processSection.style.display = 'none';
    }
    
    document.getElementById('validationContent').innerHTML = html;
    validationResults.style.display = 'block';
    validationResults.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
}

async function processFile() {
    if (!currentFile) {
        showError('No file selected');
        return;
    }
    
    // Show progress
    progressSection.style.display = 'block';
    resultsSection.style.display = 'none';
    hideError();
    
    const processBtn = document.getElementById('processBtn');
    processBtn.disabled = true;
    processBtn.textContent = 'Processing...';
    
    try {
        const formData = new FormData();
        formData.append('file', currentFile);
        
        // Collect custom rate settings and add to form data
        const customRates = {
            self_pack: parseFloat(document.getElementById('selfPackRate').value) / 100,
            partial_pack: parseFloat(document.getElementById('partialPackRate').value) / 100,
            full_pack: parseFloat(document.getElementById('fullPackRate').value) / 100,
            no_storage: parseFloat(document.getElementById('noStorageRate').value) / 100,
            storage_30days: parseFloat(document.getElementById('storage30Rate').value) / 100,
            storage_60days: parseFloat(document.getElementById('storage60Rate').value) / 100,
            insurance_per_1000: parseFloat(document.getElementById('insuranceRate').value),
            fuel_surcharge: parseFloat(document.getElementById('fuelSurcharge').value) / 100,
            minimum_charge: parseFloat(document.getElementById('minimumCharge').value),
            discount: parseFloat(document.getElementById('discountRate').value) / 100
        };
        formData.append('custom_rates', JSON.stringify(customRates));
        
        // Simulate progress animation
        let progress = 0;
        const progressInterval = setInterval(() => {
            progress += 5;
            if (progress <= 90) {
                updateProgress(progress, 'Processing calculations...');
            }
        }, 200);
        
        const response = await fetch('/bulk/process', {
            method: 'POST',
            body: formData
        });
        
        clearInterval(progressInterval);
        
        const data = await response.json();
        
        if (data.success) {
            updateProgress(100, 'Complete!');
            setTimeout(() => {
                progressSection.style.display = 'none';
                displayResults(data);
            }, 500);
        } else {
            progressSection.style.display = 'none';
            showError(data.error || 'Processing failed');
        }
        
    } catch (error) {
        progressSection.style.display = 'none';
        showError('Network error during processing: ' + error.message);
    } finally {
        processBtn.disabled = false;
        processBtn.textContent = '🚀 Process Calculations';
    }
}

function updateProgress(percent, text) {
    document.getElementById('progressFill').style.width = percent + '%';
    document.getElementById('progressText').textContent = text + ` (${percent}%)`;
}

function displayResults(data) {
    currentResults = data.results;
    const summary = data.summary;
    const errors = data.errors || [];
    
    // Display summary stats
    const summaryHTML = `
        <div class="stat-card">
            <div class="stat-label">Total Rows</div>
            <div class="stat-value">${summary.total_rows}</div>
        </div>
        <div class="stat-card success">
            <div class="stat-label">Successful</div>
            <div class="stat-value">${summary.successful}</div>
        </div>
        <div class="stat-card ${summary.failed > 0 ? 'error' : ''}">
            <div class="stat-label">Failed</div>
            <div class="stat-value">${summary.failed}</div>
        </div>
        <div class="stat-card">
            <div class="stat-label">Success Rate</div>
            <div class="stat-value">${summary.success_rate}</div>
        </div>
    `;
    document.getElementById('summaryStats').innerHTML = summaryHTML;
    
    // Display errors if any
    if (errors.length > 0) {
        let errorHTML = '<div class="bulk-errors"><h4>Processing Errors:</h4><ul>';
        errors.slice(0, 10).forEach(error => {
            errorHTML += `<li>${error}</li>`;
        });
        if (errors.length > 10) {
            errorHTML += `<li><em>... and ${errors.length - 10} more errors</em></li>`;
        }
        errorHTML += '</ul></div>';
        document.getElementById('summaryStats').innerHTML += errorHTML;
    }
    
    // Display results table
    let tableHTML = '';
    currentResults.forEach(result => {
        const statusClass = result.status === 'success' ? 'success' : 'failed';
        const statusIcon = result.status === 'success' ? '✓' : '✗';
        
        if (result.status === 'failed') {
            tableHTML += `
                <tr class="${statusClass}">
                    <td>${result.row_number}</td>
                    <td><span class="status-badge ${statusClass}">${statusIcon} FAILED</span></td>
                    <td>${result.origin}</td>
                    <td>${result.destination}</td>
                    <td>-</td>
                    <td>-</td>
                    <td>-</td>
                    <td class="error-cell">${result.error}</td>
                </tr>
            `;
        } else {
            tableHTML += `
                <tr class="${statusClass}">
                    <td>${result.row_number}</td>
                    <td><span class="status-badge ${statusClass}">${statusIcon} SUCCESS</span></td>
                    <td>${result.origin}</td>
                    <td>${result.destination}</td>
                    <td>${result.distance_miles.toLocaleString()} mi</td>
                    <td>${result.weight_pounds.toLocaleString()} lbs</td>
                    <td class="cost-cell">$${result.total_should_cost.toLocaleString('en-US', {minimumFractionDigits: 2, maximumFractionDigits: 2})}</td>
                    <td><button onclick="showRowDetails(${result.row_number})" class="details-btn">View</button></td>
                </tr>
            `;
        }
    });
    
    document.getElementById('resultsTableBody').innerHTML = tableHTML;
    
    // Show results section
    resultsSection.style.display = 'block';
    resultsSection.scrollIntoView({ behavior: 'smooth', block: 'start' });
}

function showRowDetails(rowNumber) {
    const result = currentResults.find(r => r.row_number === rowNumber);
    if (!result) return;
    
    const breakdown = result.breakdown;
    let detailsHTML = `
        <div class="modal-overlay" onclick="closeModal()">
            <div class="modal-content" onclick="event.stopPropagation()">
                <div class="modal-header">
                    <h3>Row ${rowNumber} - Detailed Breakdown</h3>
                    <button onclick="closeModal()" class="modal-close">×</button>
                </div>
                <div class="modal-body">
                    <div class="detail-section">
                        <h4>📍 Route Information</h4>
                        <p><strong>Origin:</strong> ${result.origin} (${breakdown.origin_region})</p>
                        <p><strong>Destination:</strong> ${result.destination} (${breakdown.destination_region})</p>
                        <p><strong>Distance:</strong> ${result.distance_miles.toLocaleString()} miles</p>
                        <p><strong>Weight:</strong> ${result.weight_pounds.toLocaleString()} lbs</p>
                    </div>
                    
                    <div class="detail-section">
                        <h4>💰 Cost Breakdown</h4>
                        <table class="breakdown-table">
                            <tr>
                                <td>Material Cost</td>
                                <td>$${(breakdown.material_adjusted_cost || 0).toFixed(2)}</td>
                            </tr>
                            <tr>
                                <td>Transportation Cost</td>
                                <td>$${(breakdown.transportation_cost || 0).toFixed(2)}</td>
                            </tr>
                            <tr>
                                <td>Packing (${breakdown.packing_service || 'N/A'})</td>
                                <td>$${(breakdown.packing_cost || 0).toFixed(2)}</td>
                            </tr>
                            <tr>
                                <td>Storage (${breakdown.storage_option || 'N/A'})</td>
                                <td>$${(breakdown.storage_cost || 0).toFixed(2)}</td>
                            </tr>
                            <tr>
                                <td>Fuel Surcharge</td>
                                <td>$${(breakdown.fuel_charge || 0).toFixed(2)}</td>
                            </tr>
                            <tr>
                                <td>Insurance</td>
                                <td>$${(breakdown.insurance_cost || 0).toFixed(2)}</td>
                            </tr>
                            <tr>
                                <td>Tariffs & Taxes</td>
                                <td>$${(breakdown.total_tariffs_and_taxes || 0).toFixed(2)}</td>
                            </tr>
                            <tr class="total-row">
                                <td><strong>Total Should Cost</strong></td>
                                <td><strong>$${(result.total_should_cost || 0).toFixed(2)}</strong></td>
                            </tr>
                        </table>
                    </div>
                </div>
            </div>
        </div>
    `;
    
    document.body.insertAdjacentHTML('beforeend', detailsHTML);
}

function closeModal() {
    const modal = document.querySelector('.modal-overlay');
    if (modal) {
        modal.remove();
    }
}

function downloadResults() {
    if (!currentResults || currentResults.length === 0) {
        showError('No results to download');
        return;
    }
    
    // Create a form to submit results for download
    const form = document.createElement('form');
    form.method = 'GET';
    form.action = '/bulk/download/excel';
    form.target = '_blank';
    
    const input = document.createElement('input');
    input.type = 'hidden';
    input.name = 'results';
    input.value = JSON.stringify(currentResults);
    
    form.appendChild(input);
    document.body.appendChild(form);
    form.submit();
    document.body.removeChild(form);
}

function downloadTemplate() {
    window.open('/bulk/template', '_blank');
}

// Toggle advanced settings visibility
// Toggle advanced settings visibility
function toggleSettings() {
    const settings = document.getElementById('advancedSettings');
    const toggle = document.querySelector('.settings-toggle');
    const icon = document.getElementById('toggleIcon');
    
    if (!settings || !toggle || !icon) return;
    
    settings.classList.toggle('show');
    
    if (settings.classList.contains('show')) {
        toggle.setAttribute('aria-expanded', 'true');
        icon.textContent = '▲';
    } else {
        toggle.setAttribute('aria-expanded', 'false');
        icon.textContent = '▼';
    }
}

// Reset settings to defaults
function resetSettings() {
    document.getElementById('selfPackRate').value = 100;
    document.getElementById('partialPackRate').value = 115;
    document.getElementById('fullPackRate').value = 135;
    document.getElementById('noStorageRate').value = 100;
    document.getElementById('storage30Rate').value = 120;
    document.getElementById('storage60Rate').value = 135;
    document.getElementById('insuranceRate').value = 5.00;
    document.getElementById('fuelSurcharge').value = 12;
    document.getElementById('minimumCharge').value = 500;
}

function showError(message) {
    errorMessage.textContent = '❌ ' + message;
    errorMessage.style.display = 'block';
    errorMessage.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
}

function hideError() {
    errorMessage.style.display = 'none';
}

// Keyboard accessibility for modal close
document.addEventListener('keydown', (e) => {
    if (e.key === 'Escape') {
        closeModal();
    }
});

// Keyboard accessibility for settings toggle
document.addEventListener('DOMContentLoaded', () => {
    const settingsToggle = document.querySelector('.settings-toggle');
    if (settingsToggle) {
        settingsToggle.addEventListener('keypress', (e) => {
            if (e.key === 'Enter' || e.key === ' ') {
                e.preventDefault();
                toggleSettings();
            }
        });
    }
});
