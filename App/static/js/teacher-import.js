/**
 * Teacher CSV Import Handler
 * Supports: CSV with ; or , delimiters
 * Filters columns and displays results
 */

const TEACHER_COLUMNS = [
  'Matricule_enseignant',
  'Departement',
  'Specialite',
  'Niveau_academique',
  'Disponibilite_hebdomadaire',
  'Heures_totales',
  'Heures_restantes'
];

const TEACHER_DISPLAY_COLUMNS = [
  { key: 'Matricule_enseignant', label: 'Matricule' },
  { key: 'Departement', label: 'Département' },
  { key: 'Specialite', label: 'Spécialité' },
  { key: 'Niveau_academique', label: 'Niveau académique' },
  { key: 'Heures_totales', label: 'Heures totales' },
  { key: 'Heures_restantes', label: 'Heures restantes' }
];

let teacherData = [];

/**
 * Parse CSV string
 */
function parseTeacherCSV(csvText) {
  const hasSemicolon = csvText.includes(';');
  const delimiter = hasSemicolon ? ';' : ',';
  
  const lines = csvText.trim().split('\n');
  if (lines.length < 2) {
    throw new Error('CSV vide ou invalide');
  }
  
  const headers = lines[0].split(delimiter).map(h => h.trim());
  
  const rows = [];
  for (let i = 1; i < lines.length; i++) {
    const parts = lines[i].split(delimiter).map(p => p.trim());
    if (parts.length === 1 && parts[0] === '') continue;
    
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
function filterTeacherColumns(rawRows) {
  return rawRows.map(row => {
    const filtered = {};
    TEACHER_COLUMNS.forEach(col => {
      if (row.hasOwnProperty(col)) {
        filtered[col] = row[col];
      } else {
        const key = Object.keys(row).find(k => k.toLowerCase() === col.toLowerCase());
        filtered[col] = key ? row[key] : '';
      }
    });
    return filtered;
  });
}

/**
 * Update teacher table display
 */
function updateTeacherTable(data) {
  const tbody = document.getElementById('teacherTableBody');
  if (!tbody) return;
  
  tbody.innerHTML = '';
  
  data.forEach(row => {
    const tr = document.createElement('tr');
    TEACHER_DISPLAY_COLUMNS.forEach(col => {
      const td = document.createElement('td');
      const value = row[col.key] || '–';
      td.textContent = value;
      tr.appendChild(td);
    });
    tbody.appendChild(tr);
  });
}

/**
 * Handle teacher file input
 */
function handleTeacherFileInput(event) {
  const file = event.target.files[0];
  if (!file) return;
  
  const reader = new FileReader();
  
  reader.onload = function(e) {
    try {
      const text = e.target.result;
      const rawRows = parseTeacherCSV(text);
      teacherData = filterTeacherColumns(rawRows);
      
      updateTeacherTable(teacherData);
      
      console.log('Enseignants importés:', teacherData.length);
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
  const fileInput = document.getElementById('teacherFileInput');
  if (fileInput) {
    fileInput.addEventListener('change', handleTeacherFileInput);
  }
});
