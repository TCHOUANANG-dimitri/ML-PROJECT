/**
 * Student CSV Import Handler
 * Supports: CSV with ; or , delimiters and Excel files
 * Filters columns and displays results
 */

const STUDENT_COLUMNS = [
  'Matricule',
  'Annee_academique',
  'Niveau',
  'Coefficient',
  'Filiere',
  'Genre',
  'Moyenne_annuelle',
  'Nb_matieres_validees',
  'Nb_heures_cours',
  'Nb_heures_presence',
  'Nb_projets'
];

const STUDENT_DISPLAY_COLUMNS = [
  { key: 'Matricule', label: 'Matricule' },
  { key: 'Niveau', label: 'Niveau' },
  { key: 'Filiere', label: 'Filière' },
  { key: 'Moyenne_annuelle', label: 'Moyenne annuelle' },
  { key: 'Nb_matieres_validees', label: 'Matières validées' },
  { key: 'Nb_heures_presence', label: 'Heures présence' },
  { key: 'Nb_projets', label: 'Nb projets' }
];

let studentData = [];

/**
 * Parse CSV string
 * Supports both ; and , delimiters
 */
function parseCSV(csvText) {
  // Detect delimiter
  const hasSemicolon = csvText.includes(';');
  const delimiter = hasSemicolon ? ';' : ',';
  
  const lines = csvText.trim().split('\n');
  if (lines.length < 2) {
    throw new Error('CSV vide ou invalide');
  }
  
  // Parse headers
  const headers = lines[0].split(delimiter).map(h => h.trim());
  
  // Parse rows
  const rows = [];
  for (let i = 1; i < lines.length; i++) {
    const parts = lines[i].split(delimiter).map(p => p.trim());
    if (parts.length === 1 && parts[0] === '') continue; // skip empty lines
    
    const row = {};
    headers.forEach((header, idx) => {
      row[header] = parts[idx] || '';
    });
    rows.push(row);
  }
  
  return rows;
}

/**
 * Filter columns from raw data
 */
function filterColumns(rawRows) {
  return rawRows.map(row => {
    const filtered = {};
    STUDENT_COLUMNS.forEach(col => {
      // Try exact match first
      if (row.hasOwnProperty(col)) {
        filtered[col] = row[col];
      } else {
        // Try case-insensitive match
        const key = Object.keys(row).find(k => k.toLowerCase() === col.toLowerCase());
        filtered[col] = key ? row[key] : '';
      }
    });
    return filtered;
  });
}

/**
 * Compute global indicators
 */
function computeIndicators(data) {
  const total = data.length;
  
  // Moyenne générale
  const moyennes = data.map(s => {
    const val = parseFloat(s.Moyenne_annuelle) || 0;
    return val;
  });
  const generalAverage = total > 0 ? (moyennes.reduce((a, b) => a + b, 0) / total).toFixed(2) : 0;
  
  // Taux de réussite (rules: niv3+ : >=60 crédits, niv1-2: >=45 crédits)
  // Assuming Nb_matieres_validees * 10 = credits approximation, or use Nb_matieres_validees directly
  let successCount = 0;
  data.forEach(s => {
    const niveau = parseInt(s.Niveau) || 0;
    const credits = parseInt(s.Nb_matieres_validees) || 0;
    let isSuccess = false;
    
    if (niveau >= 3) {
      isSuccess = credits >= 6; // approx 60 crédits = 6 matières
    } else if (niveau === 1 || niveau === 2) {
      isSuccess = credits >= 4; // approx 45 crédits = 4.5 matières
    }
    
    if (isSuccess) successCount++;
  });
  const successRate = total > 0 ? ((successCount / total) * 100).toFixed(1) : 0;
  
  return {
    total,
    generalAverage,
    successRate,
    successCount
  };
}

/**
 * Update table display
 */
function updateStudentTable(data) {
  const tbody = document.getElementById('studentTableBody');
  if (!tbody) return;
  
  tbody.innerHTML = '';
  
  data.forEach(row => {
    const tr = document.createElement('tr');
    STUDENT_DISPLAY_COLUMNS.forEach(col => {
      const td = document.createElement('td');
      const value = row[col.key] || '–';
      td.textContent = value;
      tr.appendChild(td);
    });
    tbody.appendChild(tr);
  });
}

/**
 * Update indicators display
 */
function updateIndicators(indicators) {
  document.getElementById('statTotalStudents').textContent = indicators.total;
  document.getElementById('statGeneralAverage').textContent = indicators.generalAverage + ' / 20';
  document.getElementById('statSuccessRate').textContent = indicators.successRate + ' %';
}

/**
 * Draw charts using Canvas (simple bar chart)
 */
function drawCharts(data) {
  // Chart 1: Distribution of averages (histogram)
  drawAverageHistogram(data);
  
  // Chart 2: Success rate by level
  drawSuccessByLevel(data);
}

function drawAverageHistogram(data) {
  const canvas = document.getElementById('chartAverages');
  if (!canvas) return;
  
  const ctx = canvas.getContext('2d');
  const averages = data.map(s => parseFloat(s.Moyenne_annuelle) || 0);
  
  // Bins: 0-5, 5-10, 10-15, 15-20
  const bins = [0, 0, 0, 0];
  averages.forEach(avg => {
    if (avg < 5) bins[0]++;
    else if (avg < 10) bins[1]++;
    else if (avg < 15) bins[2]++;
    else bins[3]++;
  });
  
  // Simple bar chart
  const barWidth = canvas.width / 4;
  const maxBin = Math.max(...bins);
  const scale = (canvas.height - 40) / (maxBin || 1);
  
  ctx.clearRect(0, 0, canvas.width, canvas.height);
  ctx.fillStyle = '#007bff';
  ctx.strokeStyle = '#333';
  ctx.lineWidth = 1;
  
  bins.forEach((count, idx) => {
    const x = idx * barWidth + 10;
    const barHeight = count * scale;
    const y = canvas.height - 30 - barHeight;
    
    ctx.fillRect(x, y, barWidth - 20, barHeight);
    ctx.strokeRect(x, y, barWidth - 20, barHeight);
    
    // Label
    ctx.fillStyle = '#333';
    ctx.font = '12px Arial';
    ctx.textAlign = 'center';
    const labels = ['0–5', '5–10', '10–15', '15–20'];
    ctx.fillText(labels[idx], x + (barWidth - 20) / 2, canvas.height - 10);
    ctx.fillText(count.toString(), x + (barWidth - 20) / 2, y - 5);
  });
  
  ctx.fillStyle = '#007bff';
}

function drawSuccessByLevel(data) {
  const canvas = document.getElementById('chartMajors');
  if (!canvas) return;
  
  const ctx = canvas.getContext('2d');
  
  // Group by level and count successes
  const levels = {};
  data.forEach(s => {
    const niveau = parseInt(s.Niveau) || 0;
    if (!levels[niveau]) levels[niveau] = { total: 0, success: 0 };
    levels[niveau].total++;
    
    const credits = parseInt(s.Nb_matieres_validees) || 0;
    let isSuccess = false;
    if (niveau >= 3) {
      isSuccess = credits >= 6;
    } else if (niveau === 1 || niveau === 2) {
      isSuccess = credits >= 4;
    }
    if (isSuccess) levels[niveau].success++;
  });
  
  const levelKeys = Object.keys(levels).sort();
  const successRates = levelKeys.map(k => {
    const lvl = levels[k];
    return lvl.total > 0 ? (lvl.success / lvl.total) * 100 : 0;
  });
  
  // Draw bars
  const barWidth = canvas.width / (levelKeys.length || 1);
  
  ctx.clearRect(0, 0, canvas.width, canvas.height);
  ctx.fillStyle = '#28a745';
  ctx.strokeStyle = '#333';
  ctx.lineWidth = 1;
  
  levelKeys.forEach((level, idx) => {
    const rate = successRates[idx];
    const x = idx * barWidth + 10;
    const barHeight = (rate / 100) * (canvas.height - 40);
    const y = canvas.height - 30 - barHeight;
    
    ctx.fillRect(x, y, barWidth - 20, barHeight);
    ctx.strokeRect(x, y, barWidth - 20, barHeight);
    
    // Label
    ctx.fillStyle = '#333';
    ctx.font = '12px Arial';
    ctx.textAlign = 'center';
    ctx.fillText('Niv ' + level, x + (barWidth - 20) / 2, canvas.height - 10);
    ctx.fillText(rate.toFixed(0) + '%', x + (barWidth - 20) / 2, y - 5);
  });
}

/**
 * Handle file input change
 */
function handleStudentFileInput(event) {
  const file = event.target.files[0];
  if (!file) return;
  
  const reader = new FileReader();
  
  reader.onload = function(e) {
    try {
      const text = e.target.result;
      
      // Parse CSV
      const rawRows = parseCSV(text);
      
      // Filter columns
      studentData = filterColumns(rawRows);
      
      // Compute indicators
      const indicators = computeIndicators(studentData);
      
      // Update UI
      updateStudentTable(studentData);
      updateIndicators(indicators);
      drawCharts(studentData);
      
      console.log('Étudiants importés:', studentData.length);
    } catch (error) {
      console.error('Erreur lors du parsing:', error);
      alert('Erreur lors du parsing du fichier: ' + error.message);
    }
  };
  
  reader.readAsText(file, 'UTF-8');
}

/**
 * Initialize on DOM ready
 */
document.addEventListener('DOMContentLoaded', function() {
  const fileInput = document.getElementById('studentFileInput');
  if (fileInput) {
    fileInput.addEventListener('change', handleStudentFileInput);
  }
});
