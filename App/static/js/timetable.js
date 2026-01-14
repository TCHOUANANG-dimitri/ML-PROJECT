/**
 * Timetable Handler
 * Displays courses scheduled by room and time slot
 */

const TIMETABLE_SLOTS = [
  { id: 'morning', label: '7h30–11h30' },
  { id: 'afternoon', label: '12h30–16h30' }
];

const DAYS_OF_WEEK = ['Lundi', 'Mardi', 'Mercredi', 'Jeudi', 'Vendredi', 'Samedi'];

let timetableData = [];

/**
 * Initialize timetable layout
 */
function initializeTimetable() {
  const tbody = document.getElementById('timetableBody');
  if (!tbody) return;
  
  // Create time slot rows
  TIMETABLE_SLOTS.forEach(slot => {
    const tr = document.createElement('tr');
    
    const tdSlot = document.createElement('td');
    tdSlot.textContent = slot.label;
    tdSlot.style.fontWeight = 'bold';
    tr.appendChild(tdSlot);
    
    // Add empty cells for each day
    DAYS_OF_WEEK.forEach(() => {
      const td = document.createElement('td');
      td.className = 'timetable-cell';
      td.setAttribute('data-slot', slot.id);
      tr.appendChild(td);
    });
    
    tbody.appendChild(tr);
  });
}

/**
 * Add a course to timetable (simulated)
 */
function addCourseToTimetable(course) {
  // course: { salle, enseignant, matiere, filiere, jour, heure, effectif }
  const dayIndex = DAYS_OF_WEEK.indexOf(course.jour);
  const tbody = document.getElementById('timetableBody');
  if (!tbody || dayIndex < 0) return;
  
  const rows = tbody.querySelectorAll('tr');
  let targetRow = null;
  
  // Find the row matching the time slot
  rows.forEach(row => {
    const cells = row.querySelectorAll('[data-slot]');
    cells.forEach(cell => {
      if (cell.getAttribute('data-slot') === course.heure) {
        targetRow = row;
      }
    });
  });
  
  if (!targetRow) return;
  
  // Add course to the appropriate day cell
  const cells = targetRow.querySelectorAll('td');
  if (cells[dayIndex + 1]) {
    const courseDiv = document.createElement('div');
    courseDiv.className = 'timetable-course';
    courseDiv.style.padding = '4px';
    courseDiv.style.background = '#e3f2fd';
    courseDiv.style.margin = '2px 0';
    courseDiv.style.borderRadius = '4px';
    courseDiv.style.fontSize = '12px';
    courseDiv.innerHTML = `
      <strong>${course.matiere}</strong><br>
      <small>${course.salle} • ${course.enseignant}</small>
    `;
    cells[dayIndex + 1].appendChild(courseDiv);
  }
}

/**
 * Clear timetable
 */
function clearTimetable() {
  const tbody = document.getElementById('timetableBody');
  if (tbody) {
    tbody.innerHTML = '';
  }
}

/**
 * Handle programmer button click
 * (already defined in main script but enhanced here)
 */
function openProgrammerDialog(roomId, teacherId) {
  // Open a modal or overlay to schedule
  const dialog = document.createElement('div');
  dialog.className = 'modal-overlay';
  dialog.style.cssText = `
    position: fixed;
    top: 0; left: 0;
    width: 100%; height: 100%;
    background: rgba(0,0,0,0.5);
    display: flex;
    align-items: center;
    justify-content: center;
    z-index: 9999;
  `;
  
  const modal = document.createElement('div');
  modal.className = 'modal-content';
  modal.style.cssText = `
    background: white;
    padding: 20px;
    border-radius: 8px;
    max-width: 500px;
    width: 90%;
    box-shadow: 0 4px 12px rgba(0,0,0,0.2);
  `;
  
  modal.innerHTML = `
    <h2>Programmer un cours</h2>
    <form id="programmerForm" style="display: grid; gap: 12px;">
      <div>
        <label>Salle / Enseignant:</label>
        <input type="text" value="${roomId || teacherId || '—'}" disabled style="width: 100%; padding: 8px; border: 1px solid #ccc; border-radius: 4px;">
      </div>
      <div>
        <label>Date:</label>
        <input type="date" id="programDate" style="width: 100%; padding: 8px; border: 1px solid #ccc; border-radius: 4px;">
      </div>
      <div>
        <label>Créneau:</label>
        <select id="programSlot" style="width: 100%; padding: 8px; border: 1px solid #ccc; border-radius: 4px;">
          <option value="morning">7h30–11h30</option>
          <option value="afternoon">12h30–16h30</option>
        </select>
      </div>
      <div style="display: flex; gap: 8px; margin-top: 12px;">
        <button type="submit" class="btn primary" style="flex: 1;">Programmer</button>
        <button type="button" onclick="this.closest('.modal-overlay').remove();" class="btn ghost" style="flex: 1;">Annuler</button>
      </div>
    </form>
  `;
  
  dialog.appendChild(modal);
  document.body.appendChild(dialog);
  
  document.getElementById('programmerForm').addEventListener('submit', function(e) {
    e.preventDefault();
    const date = document.getElementById('programDate').value;
    const slot = document.getElementById('programSlot').value;
    alert(`Programmé pour ${date} à ${slot}`);
    dialog.remove();
  });
}

/**
 * Initialize on DOM ready
 */
document.addEventListener('DOMContentLoaded', function() {
  initializeTimetable();
});
