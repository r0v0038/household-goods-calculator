// Household Goods Calculator - Client-side JavaScript
// Handles form submission, API calls, and results display

const form = document.getElementById('calculatorForm');
const resultsDiv = document.getElementById('results');
const errorDiv = document.getElementById('errorMessage');
const calculateBtn = document.getElementById('calculateBtn');

// Form submission handler
form.addEventListener('submit', async (e) => {
    e.preventDefault();
    
    // Hide previous results and errors
    resultsDiv.classList.remove('show');
    errorDiv.classList.remove('show');
    
    // Disable button and show loading state
    calculateBtn.disabled = true;
    calculateBtn.textContent = 'Calculating...';
    
    try {
        const formData = {
            origin: document.getElementById('origin').value,
            destination: document.getElementById('destination').value,
            weight: parseFloat(document.getElementById('weight').value),
            packing_service: document.getElementById('packing').value,
            storage_option: document.getElementById('storage').value,
            include_insurance: document.getElementById('insurance').checked,
            // Custom rate settings
            custom_rates: {
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
            }
        };
        
        // Add manual distance if provided
        const distanceInput = document.getElementById('distance').value;
        if (distanceInput) {
            formData.distance_miles = parseFloat(distanceInput);
        }
        
        const response = await fetch('/calculate', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(formData)
        });
        
        const data = await response.json();
        
        if (data.success) {
            displayResults(data.result);
        } else {
            showError(data.error || 'Calculation failed');
        }
    } catch (error) {
        showError('Network error: ' + error.message);
    } finally {
        // Re-enable button
        calculateBtn.disabled = false;
        calculateBtn.textContent = 'Calculate Should Cost';
    }
});

function displayResults(result) {
    // Update summary
    document.getElementById('routeSummary').textContent = 
        `${result.origin} → ${result.destination}`;
    
    // Show distance with auto-calculated indicator if applicable
    const distanceInput = document.getElementById('distance').value;
    const distanceText = result.distance_miles.toLocaleString();
    const distanceSummary = document.getElementById('distanceSummary');
    
    if (!distanceInput || distanceInput.trim() === '') {
        // Distance was auto-calculated
        distanceSummary.innerHTML = `${distanceText} <span style="font-size: 0.8em; color: #06a77d;">✓ auto-calculated</span>`;
    } else {
        distanceSummary.textContent = distanceText;
    }
    
    document.getElementById('weightSummary').textContent = 
        result.weight_pounds.toLocaleString();
    document.getElementById('totalCost').textContent = 
        `$${result.total_should_cost.toLocaleString('en-US', {minimumFractionDigits: 2, maximumFractionDigits: 2})}`;
    
    // Build breakdown with organized sections
    const breakdown = result.breakdown;
    const breakdownHTML = buildBreakdownHTML(result, breakdown);
    
    document.getElementById('breakdownDetails').innerHTML = breakdownHTML;
    
    // Show results
    resultsDiv.classList.add('show');
    
    // Scroll to results
    resultsDiv.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
}

function buildBreakdownHTML(result, breakdown) {
    return `
        <!-- Material Costs Section -->
        <div class="cost-section material">
            <h3><span class="icon">📦</span>Material Costs (Household Goods)</h3>
            <div class="breakdown-item">
                <span class="breakdown-label">Base Material Cost (${result.weight_pounds.toLocaleString()} lbs @ $${((breakdown.material_base_cost || 0) / result.weight_pounds).toFixed(2)} per lb)</span>
                <span class="breakdown-value">$${(breakdown.material_base_cost || 0).toFixed(2)}</span>
            </div>
            <div class="breakdown-item">
                <span class="breakdown-label">Weight Tier Adjustment (${((breakdown.material_weight_adjustment || 1) * 100).toFixed(0)}%)</span>
                <span class="breakdown-value">${(breakdown.material_weight_adjustment || 1) < 1 ? 'Discount' : 'Premium'}</span>
            </div>
            <div class="breakdown-item section-total">
                <span class="breakdown-label">Total Material Cost</span>
                <span class="breakdown-value">$${(breakdown.material_adjusted_cost || 0).toFixed(2)}</span>
            </div>
        </div>

        <!-- Transportation Costs Section -->
        <div class="cost-section transportation">
            <h3><span class="icon">🚚</span>Transportation Costs</h3>
            <div class="breakdown-item">
                <span class="breakdown-label">Matrix-Based Transportation Cost</span>
                <span class="breakdown-value">$${(breakdown.transportation_cost || 0).toFixed(2)}</span>
            </div>
            <div class="breakdown-item">
                <span class="breakdown-label">Weight Bracket: ${breakdown.transportation_weight_bracket || 'N/A'}</span>
                <span class="breakdown-value"></span>
            </div>
            <div class="breakdown-item">
                <span class="breakdown-label">Distance Bracket: ${breakdown.transportation_distance_bracket || 'N/A'}</span>
                <span class="breakdown-value"></span>
            </div>
            <div class="breakdown-item section-total">
                <span class="breakdown-label">Total Transportation Cost</span>
                <span class="breakdown-value">$${(breakdown.transportation_cost || 0).toFixed(2)}</span>
            </div>
        </div>

        <!-- Service Costs Section -->
        <div class="cost-section services">
            <h3><span class="icon">🛠️</span>Service Costs</h3>
            <div class="breakdown-item">
                <span class="breakdown-label">
                    Packing Service: ${(breakdown.packing_service || 'self_pack').replace(/_/g, ' ').replace(/\b\w/g, l => l.toUpperCase())}
                    <div class="tariff-rate">Multiplier: ${((breakdown.packing_multiplier || 1.0) * 100).toFixed(0)}%</div>
                </span>
                <span class="breakdown-value">${(breakdown.packing_cost || 0) > 0 ? '$' + (breakdown.packing_cost || 0).toFixed(2) : 'Included'}</span>
            </div>
            <div class="breakdown-item">
                <span class="breakdown-label">
                    Storage: ${(breakdown.storage_option || 'no_storage').replace(/_/g, ' ').replace(/\b\w/g, l => l.toUpperCase())}
                    <div class="tariff-rate">Multiplier: ${((breakdown.storage_multiplier || 1.0) * 100).toFixed(0)}%</div>
                </span>
                <span class="breakdown-value">${(breakdown.storage_cost || 0) > 0 ? '$' + (breakdown.storage_cost || 0).toFixed(2) : 'Included'}</span>
            </div>
            <div class="breakdown-item section-total">
                <span class="breakdown-label">Total Service Cost</span>
                <span class="breakdown-value">$${((breakdown.packing_cost || 0) + (breakdown.storage_cost || 0)).toFixed(2)}</span>
            </div>
        </div>

        <!-- Other Costs Section -->
        <div class="cost-section other">
            <h3><span class="icon">💰</span>Other Costs</h3>
            <div class="breakdown-item">
                <span class="breakdown-label">Regional Adjustment (${breakdown.origin_region || 'default'} → ${breakdown.destination_region || 'default'})</span>
                <span class="breakdown-value">${(breakdown.regional_cost_adjustment || 0) >= 0 ? '$' + (breakdown.regional_cost_adjustment || 0).toFixed(2) : '-$' + Math.abs(breakdown.regional_cost_adjustment || 0).toFixed(2)}</span>
            </div>
            <div class="breakdown-item">
                <span class="breakdown-label">Fuel Surcharge (${((breakdown.fuel_surcharge_rate || 0) * 100).toFixed(0)}%)</span>
                <span class="breakdown-value">$${(breakdown.fuel_charge || 0).toFixed(2)}</span>
            </div>
            <div class="breakdown-item">
                <span class="breakdown-label">
                    Insurance Coverage
                    ${(breakdown.insurance_cost || 0) > 0 ? `<div class="tariff-rate">Rate: $${((result.weight_pounds || 0) / 1000).toFixed(1)}K lbs @ $5.00 per 1000 lbs</div>` : ''}
                </span>
                <span class="breakdown-value">${(breakdown.insurance_cost || 0) > 0 ? '$' + (breakdown.insurance_cost || 0).toFixed(2) : 'Not Included'}</span>
            </div>
            <div class="breakdown-item section-total">
                <span class="breakdown-label">Total Other Costs</span>
                <span class="breakdown-value">$${((breakdown.regional_cost_adjustment || 0) + (breakdown.fuel_charge || 0) + (breakdown.insurance_cost || 0)).toFixed(2)}</span>
            </div>
        </div>

        <!-- Discount Section -->
        ${(breakdown.discount_amount || 0) > 0 ? `
        <div class="cost-section discount" style="background: #c8e6c9; border-left: 4px solid #2e7d32;">
            <h3><span class="icon">✂️</span>Discount Applied</h3>
            <div class="breakdown-item">
                <span class="breakdown-label">
                    Discount (${((breakdown.discount_rate || 0) * 100).toFixed(1)}% off subtotal)
                    <div class="tariff-rate">Applied to: Material + Transportation + Services + Regional + Insurance</div>
                </span>
                <span class="breakdown-value" style="color: #2e7d32; font-weight: bold;">-$${(breakdown.discount_amount || 0).toFixed(2)}</span>
            </div>
            <div class="breakdown-item" style="background: #a5d6a7; padding: 8px; margin-top: 8px; border-radius: 4px;">
                <span class="breakdown-label" style="color: #1b5e20;"><strong>Subtotal After Discount</strong></span>
                <span class="breakdown-value" style="color: #1b5e20; font-weight: bold;">$${(breakdown.subtotal_after_discount || 0).toFixed(2)}</span>
            </div>
        </div>
        ` : ''}

        <!-- Tariffs & Taxes Section -->
        ${(breakdown.total_tariffs_and_taxes || 0) > 0 ? `
        <div class="cost-section tariffs">
            <h3><span class="icon">📊</span>Tariffs & Taxes</h3>
            
            <!-- Collapsible Toggle -->
            <div class="tariff-toggle" onclick="toggleTariffDetails()" role="button" tabindex="0" aria-expanded="false" aria-controls="tariffDetails">
                <div>
                    <strong>Total Tariffs & Taxes: $${(breakdown.total_tariffs_and_taxes || 0).toFixed(2)}</strong>
                    <div class="tariff-rate">Click to view breakdown</div>
                </div>
                <span class="tariff-toggle-icon" id="tariffToggleIcon">▼</span>
            </div>

            <!-- Detailed Breakdown (Collapsible) -->
            <div class="tariff-details" id="tariffDetails">
                ${(breakdown.interstate_tariff || 0) > 0 ? `
                <div class="breakdown-item">
                    <span class="breakdown-label">
                        ${breakdown.tariff_description} Commerce Fee
                        <div class="tariff-rate">Rate: 3.00% of subtotal ($${(breakdown.subtotal_before_tariffs || 0).toFixed(2)})</div>
                    </span>
                    <span class="breakdown-value">$${(breakdown.interstate_tariff || 0).toFixed(2)}</span>
                </div>
                ` : `
                <div class="breakdown-item">
                    <span class="breakdown-label">
                        Interstate Commerce Fee
                        <div class="tariff-rate">Not applicable (intrastate move)</div>
                    </span>
                    <span class="breakdown-value">$0.00</span>
                </div>
                `}
                ${(breakdown.state_tax || 0) > 0 ? `
                <div class="breakdown-item">
                    <span class="breakdown-label">
                        State Moving Tax (${breakdown.destination_state})
                        <div class="tariff-rate">Rate: ${getStateTaxRate(breakdown.destination_state || '')} of subtotal ($${(breakdown.subtotal_before_tariffs || 0).toFixed(2)})</div>
                    </span>
                    <span class="breakdown-value">$${(breakdown.state_tax || 0).toFixed(2)}</span>
                </div>
                ` : `
                <div class="breakdown-item">
                    <span class="breakdown-label">
                        State Moving Tax (${breakdown.destination_state || 'N/A'})
                        <div class="tariff-rate">No state tax configured for this state</div>
                    </span>
                    <span class="breakdown-value">$0.00</span>
                </div>
                `}
                <div class="breakdown-item section-total" style="margin-top: 10px;">
                    <span class="breakdown-label">Total Tariffs & Taxes</span>
                    <span class="breakdown-value">$${(breakdown.total_tariffs_and_taxes || 0).toFixed(2)}</span>
                </div>
                
                <!-- Effective Rate Calculation -->
                <div class="breakdown-item" style="background: #e3f2fd; padding: 10px; margin-top: 10px; border-radius: 4px;">
                    <span class="breakdown-label" style="color: #0d47a1;">
                        <strong>Effective Tariff Rate</strong>
                        <div class="tariff-rate" style="color: #1565c0;">
                            ${(((breakdown.total_tariffs_and_taxes || 0) / (breakdown.subtotal_before_tariffs || 1)) * 100).toFixed(2)}% of subtotal
                        </div>
                    </span>
                    <span class="breakdown-value" style="color: #0d47a1;">
                        <strong>${(breakdown.tariff_type || 'none').charAt(0).toUpperCase() + (breakdown.tariff_type || 'none').slice(1)}</strong>
                    </span>
                </div>
            </div>
        </div>
        ` : `
        <div class="cost-section tariffs">
            <h3><span class="icon">✅</span>Tariffs & Taxes</h3>
            <div class="breakdown-item">
                <span class="breakdown-label">No tariffs or taxes apply</span>
                <span class="breakdown-value">$0.00</span>
            </div>
        </div>
        `}

        ${breakdown.applied_minimum_charge ? `
        <div class="breakdown-item" style="background: #fff3cd; padding: 10px; margin-top: 10px; border-radius: 4px;">
            <span class="breakdown-label" style="color: #856404;">⚠️ Minimum Charge Applied</span>
            <span class="breakdown-value" style="color: #856404;">Calculation below minimum, adjusted to minimum charge</span>
        </div>
        ` : ''}
    `;
}

function showError(message) {
    errorDiv.textContent = '❌ ' + message;
    errorDiv.classList.add('show');
    errorDiv.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
}

function toggleSettings() {
    const content = document.getElementById('advancedSettings');
    const icon = document.getElementById('toggleIcon');
    const toggle = document.querySelector('.settings-toggle');
    
    content.classList.toggle('open');
    icon.classList.toggle('open');
    
    const isOpen = content.classList.contains('open');
    toggle.setAttribute('aria-expanded', isOpen);
}

function resetSettings() {
    // Reset to default values and clear highlighting
    advancedSettingsInputs.forEach(inputId => {
        const input = document.getElementById(inputId);
        if (input) {
            input.value = defaultValues[inputId];
            input.style.backgroundColor = '';
            input.style.borderColor = '';
        }
    });
    
    alert('Settings reset to defaults!');
}

// Keyboard accessibility for settings toggle
document.querySelector('.settings-toggle').addEventListener('keypress', (e) => {
    if (e.key === 'Enter' || e.key === ' ') {
        e.preventDefault();
        toggleSettings();
    }
});

// Track changes to advanced settings
const advancedSettingsInputs = [
    'selfPackRate', 'partialPackRate', 'fullPackRate',
    'noStorageRate', 'storage30Rate', 'storage60Rate',
    'insuranceRate', 'fuelSurcharge', 'minimumCharge', 'discountRate'
];

const defaultValues = {
    'selfPackRate': 100,
    'partialPackRate': 115,
    'fullPackRate': 135,
    'noStorageRate': 100,
    'storage30Rate': 120,
    'storage60Rate': 135,
    'insuranceRate': 5.00,
    'fuelSurcharge': 12,
    'minimumCharge': 500,
    'discountRate': 0
};

advancedSettingsInputs.forEach(inputId => {
    const input = document.getElementById(inputId);
    if (input) {
        input.addEventListener('change', (e) => {
            const value = parseFloat(e.target.value);
            const defaultValue = defaultValues[inputId];
            
            // Highlight if value differs from default
            if (value !== defaultValue) {
                e.target.style.backgroundColor = '#fff3cd';
                e.target.style.borderColor = '#ffc107';
            } else {
                e.target.style.backgroundColor = '';
                e.target.style.borderColor = '';
            }
        });
    }
});

// Toggle tariff details section
function toggleTariffDetails() {
    const details = document.getElementById('tariffDetails');
    const icon = document.getElementById('tariffToggleIcon');
    const toggle = document.querySelector('.tariff-toggle');
    
    if (details && icon && toggle) {
        details.classList.toggle('open');
        icon.classList.toggle('open');
        
        const isOpen = details.classList.contains('open');
        toggle.setAttribute('aria-expanded', isOpen);
    }
}

// Get state tax rate for display
function getStateTaxRate(state) {
    const stateTaxRates = {
        'CA': '7.25%',
        'TX': '6.25%',
        'NY': '4.00%',
        'FL': '6.00%',
        'IL': '6.25%',
        'PA': '6.00%',
        'OH': '5.75%',
        'GA': '4.00%',
        'NC': '4.75%',
        'MI': '6.00%'
    };
    return stateTaxRates[state] || '0%';
}

// Keyboard accessibility for tariff toggle
const tariffToggle = document.querySelector('.tariff-toggle');
if (tariffToggle) {
    tariffToggle.addEventListener('keypress', (e) => {
        if (e.key === 'Enter' || e.key === ' ') {
            e.preventDefault();
            toggleTariffDetails();
        }
    });
}
