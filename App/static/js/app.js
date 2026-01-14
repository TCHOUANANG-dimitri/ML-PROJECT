 // Simple in-memory datasets (rooms, teachers, filières/matières) -----------------------

 // Les données filieresMatieres seront remplacées par MATIERES_BY_LEVEL du serveur Django
 // Ceci est un fallback en cas où les données ne sont pas disponibles
 const filieresData = (typeof MATIERES_BY_LEVEL !== 'undefined') ? MATIERES_BY_LEVEL : {
   "TRONC COMMUN": {
     1: [
       "Mathématiques Générales I",
       "Physique Générale I",
       "Chimie Générale",
       "Informatique de base",
       "Algèbre Linéaire",
       "Mécanique du point",
       "Communication",
       "Dessin technique",
     ],
     2: [
       "Mathématiques Générales II",
       "Physique Générale II",
       "Électricité",
       "Programmation C",
       "Analyse Numérique",
       "Thermodynamique",
       "Probabilités et Statistiques",
       "Anglais technique",
     ],
   },
   GIT: {
     3: [
       "Algorithmique Avancée",
       "Bases de données",
       "Réseaux et Protocoles",
       "Génie Logiciel",
       "Systèmes d'exploitation",
       "Architecture des ordinateurs",
       "Programmation orientée objet",
       "Mathématiques pour l'informatique",
     ],
     4: [
       "Sécurité informatique",
       "Développement web",
       "Intelligence Artificielle",
       "Réseaux avancés",
       "Systèmes distribués",
       "Compilation",
       "Administration systèmes",
       "Gestion de projets informatiques",
     ],
     5: [
       "Cloud Computing",
       "Cybersécurité",
       "Architecture logicielle",
       "Blockchain",
       "IoT et systèmes embarqués",
       "DevOps",
       "Big Data et Analytics",
       "Entrepreneuriat Tech",
     ],
   },
   SDIA: {
     3: [
       "Machine Learning",
       "Data Mining",
       "Statistiques Avancées",
       "Programmation Python",
       "Bases de données NoSQL",
       "Algèbre linéaire appliquée",
       "Visualisation de données",
       "Collecte et traitement de données",
     ],
     4: [
       "Deep Learning",
       "Big Data",
       "Traitement automatique des langues",
       "Vision par ordinateur",
       "Optimisation",
       "Séries temporelles",
       "Apprentissage par renforcement",
       "Éthique de l'IA",
     ],
     5: [
       "IA Générative",
       "MLOps",
       "Recommandation Systems",
       "Graph Neural Networks",
       "IA Explicable",
       "Data Engineering",
       "Recherche opérationnelle",
       "Projet de fin d'études",
     ],
   },
   GCI: {
     3: [
       "Résistance des Matériaux",
       "Mécanique des sols",
       "Topographie",
       "Matériaux de construction",
       "Hydraulique générale",
       "Dessin assisté par ordinateur",
       "Béton armé I",
       "Géotechnique I",
     ],
     4: [
       "Béton armé II",
       "Structures Métalliques",
       "Géotechnique II",
       "Hydraulique appliquée",
       "Routes et terrassements",
       "Calcul des structures",
       "Ouvrages d'art",
       "VRD",
     ],
     5: [
       "Construction métallique avancée",
       "Dynamique des structures",
       "Fondations spéciales",
       "Barrages",
       "Pathologie des constructions",
       "BIM et maquette numérique",
       "Gestion de chantier",
       "Projet de fin d'études",
     ],
   },
   // Additional filières placeholders so selects can be populated dynamically.
   GM: { 3: [], 4: [], 5: [] },
   GPR: { 3: [], 4: [], 5: [] },
   GE: { 3: [], 4: [], 5: [] },
   GESI: { 3: [], 4: [], 5: [] },
   GMP: { 3: [], 4: [], 5: [] },
   GAM: { 3: [], 4: [], 5: [] },
   GQHSE: { 3: [], 4: [], 5: [] },
   METEO: { 3: [], 4: [], 5: [] },
   MEMA: { 3: [], 4: [], 5: [] },
   CIBI: { 3: [], 4: [], 5: [] },
   GEE: { 3: [], 4: [], 5: [] },
   ENERGIE: { 3: [], 4: [], 5: [] },
   EEAT: { 3: [], 4: [], 5: [] },
 };

const rooms = [
  { id: 1, name: "Amphi A", capacity: 220 },
  { id: 2, name: "Amphi B", capacity: 180 },
  { id: 3, name: "Salle Info 1", capacity: 40 },
  { id: 4, name: "Salle Info 2", capacity: 35 },
  { id: 5, name: "Salle TD 101", capacity: 60 },
  { id: 6, name: "Lab IA", capacity: 30 },
];

const teachers = [
  {
    id: 1,
    matricule: "ENS-001",
    name: "Dr. N. Talla",
    filieres: ["GIT", "SDIA"],
    subjects: ["Intelligence Artificielle", "Machine Learning"],
    speciality: "IA",
    hoursPlanned: 120,
    hoursDone: 40,
  },
  {
    id: 2,
    matricule: "ENS-002",
    name: "Pr. M. Mbarga",
    filieres: ["TRONC COMMUN", "GCI"],
    subjects: ["Mathématiques Générales I", "Résistance des Matériaux"],
    speciality: "Mathématiques / Structures",
    hoursPlanned: 160,
    hoursDone: 90,
  },
  {
    id: 3,
    matricule: "ENS-003",
    name: "Dr. A. Ngono",
    filieres: ["GIT"],
    subjects: ["Développement web", "Bases de données"],
    speciality: "Informatique",
    hoursPlanned: 140,
    hoursDone: 60,
  },
  {
    id: 4,
    matricule: "ENS-004",
    name: "Dr. J. Ekane",
    filieres: ["SDIA"],
    subjects: ["Data Mining", "Big Data"],
    speciality: "Data / IA",
    hoursPlanned: 140,
    hoursDone: 110,
  },
];

teachers.forEach((t) => {
  t.hoursRemaining = t.hoursPlanned - t.hoursDone;
});

const timetableSlots = [
  { id: "AM", label: "07h30 – 11h30" },
  { id: "PM", label: "12h30 – 16h30" },
];

const days = ["Lundi", "Mardi", "Mercredi", "Jeudi", "Vendredi", "Samedi"];

// In-memory timetable (day -> slotId -> entry)
const timetable = {};
days.forEach((d) => {
  timetable[d] = {};
  timetableSlots.forEach((s) => {
    timetable[d][s.id] = null;
  });
});

 // Student dataset and loading state
 // The dashboard will remain placeholder until a student file is imported.
 let studentSample = [];
 let studentsLoaded = false;

// Navigation -------------------------------------------------------------------

function initNavigation() {
  const sidebar = document.getElementById("sidebar");
  const sidebarLogo = document.getElementById("sidebarLogo");
  const sidebarItems = Array.from(document.querySelectorAll(".sidebar-item"));
  const pages = Array.from(document.querySelectorAll(".page"));

  if (sidebarLogo && sidebar) {
    sidebarLogo.addEventListener("click", () => {
      sidebar.classList.toggle("collapsed");
    });
  }

  sidebarItems.forEach((btn) => {
    btn.addEventListener("click", () => {
      const page = btn.dataset.page;
      activatePage(page);
    });

    // simple tooltip via title based on label text (for collapsed mode)
    const label = btn.querySelector(".label");
    if (label) {
      btn.title = label.textContent.trim();
    }
  });

  document
    .querySelectorAll("[data-page-target]")
    .forEach((btn) =>
      btn.addEventListener("click", () =>
        activatePage(btn.getAttribute("data-page-target"))
      )
    );
}

function activatePage(pageName) {
  const sidebarItems = Array.from(document.querySelectorAll(".sidebar-item"));
  const pages = Array.from(document.querySelectorAll(".page"));
  
  sidebarItems.forEach((b) =>
    b.classList.toggle("active", b.dataset.page === pageName)
  );
  pages.forEach((p) =>
    p.classList.toggle("active", p.id === `page-${pageName}`)
  );
}

// Dashboard --------------------------------------------------------------------

function refreshDashboard() {
  const tbody = document.getElementById("studentTableBody");
  tbody.innerHTML = "";

  // If no student file imported yet, show placeholder + keep charts/stats empty
  if (!studentsLoaded) {
    // placeholder row explaining import
    const noteRow = document.createElement("tr");
    noteRow.innerHTML = `<td colspan="8" style="font-size:13px;color:#6b7280;padding:16px 12px;">
      Aucune liste d'étudiants importée — importez un fichier CSV / Excel pour afficher le tableau, les graphiques et les indicateurs.
    </td>`;
    tbody.appendChild(noteRow);

    // clear statistics
    document.getElementById("statTotalStudents").textContent = "–";
    document.getElementById("statGeneralAverage").textContent = "– / 20";
    document.getElementById("statSuccessRate").textContent = "– %";

    // clear charts
    drawMajorsPie({});
    drawAveragesBars([]);
    return;
  }

  // compute global stats from full dataset
  let sum = 0;
  let successCount = 0;
  const filiereCounts = {};

  studentSample.forEach((s) => {
    if (!isNaN(parseFloat(s.avg))) {
      sum += parseFloat(s.avg);
    }
    if (s.status === "Admis") successCount++;
    if (s.filiere) filiereCounts[s.filiere] = (filiereCounts[s.filiere] || 0) + 1;
  });

  const total = studentSample.length || 1;
  const avgGeneral = studentSample.filter(s => !isNaN(parseFloat(s.avg))).length ? (sum / studentSample.filter(s => !isNaN(parseFloat(s.avg))).length) : 0;

  document.getElementById("statTotalStudents").textContent = studentSample.length;
  document.getElementById("statGeneralAverage").textContent = `${avgGeneral.toFixed(1)} / 20`;
  document.getElementById("statSuccessRate").textContent = `${((successCount / total) * 100).toFixed(1)} %`;

  // Show only a small random sample (3 rows) in the table for clarity
  const sampleCount = Math.min(3, studentSample.length);
  const shuffled = [...studentSample].sort(() => 0.5 - Math.random());
  const sample = shuffled.slice(0, sampleCount);

  sample.forEach((s) => {
    const tr = document.createElement("tr");
    // render status as a colored badge: green checked square for Admis, red crossed square for Echec
    const statusClass =
      s.status === "Admis" ? "admis" : s.status === "Echec" ? "echec" : "neutral";
    const statusContent =
      s.status === "Admis" ? "✔" : s.status === "Echec" ? "✖" : (s.status || "–");

    tr.innerHTML = `
      <td>${s.id}</td>
      <td>${s.name || "–"}</td>
      <td>${(s.avg !== undefined && s.avg !== null) ? parseFloat(s.avg).toFixed(1) : "–"}</td>
      <td>${s.presence !== undefined && s.presence !== null ? s.presence + "%" : "–"}</td>
      <td>${s.projects !== undefined ? s.projects : "–"}</td>
      <td>${s.distance || "–"}</td>
      <td>${s.travaille || "–"}</td>
      <td><span class="status-badge ${statusClass}">${statusContent}</span></td>
    `;
    tbody.appendChild(tr);
  });

  // add a small note indicating the table is an aléatoire échantillon
  let noteRow = document.getElementById("studentSampleNoteRow");
  if (!noteRow) {
    noteRow = document.createElement("tr");
    noteRow.id = "studentSampleNoteRow";
    noteRow.innerHTML = `<td colspan="6" style="font-size:12px;color:#6b7280;padding:8px 10px;">Affiche ${sampleCount} étudiants (échantillon aléatoire). Importez un fichier pour voir la liste complète.</td>`;
    tbody.appendChild(noteRow);
  }

  // Draw charts using full dataset
  drawMajorsPie(filiereCounts);
  drawAveragesBars(studentSample);
}

// Recommendation form ----------------------------------------------------------

// NOTE: Don't query these at module level - wait for DOM to be ready!
let recFiliereSelect = null;
let recNiveauSelect = null;
let recMatiereSelect = null;

function populateFiliereSelects() {
  // Recommendation filière
  if (!recFiliereSelect) recFiliereSelect = document.getElementById("rec-filiere");
  if (!recFiliereSelect) return; // DOM not ready
  
  recFiliereSelect.innerHTML = `<option value="">Sélectionner</option>`;
  Object.keys(filieresData).forEach((f) => {
    const opt = document.createElement("option");
    opt.value = f;
    opt.textContent = f;
    recFiliereSelect.appendChild(opt);
  });
}

function populateMatiereOptions() {
  if (!recFiliereSelect || !recNiveauSelect || !recMatiereSelect) return;
  const filiere = recFiliereSelect.value;
  const level = recNiveauSelect.value ? parseInt(recNiveauSelect.value, 10) : null;

  recMatiereSelect.innerHTML =
    '<option value="">Choisir une matière</option>';

  if (!filiere || !level || !filieresData[filiere] || !filieresData[filiere][level]) return;
  const subjects = filieresData[filiere][level] || [];
  subjects.forEach((m) => {
    const opt = document.createElement("option");
    opt.value = m;
    opt.textContent = m;
    recMatiereSelect.appendChild(opt);
  });
}

function initRecommendationForm() {
  // Get form elements AFTER DOM is ready - utiliser les IDs avec préfixe 'rec-'
  recFiliereSelect = document.getElementById("rec-filiere");
  recNiveauSelect = document.getElementById("rec-niveau");
  recMatiereSelect = document.getElementById("rec-nom_matiere");
  
  if (recFiliereSelect && recNiveauSelect && recMatiereSelect) {
    recFiliereSelect.addEventListener("change", populateMatiereOptions);
    recNiveauSelect.addEventListener("change", populateMatiereOptions);
  }
}

let recommendationForm = null;
let recommendationResults = null;
let roomRecommendationsDiv = null;
let teacherRecommendationsDiv = null;

// Simple heuristic "IA" for recommendations
function recommendRooms(effectif) {
  const sorted = rooms
    .filter((r) => r.capacity >= effectif)
    .sort((a, b) => a.capacity - b.capacity);
  return (sorted.length ? sorted : rooms).slice(0, 3);
}

function recommendTeachers({ filiere, matiere }) {
  const candidates = teachers
    .map((t) => ({ ...t }))
    .sort((a, b) => a.hoursRemaining - b.hoursRemaining); // prioriser ceux qui ont plus d'heures restantes?

  // Score function based on speciality, filière and subject match
  const scored = candidates.map((t) => {
    let score = 0;
    if (t.filieres.includes(filiere)) score += 2;
    if (t.subjects.includes(matiere)) score += 3;
    if (t.hoursRemaining > 0) score += 1;
    if (t.hoursRemaining < 10) score -= 2;
    return { ...t, score };
  });

  scored.sort((a, b) => b.score - a.score);
  return scored.slice(0, 3);
}

// Program a course into timetable and update teacher hours
function programCourse({ day, slotId, courseData }) {
  // No overlap, one room & one teacher per slot
  const existing = timetable[day][slotId];
  if (existing) {
    return { ok: false, reason: "Créneau déjà occupé." };
  }

  // capacity & teacher hours already ensured at recommendation level
  timetable[day][slotId] = courseData;

  // Update teacher hours
  const teacher = teachers.find((t) => t.id === courseData.teacherId);
  if (teacher) {
    teacher.hoursDone += courseData.durationHours;
    teacher.hoursRemaining = teacher.hoursPlanned - teacher.hoursDone;
  }

  refreshTimetable();
  refreshTeachersTable();

  return { ok: true };
}

function handleRecommendationSubmit(e) {
  e.preventDefault();
  if (!recFiliereSelect || !recNiveauSelect || !recMatiereSelect) return;
  
  // Utiliser les vrais IDs du formulaire HTML avec préfixe 'rec-'
  const filiere = document.getElementById("rec-filiere").value;
  const niveau = document.getElementById("rec-niveau").value;
  const matiere = document.getElementById("rec-nom_matiere").value;
  const type = document.getElementById("rec-Type_cours").value;
  const effectif = parseInt(document.getElementById("rec-Nb_personnes").value, 10);
  const jour = document.getElementById("rec-jour").value;
  const heure = document.getElementById("rec-heure").value;

  if (!filiere || !niveau || !matiere || !type || !effectif)
    return;

  // Envoyer au serveur Django
  const formData = new FormData();
  formData.append("filiere", filiere);
  formData.append("niveau", niveau);
  formData.append("nom_matiere", matiere);
  formData.append("Type_cours", type);
  formData.append("Nb_personnes", effectif);
  formData.append("jour", jour);
  formData.append("heure", heure);
  formData.append("besoin_projecteur", document.getElementById("rec-besoin_projecteur").value);

  fetch("/recommendation/", {
    method: "POST",
    headers: {
      "X-CSRFToken": document.querySelector("[name=csrfmiddlewaretoken]").value,
      "X-Requested-With": "XMLHttpRequest"
    },
    body: formData
  })
  .then(response => response.json())
  .then(data => {
    if (data.rooms && data.teachers) {
      renderRoomRecommendations(data.rooms, {
        filiere,
        niveau,
        matiere,
        type,
        effectif,
        jour,
        heure,
      });
      renderTeacherRecommendations(data.teachers, {
        filiere,
        niveau,
        matiere,
        type,
        effectif,
        jour,
        heure,
      });

      if (recommendationResults) {
        recommendationResults.style.display = "block";
      }
    }
  })
  .catch(error => console.error("Erreur:", error));
}

/**
 * Fonction pour programmer une salle ou un enseignant
 * @param {HTMLElement} button - Le bouton cliqué
 * @param {string} type - 'room' ou 'teacher'
 */
function openProgrammer(button, type) {
  // Récupérer les données de la recommandation
  const dataAttr = type === 'room' ? 'data-room' : 'data-teacher';
  const nameAttr = type === 'room' ? 'data-room-name' : 'data-teacher-name';
  
  const id = button.getAttribute(dataAttr);
  const name = button.getAttribute(nameAttr);
  
  if (!id || !name) {
    alert("Données manquantes pour cette recommandation");
    return;
  }

  // Récupérer les données du formulaire
  const filiere = document.getElementById("rec-filiere").value;
  const niveau = document.getElementById("rec-niveau").value;
  const matiere = document.getElementById("rec-nom_matiere").value;
  const typeSeance = document.getElementById("rec-Type_cours").value;
  const effectif = parseInt(document.getElementById("rec-Nb_personnes").value, 10);
  const jour = document.getElementById("rec-jour").value;
  const heure = document.getElementById("rec-heure").value;

  if (!filiere || !niveau || !matiere || !jour || !heure) {
    alert("Veuillez d'abord remplir les champs obligatoires du formulaire");
    return;
  }

  // Créer une boîte de dialogue pour confirmer et sélectionner le créneau
  const modal = document.createElement("div");
  modal.className = "modal";
  modal.style.cssText = "position:fixed;top:0;left:0;width:100%;height:100%;background:rgba(0,0,0,0.5);display:flex;align-items:center;justify-content:center;z-index:10000;";
  
  const content = document.createElement("div");
  content.className = "modal-content";
  content.style.cssText = "background:white;padding:24px;border-radius:8px;max-width:400px;box-shadow:0 4px 12px rgba(0,0,0,0.15);";
  
  const title = document.createElement("h3");
  title.textContent = `Programmer ${type === 'room' ? 'salle' : 'enseignant'}`;
  title.style.marginBottom = "16px";
  
  const info = document.createElement("div");
  info.style.cssText = "background:#f5f5f5;padding:12px;border-radius:4px;margin-bottom:16px;font-size:14px;";
  info.innerHTML = `
    <strong>${type === 'room' ? 'Salle' : 'Enseignant'}:</strong> ${name}<br/>
    <strong>Matière:</strong> ${matiere}<br/>
    <strong>Filière/Niveau:</strong> ${filiere} - Niveau ${niveau}<br/>
    <strong>Type:</strong> ${typeSeance}<br/>
    <strong>Effectif:</strong> ${effectif} étudiants<br/>
    <strong>Date:</strong> ${jour}
  `;
  
  const slotLabel = document.createElement("label");
  slotLabel.textContent = "Sélectionner un créneau:";
  slotLabel.style.cssText = "display:block;margin-bottom:8px;font-weight:bold;";
  
  const slotSelect = document.createElement("select");
  slotSelect.style.cssText = "width:100%;padding:8px;margin-bottom:16px;border:1px solid #ddd;border-radius:4px;";
  
  // Ajouter les créneaux disponibles
  const options = [
    { value: "morning", text: "Matin (7:30 - 11:30)" },
    { value: "afternoon", text: "Après-midi (12:30 - 16:30)" }
  ];
  
  options.forEach(opt => {
    const option = document.createElement("option");
    option.value = opt.value;
    option.textContent = opt.text;
    slotSelect.appendChild(option);
  });
  
  const buttons = document.createElement("div");
  buttons.style.cssText = "display:flex;gap:8px;justify-content:flex-end;";
  
  const cancelBtn = document.createElement("button");
  cancelBtn.textContent = "Annuler";
  cancelBtn.className = "btn";
  cancelBtn.style.cssText = "padding:8px 16px;background:#f0f0f0;border:1px solid #ddd;border-radius:4px;cursor:pointer;";
  cancelBtn.onclick = () => modal.remove();
  
  const confirmBtn = document.createElement("button");
  confirmBtn.textContent = "Confirmer";
  confirmBtn.className = "btn primary";
  confirmBtn.style.cssText = "padding:8px 16px;background:#007bff;color:white;border:none;border-radius:4px;cursor:pointer;";
  confirmBtn.onclick = () => {
    const slot = slotSelect.value;
    const day = jour ? new Date(jour).toLocaleDateString('fr-FR', { weekday: 'long' }) : "Lundi";
    
    const courseData = {
      matiere,
      filiere,
      niveau,
      type: typeSeance,
      effectif,
      [type === 'room' ? 'roomId' : 'teacherId']: id,
      [type === 'room' ? 'roomName' : 'teacherName']: name
    };
    
    const result = programCourse({
      day: day.charAt(0).toUpperCase() + day.slice(1),
      slotId: slot,
      courseData
    });
    
    if (result.ok) {
      alert(`✓ ${type === 'room' ? 'Salle' : 'Enseignant'} programmé(e) avec succès!`);
      modal.remove();
      // Aller à la section emploi du temps
      const timetableSection = document.getElementById("page-timetable");
      if (timetableSection) {
        timetableSection.scrollIntoView({ behavior: 'smooth' });
      }
    } else {
      alert(`✗ Erreur: ${result.reason}`);
    }
  };
  
  buttons.appendChild(cancelBtn);
  buttons.appendChild(confirmBtn);
  
  content.appendChild(title);
  content.appendChild(info);
  content.appendChild(slotLabel);
  content.appendChild(slotSelect);
  content.appendChild(buttons);
  
  modal.appendChild(content);
  document.body.appendChild(modal);
  
  // Fermer avec Échap
  document.addEventListener("keydown", (e) => {
    if (e.key === "Escape") modal.remove();
  });
}

// Attach form listener after DOM is ready
function attachRecommendationFormListener() {
  recommendationForm = document.getElementById("recommendationForm");
  recommendationResults = document.getElementById("recommendationResults");
  roomRecommendationsDiv = document.getElementById("roomRecommendations");
  teacherRecommendationsDiv = document.getElementById("teacherRecommendations");
  
  if (recommendationForm) {
    recommendationForm.addEventListener("submit", handleRecommendationSubmit);
  }

  // Ajouter les event listeners aux boutons Programmer
  document.addEventListener("click", (e) => {
    if (e.target && e.target.classList && e.target.classList.contains("program-btn")) {
      const button = e.target;
      const isRoom = button.hasAttribute("data-room");
      const type = isRoom ? "room" : "teacher";
      openProgrammer(button, type);
    }
  });
}

function renderRoomRecommendations(list, context) {
  if (!roomRecommendationsDiv) roomRecommendationsDiv = document.getElementById("roomRecommendations");
  if (!roomRecommendationsDiv) return;
  
  roomRecommendationsDiv.innerHTML = "";
  list.forEach((room, index) => {
    const wrapper = document.createElement("div");
    wrapper.className = "recommendation-item";
    wrapper.innerHTML = `
      <div class="recommendation-main">
        <div class="recommendation-name">${index + 1}. ${
      room.name
    }</div>
        <div class="recommendation-meta">Capacité : ${room.capacity} étudiants</div>
      </div>
      <button class="btn ghost btn-program-room" data-room-id="${
        room.id
      }">Programmer</button>
    `;
    roomRecommendationsDiv.appendChild(wrapper);
  });

  roomRecommendationsDiv
    .querySelectorAll(".btn-program-room")
    .forEach((btn) => {
      btn.addEventListener("click", () => {
        const roomId = parseInt(btn.dataset.roomId, 10);
        openQuickScheduleModal({ ...context, roomId });
      });
    });
}

function renderTeacherRecommendations(list, context) {
  teacherRecommendationsDiv.innerHTML = "";
  list.forEach((t, index) => {
    const wrapper = document.createElement("div");
    wrapper.className = "recommendation-item";
    const alertLow =
      t.hoursRemaining <= 0
        ? '<span class="chip-alert">Charge complète</span>'
        : t.hoursRemaining < 5
        ? '<span class="chip-alert">Heures restantes faibles</span>'
        : "";
    wrapper.innerHTML = `
      <div class="recommendation-main">
        <div class="recommendation-name">${index + 1}. ${
      t.name
    }</div>
        <div class="recommendation-meta">
          Spécialité : ${t.speciality} • Heures restantes : ${
      t.hoursRemaining
    }h
        </div>
        ${alertLow}
      </div>
      <button class="btn ghost btn-program-teacher" data-teacher-id="${
        t.id
      }" ${t.hoursRemaining <= 0 ? "disabled" : ""}>Programmer</button>
    `;
    teacherRecommendationsDiv.appendChild(wrapper);
  });

  teacherRecommendationsDiv
    .querySelectorAll(".btn-program-teacher")
    .forEach((btn) => {
      btn.addEventListener("click", () => {
        const teacherId = parseInt(btn.dataset.teacherId, 10);
        openQuickScheduleModal({ ...context, teacherId });
      });
    });
}

// Quick scheduling modal (simple prompt-based for now to stay minimal) ----------
function openQuickScheduleModal(context) {
  const day = prompt(
    "Jour pour la programmation (Lundi, Mardi, Mercredi, Jeudi, Vendredi, Samedi) :",
    "Lundi"
  );
  if (!day || !days.includes(day)) return;

  const slotLabel = prompt(
    "Créneau (AM pour 07h30 – 11h30, PM pour 12h30 – 16h30) :",
    "AM"
  );
  const slotId = slotLabel === "PM" ? "PM" : "AM";

  const durationHours = slotId === "AM" ? 4 : 4; // simplification
  const teacherId =
    context.teacherId ||
    (teachers.find((t) =>
      t.subjects.includes(context.matiere)
    )?.id || teachers[0].id);
  const roomId =
    context.roomId ||
    (rooms.find((r) => r.capacity >= context.effectif)?.id || rooms[0].id);

  const teacher = teachers.find((t) => t.id === teacherId);
  if (!teacher) return;
  if (teacher.hoursRemaining < durationHours) {
    alert(
      `Impossible de programmer ${teacher.name} : heures restantes (${teacher.hoursRemaining}h) insuffisantes pour un cours de ${durationHours}h.`
    );
    return;
  }

  const room = rooms.find((r) => r.id === roomId);
  if (!room) return;
  if (room.capacity < context.effectif) {
    alert(
      `Impossible de programmer dans ${room.name} : capacité insuffisante (${room.capacity} < ${context.effectif}).`
    );
    return;
  }

  const res = programCourse({
    day,
    slotId,
    courseData: {
      filiere: context.filiere,
      niveau: context.niveau,
      matiere: context.matiere,
      type: context.type,
      effectif: context.effectif,
      date: context.date,
      teacherId,
      teacherName: teacher.name,
      roomId,
      roomName: room.name,
      durationHours,
    },
  });

  if (!res.ok) {
    alert(`Programmation impossible : ${res.reason}`);
  } else {
    alert("Cours programmé avec succès dans l'emploi du temps.");
  }
}

// Timetable rendering ----------------------------------------------------------

function refreshTimetable() {
  const tbody = document.getElementById("timetableBody");
  tbody.innerHTML = "";

  timetableSlots.forEach((slot) => {
    const tr = document.createElement("tr");
    const firstTd = document.createElement("td");
    firstTd.textContent = slot.label;
    tr.appendChild(firstTd);

    days.forEach((day) => {
      const td = document.createElement("td");
      const entry = timetable[day][slot.id];
      if (entry) {
        td.className = "slot-cell";
        td.innerHTML = `
          <div class="slot-course">${entry.matiere} (${entry.type})</div>
          <div class="slot-meta">${entry.filiere} • Niveau ${entry.niveau}</div>
          <div class="slot-meta">${entry.roomName} • ${entry.teacherName}</div>
        `;
      } else {
        td.className = "slot-cell";
        td.style.color = "#9ca3af";
        td.textContent = "—";
      }
      tr.appendChild(td);
    });

    tbody.appendChild(tr);
  });
}

// Teachers table ---------------------------------------------------------------

function refreshTeachersTable() {
  const tbody = document.getElementById("teacherTableBody");
  tbody.innerHTML = "";

  teachers.forEach((t) => {
    const tr = document.createElement("tr");
    tr.innerHTML = `
      <td>${t.matricule}</td>
      <td>${t.name}</td>
      <td>${t.filieres.join(", ")}</td>
      <td>${t.subjects.join(", ")}</td>
      <td>${t.subjects.length}</td>
      <td>${t.hoursPlanned}h</td>
      <td>${t.hoursDone}h</td>
      <td>${t.hoursRemaining}h</td>
    `;
    tbody.appendChild(tr);
  });
}

 // Teacher file import (very minimal CSV support) --------------------------------

 document
   .getElementById("teacherFileInput")
   .addEventListener("change", (event) => {
     const file = event.target.files?.[0];
     if (!file) return;

     if (!file.name.toLowerCase().endsWith(".csv")) {
       alert("Seul le format CSV simple est supporté dans cette démo.");
       return;
     }

     const reader = new FileReader();
     reader.onload = () => {
       const text = reader.result;
       if (typeof text !== "string") return;

       const lines = text.split(/\r?\n/).filter((l) => l.trim());
       if (lines.length < 2) return;

       const header = lines[0].split(";").map((h) => h.trim());
       const idx = {
         matricule: header.indexOf("Matricule"),
         nom: header.indexOf("Nom"),
         filieres: header.indexOf("Filières"),
         matieres: header.indexOf("Matières"),
         heuresPrevues: header.indexOf("Heures totales prévues"),
         heuresFaites: header.indexOf("Heures déjà faites"),
         heuresRestantes: header.indexOf("Heures restantes"),
       };

       lines.slice(1).forEach((line, i) => {
         const cols = line.split(";").map((c) => c.trim());
         if (!cols[idx.matricule] || !cols[idx.nom]) return;

         const existing = teachers.find(
           (t) => t.matricule === cols[idx.matricule]
         );
         const base = existing || {
           id: teachers.length + 1 + i,
           speciality: "N/A",
         };

         const hoursPlanned = parseFloat(cols[idx.heuresPrevues] || "0") || 0;
         const hoursDone = parseFloat(cols[idx.heuresFaites] || "0") || 0;
         const hoursRemaining =
           parseFloat(cols[idx.heuresRestantes] || "0") ||
           Math.max(hoursPlanned - hoursDone, 0);

         const updated = {
           ...base,
           matricule: cols[idx.matricule],
           name: cols[idx.nom],
           filieres: (cols[idx.filieres] || "")
             .split(",")
             .map((s) => s.trim())
             .filter(Boolean),
           subjects: (cols[idx.matieres] || "")
             .split(",")
             .map((s) => s.trim())
             .filter(Boolean),
           hoursPlanned,
           hoursDone,
           hoursRemaining,
         };

         if (existing) {
           Object.assign(existing, updated);
         } else {
           teachers.push(updated);
         }
       });

       refreshTeachersTable();
       alert("Fichier enseignants importé (démo).");
     };
     reader.readAsText(file, "utf-8");
   });

 // Student file import (CSV) -----------------------------------------------------
 document.getElementById("studentFileInput").addEventListener("change", (event) => {
   const file = event.target.files?.[0];
   if (!file) return;
   const reader = new FileReader();
   reader.onload = () => {
     const text = reader.result;
     if (typeof text !== "string") return;
     const lines = text.split(/\r?\n/).filter((l) => l.trim());
     if (lines.length < 2) return;
     // detect separator ; or ,
     const sep = lines[0].includes(";") ? ";" : ",";
     const header = lines[0].split(sep).map(h => h.trim());
     const idx = {
       matricule: header.findIndex(h => /matricule/i.test(h)),
       nom: header.findIndex(h => /nom/i.test(h)),
       filiere: header.findIndex(h => /fili[ií]re|filiere|major/i.test(h)),
       niveau: header.findIndex(h => /niveau|level/i.test(h)),
       moyenne: header.findIndex(h => /moyenne|average/i.test(h)),
       presence: header.findIndex(h => /presence|taux de présence|attendance/i.test(h)),
       projects: header.findIndex(h => /projets|projects|nombre de projets/i.test(h)),
       distance: header.findIndex(h => /distance/i.test(h)),
       travaille: header.findIndex(h => /travaille|job|emploi/i.test(h)),
       statut: header.findIndex(h => /statut|status/i.test(h)),
     };
     const parsed = [];
     lines.slice(1).forEach(line => {
       const cols = line.split(sep).map(c => c.trim());
       if (!cols[idx.matricule]) return;
       const rawAvg = cols[idx.moyenne] || "";
       const avgVal = rawAvg ? parseFloat(rawAvg.replace(",", ".")) : null;
       let statusVal = cols[idx.statut] || "";
       // Enforce rule: if average < 10, cannot be 'Admis'
       if (avgVal !== null && !isNaN(avgVal) && avgVal < 10 && /^admis$/i.test(statusVal)) {
         statusVal = "Ajour.";
       }
       parsed.push({
         id: cols[idx.matricule] || "",
         name: cols[idx.nom] || "",
         filiere: cols[idx.filiere] || "",
         level: cols[idx.niveau] ? parseInt(cols[idx.niveau],10) : null,
         avg: avgVal,
         presence: cols[idx.presence] ? parseInt(cols[idx.presence].replace("%",""),10) : null,
         projects: cols[idx.projects] ? parseInt(cols[idx.projects],10) : 0,
         distance: cols[idx.distance] || "",
         travaille: cols[idx.travaille] || "",
         status: statusVal || "",
       });
     });
     if (parsed.length) {
       studentSample = parsed;
       refreshDashboard();
       alert("Fichier étudiants importé et tableau mis à jour.");
     } else {
       alert("Aucune ligne étudiante valide trouvée dans le fichier.");
     }
   };
   reader.readAsText(file, "utf-8");
 });

 // Simple chart helpers (canvas) ------------------------------------------------
 function drawMajorsPie(counts) {
   const canvas = document.getElementById("chartMajors");
   if (!canvas) return;
   const ctx = canvas.getContext("2d");
   ctx.clearRect(0,0,canvas.width,canvas.height);
   const entries = Object.entries(counts);
   if (entries.length === 0) {
     ctx.fillStyle = "#9ca3af";
     ctx.font = "13px sans-serif";
     ctx.fillText("Aucune donnée", 10, 20);
     return;
   }
   const total = entries.reduce((s,[,v]) => s + v, 0);
   let start = -Math.PI/2;
   entries.forEach(([k,v],i) => {
     const slice = (v/total) * Math.PI * 2;
     ctx.beginPath();
     ctx.moveTo(canvas.width/2, canvas.height/2);
     const hue = (i * 55) % 360;
     ctx.fillStyle = `hsl(${hue} 70% 55%)`;
     ctx.arc(canvas.width/2, canvas.height/2, Math.min(canvas.width, canvas.height)/2 - 10, start, start + slice);
     ctx.closePath();
     ctx.fill();
     start += slice;
   });
   // legend
   ctx.font = "11px sans-serif";
   let y = 12;
   entries.forEach(([k,v],i) => {
     const hue = (i * 55) % 360;
     ctx.fillStyle = `hsl(${hue} 70% 55%)`;
     ctx.fillRect(6, y-10, 10, 8);
     ctx.fillStyle = "#111827";
     ctx.fillText(`${k} (${v})`, 22, y-2);
     y += 14;
   });
 }

 function drawAveragesBars(students) {
   const canvas = document.getElementById("chartAverages");
   if (!canvas) return;
   const ctx = canvas.getContext("2d");
   ctx.clearRect(0,0,canvas.width,canvas.height);
   if (!students.length) {
     ctx.fillStyle = "#9ca3af";
     ctx.font = "13px sans-serif";
     ctx.fillText("Aucune donnée", 10, 20);
     return;
   }
   // bucket averages into ranges
   const buckets = {"0-5":0,"5-10":0,"10-12":0,"12-14":0,"14-16":0,"16-20":0};
   students.forEach(s => {
     const a = parseFloat(s.avg) || 0;
     if (a < 5) buckets["0-5"]++;
     else if (a < 10) buckets["5-10"]++;
     else if (a < 12) buckets["10-12"]++;
     else if (a < 14) buckets["12-14"]++;
     else if (a < 16) buckets["14-16"]++;
     else buckets["16-20"]++;
   });
   const keys = Object.keys(buckets);
   const max = Math.max(...Object.values(buckets),1);
   const pad = 10;
   const w = (canvas.width - pad*2) / keys.length;
   keys.forEach((k,i) => {
     const h = (buckets[k] / max) * (canvas.height - 40);
     ctx.fillStyle = "#0077c2";
     ctx.fillRect(pad + i * w + 6, canvas.height - 20 - h, w - 12, h);
     ctx.fillStyle = "#111827";
     ctx.font = "11px sans-serif";
     ctx.fillText(k, pad + i * w + 8, canvas.height - 4);
   });
 }

// Prediction form (student) ----------------------------------------------------

const predictionForm = document.getElementById("predictionForm");
const predictionBtn = document.getElementById("predictionBtn");
const predictionResults = document.getElementById("predictionResults");
const predictedAverageSpan = document.getElementById("predictedAverage");
const predictedSuccessSpan = document.getElementById("predictedSuccess");
const predictedSuccessBar = document.getElementById("predictedSuccessBar");
const predictionMessage = document.getElementById("predictionMessage");

const requiredPredictionFields = [
  "predMajor",
  "predLevel",
  "predAttendance",
  "predProjects",
  "predDistance"
];

function checkPredictionFormValidity() {
  const valid = requiredPredictionFields.every((id) => {
    const el = document.getElementById(id);
    return el && el.value !== "";
  });
  predictionBtn.disabled = !valid;
}

requiredPredictionFields.forEach((id) => {
  const el = document.getElementById(id);
  if (el) {
    el.addEventListener("input", checkPredictionFormValidity);
    el.addEventListener("change", checkPredictionFormValidity);
  }
});

// Very simple "ML" heuristic for demo
function computePrediction(features) {
  const {
    attendance,
    studyHours,
    participation,
    previousAverage = 12,
  } = features;
  const att = Math.min(Math.max(attendance, 0), 100);
  const study = Math.min(Math.max(studyHours, 0), 80);
  const part = Math.min(Math.max(participation, 0), 10);
  const prev = Math.min(Math.max(previousAverage, 0), 20);

  let avg =
    0.25 * (att / 5) + 0.2 * (study / 4) + 0.2 * (part * 2) + 0.35 * prev;

  avg = Math.max(0, Math.min(avg, 20));

  // success probability: logistic-like transform
  const center = 12;
  const k = 0.6;
  const prob = 1 / (1 + Math.exp(-k * (avg - center)));
  const successPercent = Math.round(prob * 100);

  return { avg, successPercent };
}

predictionForm.addEventListener("submit", (e) => {
  e.preventDefault();
  const attendance = parseFloat(
    document.getElementById("predAttendance").value
  );
  // removed studyHours, participation and previousAverage fields -> use defaults
  const studyHours = undefined;
  const participation = undefined;
  const previousAverage = undefined;

  const { avg, successPercent } = computePrediction({
    attendance,
    studyHours,
    participation,
    previousAverage,
  });

  predictedAverageSpan.textContent = `${avg.toFixed(1)} / 20`;
  predictedSuccessSpan.textContent = `${successPercent} %`;
  predictedSuccessBar.style.width = `${successPercent}%`;

  if (successPercent >= 75) {
    predictionMessage.textContent =
      "Selon les données saisies, cet étudiant présente une probabilité élevée de réussite académique.";
  } else if (successPercent >= 50) {
    predictionMessage.textContent =
      "Selon les données saisies, cet étudiant présente une probabilité modérée de réussite académique. Un accompagnement ciblé peut améliorer ses résultats.";
  } else {
    predictionMessage.textContent =
      "Selon les données saisies, cet étudiant présente une probabilité faible de réussite académique. Un suivi rapproché et un plan de remédiation sont recommandés.";
  }

  predictionResults.hidden = false;
});

// ANALYSE DES PERFORMANCES (JS) -----------------------------------------------

const analysisForm = document.getElementById("analysisForm");
const analyzeBtn = document.getElementById("analyzeBtn");
const analysisResultsCard = document.getElementById("analysisResults");
const radarCanvas = document.getElementById("radarCanvas");
const workText = document.getElementById("workText");
const statusEmoji = document.getElementById("statusEmoji");
const statusText = document.getElementById("statusText");
const analysisText = document.getElementById("analysisText");
const analysisTips = document.getElementById("analysisTips");
const impactChain = document.getElementById("impactChain");

function mapDistanceToScore(dist) {
  // closer -> higher score (for radar: normalized 0-10)
  if (!dist) return 5;
  if (dist === "<5") return 9;
  if (dist === "5-15") return 6;
  return 3; // >15
}

function drawRadar(data) {
  if (!radarCanvas) return;
  const ctx = radarCanvas.getContext("2d");
  ctx.clearRect(0,0,radarCanvas.width,radarCanvas.height);
  const w = radarCanvas.width;
  const h = radarCanvas.height;
  const cx = w/2 - 10;
  const cy = h/2 + 10;
  const radius = Math.min(w,h)/3.2;
  const axes = Object.keys(data);
  const steps = 5;

  // grid
  ctx.strokeStyle = "#e6eef9";
  ctx.lineWidth = 1;
  for (let s=steps; s>=1; s--) {
    ctx.beginPath();
    axes.forEach((a,i) => {
      const angle = (Math.PI * 2 * i / axes.length) - Math.PI/2;
      const r = (radius * s / steps);
      const x = cx + Math.cos(angle)*r;
      const y = cy + Math.sin(angle)*r;
      if (i===0) ctx.moveTo(x,y); else ctx.lineTo(x,y);
    });
    ctx.closePath();
    ctx.stroke();
  }

  // labels
  ctx.fillStyle = "#0b3b66";
  ctx.font = "12px sans-serif";
  axes.forEach((a,i) => {
    const angle = (Math.PI * 2 * i / axes.length) - Math.PI/2;
    const x = cx + Math.cos(angle)*(radius+18);
    const y = cy + Math.sin(angle)*(radius+18);
    ctx.fillText(a, x-10, y+4);
  });

  // polygon (data)
  ctx.beginPath();
  axes.forEach((a,i) => {
    const val = Math.max(0, Math.min(10, data[a]));
    const angle = (Math.PI * 2 * i / axes.length) - Math.PI/2;
    const r = (radius * val / 10);
    const x = cx + Math.cos(angle)*r;
    const y = cy + Math.sin(angle)*r;
    if (i===0) ctx.moveTo(x,y); else ctx.lineTo(x,y);
  });
  ctx.closePath();
  ctx.fillStyle = "rgba(0,119,194,0.18)";
  ctx.fill();
  ctx.strokeStyle = "#0077c2";
  ctx.lineWidth = 2;
  ctx.stroke();
}

// build impact chain icons
function renderImpactChain(items) {
  impactChain.innerHTML = "";
  items.forEach((it, idx) => {
    const el = document.createElement("div");
    el.style.display = "inline-flex";
    el.style.alignItems = "center";
    el.style.gap = "8px";
    el.innerHTML = `<div style="font-size:20px;">${it.icon}</div><div style="font-size:13px;color:var(--text-muted)">${it.label}</div>`;
    impactChain.appendChild(el);
    if (idx < items.length-1) {
      const arrow = document.createElement("div");
      arrow.textContent = "→";
      arrow.style.margin = "0 6px";
      arrow.style.color = "var(--text-muted)";
      impactChain.appendChild(arrow);
    }
  });
}

if (analyzeBtn) {
  // Elements
  const statusSelectEl = document.getElementById("anStatus");
  const anAverageEl = document.getElementById("anAverage");
  const anPresenceEl = document.getElementById("anPresence");
  const anProjectsEl = document.getElementById("anProjects");
  const anDistanceEl = document.getElementById("anDistance");
  const anTravailleEl = document.getElementById("anTravaille");

  // Enforce admissibility of "Admis" when moyenne < 10
  function enforceAdmisRule() {
    const avgVal = parseFloat(anAverageEl.value || "0");
    if (statusSelectEl) {
      const optAd = statusSelectEl.querySelector('option[value="Admis"]');
      // disable 'Admis' option when moyenne < 10 and clear selection if invalid
      if (optAd) {
        if (avgVal < 10) {
          optAd.disabled = true;
          if (statusSelectEl.value === "Admis") {
            statusSelectEl.value = "";
          }
        } else {
          optAd.disabled = false;
        }
      }
    }
  }

  // helper to show inline field error messages beneath inputs
  function setFieldError(el, msg) {
    if (!el) return;
    let container = el.closest(".form-group");
    if (!container) container = el.parentElement;
    if (!container) return;
    let err = container.querySelector(".field-error");
    if (!err) {
      err = document.createElement("div");
      err.className = "field-error";
      err.style.fontSize = "12px";
      err.style.color = "var(--danger)";
      err.style.marginTop = "6px";
      container.appendChild(err);
    }
    err.textContent = msg || "";
    if (!msg) err.style.display = "none";
    else err.style.display = "block";
  }

  // Validate analysis form fields and enable/disable the analyze button,
  // showing helper messages for each invalid field.
  function validateAnalysisForm() {
    let valid = true;

    // clear previous field errors (do not show inline messages for distance, travaille and statut)
    [anAverageEl, anPresenceEl, anProjectsEl].forEach(el => setFieldError(el, ""));

    // moyenne: required, numeric, 0..20 and accepts integer or 1–2 decimals
    const avgRaw = anAverageEl.value;
    const avg = avgRaw === "" ? null : parseFloat(avgRaw);
    const avgNumberRegex = /^\d+(\.\d{1,2})?$/;
    if (avgRaw === "" || !avgNumberRegex.test(avgRaw) || isNaN(avg) || avg < 0 || avg > 20) {
      valid = false;
      setFieldError(anAverageEl, "Entrez une moyenne valide entre 0 et 20 (ex: 12 ou 12.5).");
    }

    // presence: required and must be 0..100
    const presRaw = anPresenceEl.value;
    if (presRaw === "") {
      valid = false;
      setFieldError(anPresenceEl, "Renseignez le taux de présence (0–100).");
    } else {
      const pres = parseInt(presRaw, 10);
      if (isNaN(pres) || pres < 0 || pres > 100) {
        valid = false;
        setFieldError(anPresenceEl, "Le taux de présence doit être un entier entre 0 et 100.");
      }
    }

    // projects: optional but if provided must be integer >=0 and reasonable cap (0..50)
    const projRaw = anProjectsEl.value;
    if (projRaw !== "") {
      const proj = parseInt(projRaw, 10);
      if (isNaN(proj) || proj < 0 || proj > 50) {
        valid = false;
        setFieldError(anProjectsEl, "Nombre de projets invalide (entier entre 0 et 50).");
      }
    }

    // distance: must be one of the allowed options (cannot be the placeholder "")
    const dist = anDistanceEl.value;
    const allowedDists = ["<5", "5-15", ">15"];
    if (!allowedDists.includes(dist)) {
      valid = false;
      // no inline error message shown for distance per UI requirement
    }

    // statut: REQUIRED — ensure a selection is made
    const statusVal = statusSelectEl ? statusSelectEl.value : "";
    if (!statusVal) {
      valid = false;
      // no inline error message shown for statut per UI requirement
    }

    // travaille: NOW REQUIRED — must be either "Oui" or "Non"
    const travailleValRaw = anTravailleEl && anTravailleEl.value ? anTravailleEl.value : "";
    if (travailleValRaw !== "Oui" && travailleValRaw !== "Non") {
      valid = false;
      // no inline error message shown for travaille per UI requirement
    }

    // Additional rule: if moyenne < 10 then 'Admis' must not be selected
    if (avg !== null && !isNaN(avg) && avg < 10) {
      if (statusSelectEl && statusSelectEl.value === "Admis") {
        valid = false;
        setFieldError(statusSelectEl, "Moyenne < 10 : le statut 'Admis' n'est pas autorisé.");
      }
    }

    // Apply disabled state
    analyzeBtn.disabled = !valid;
    if (!valid) {
      analyzeBtn.classList.add("disabled");
    } else {
      analyzeBtn.classList.remove("disabled");
    }

    return valid;
  }

  // Attach listeners for live validation and admiss rule (including status select)
  [anAverageEl, anPresenceEl, anProjectsEl, anDistanceEl, anTravailleEl, statusSelectEl].forEach((el) => {
    if (!el) return;
    el.addEventListener("input", () => {
      enforceAdmisRule();
      validateAnalysisForm();
    });
    el.addEventListener("change", () => {
      enforceAdmisRule();
      validateAnalysisForm();
    });
  });

  // Initial enforcement and validation
  enforceAdmisRule();
  validateAnalysisForm();

  // Click handler observes disabled state and prevents analysis if invalid
  analyzeBtn.addEventListener("click", (e) => {
    e.preventDefault();
    // If button disabled do nothing
    if (analyzeBtn.disabled) {
      alert("Formulaire invalide : corrigez les champs hors plages autorisées avant d'analyser.");
      return;
    }

    // collect inputs
    const name = document.getElementById("anName").value || "—";
    const avg = parseFloat(document.getElementById("anAverage").value || "0");
    const presence = anPresenceEl.value ? parseInt(anPresenceEl.value, 10) : null;
    const dist = document.getElementById("anDistance").value;
    const projects = parseInt(document.getElementById("anProjects").value || "0",10);
    // Treat 'travaille' as provided: if empty but projects>0, we treat it as "Oui"
    let travaille = document.getElementById("anTravaille")?.value || "";
    if (!travaille && projects > 0) travaille = "Oui";
    const status = statusSelectEl?.value || "—";

    // server-side check mirrored on client
    if (avg < 10 && status === "Admis") {
      alert("Moyenne strictement inférieure à 10 — le statut 'Admis' n'est pas disponible.");
      return;
    }

    // Prepare analysis pieces
    let impression = [];
    if (avg >= 14) impression.push("Bonne moyenne générale.");
    else if (avg >= 12) impression.push("Moyenne correcte, marge d'amélioration.");
    else impression.push("Moyenne faible, nécessite intervention.");

    if (dist === ">15") impression.push("Longue distance domicile-école — fatigue/absences possibles.");
    else if (dist === "5-15") impression.push("Distance modérée — prévoir organisation du trajet.");
    else if (dist === "<5") impression.push("Proche — avantage logistique.");

    if (projects >= 2) impression.push("Engagement en projets visible — positif pour apprentissage pratique.");
    else if (projects === 1) impression.push("Participation projet unique — encourager plus d'implication.");
    else impression.push("Peu de projets — stimuler travaux pratiques.");

    if (status === "Echec") impression.push("Statut d'échec confirmé — plan de remédiation requis.");
    if (status === "Admis") impression.push("Statut admis — maintenir efforts.");

    const tips = [];
    if (avg < 12) tips.push("Mettre en place des séances de soutien ciblées (maths, fondements).");
    if (avg < 10) tips.unshift("Moyenne < 10 : priorité à la remédiation individuelle.");
    if ((dist === ">15") || (dist === "5-15")) tips.push("Favoriser des horaires allégés ou cours enregistrés pour les étudiants lointains.");
    if (projects < 2) tips.push("Encourager la participation à des projets pratiques et travaux dirigés.");
    tips.push("Suivi mensuel par tuteur et feedback formalisé.");

    // impact chain: compute influence scores and order by contribution to success or failure
    // normalize scores 0..1: higher => more contribution to success
    const scoreMoyenne = Math.max(0, Math.min(20, avg)) / 20; // 0..1
    const scorePresence = (presence !== null && !isNaN(presence)) ? Math.max(0, Math.min(100, presence)) / 100 : 0.5;
    const scoreProjets = Math.min(10, Math.max(0, projects)) / 10;
    const scoreDistance = (dist === "<5" ? 1 : dist === "5-15" ? 0.6 : 0.25);
    // For 'Travaille' mapping: convert to a normalized score (0..1) consistent with other metrics.
    // - Explicit mapping: "Oui" => 0.0 (reduces success contribution), "Non" => 1.0 (increases success contribution)
    // - If empty, infer a sensible default: treat as 'Oui' if projects == 0 (working likely reduces study time), else 'Non'
    let scoreTravailleSuccess;
    if (travaille === "Oui") {
      scoreTravailleSuccess = 0.0;
    } else if (travaille === "Non") {
      scoreTravailleSuccess = 1.0;
    } else {
      // sensible default when not explicitly provided: if the student does projects, assume not working (better for success)
      scoreTravailleSuccess = projects > 0 ? 1.0 : 0.0;
    }
    const scoreTravailleFailure = 1 - scoreTravailleSuccess;

    // Build array with explicit success and failure contributions
    const rawItems = [
      { key: "Moyenne", icon: "📚", scoreSuccess: scoreMoyenne, scoreFailure: 1 - scoreMoyenne },
      { key: "Présence/Motivation", icon: "👩‍🏫", scoreSuccess: scorePresence, scoreFailure: 1 - scorePresence },
      { key: "Projets", icon: "🕰️", scoreSuccess: scoreProjets, scoreFailure: 1 - scoreProjets },
      { key: "Distance", icon: "📍", scoreSuccess: scoreDistance, scoreFailure: 1 - scoreDistance },
      { key: "Travaille", icon: "💼", scoreSuccess: scoreTravailleSuccess, scoreFailure: scoreTravailleFailure },
    ];

    // decide ordering basis: if Admis -> sort by scoreSuccess desc, if Echec -> scoreFailure desc, else by scoreSuccess desc
    let ordered;
    if (status === "Admis") {
      ordered = rawItems.sort((a,b) => b.scoreSuccess - a.scoreSuccess);
    } else if (status === "Echec") {
      ordered = rawItems.sort((a,b) => b.scoreFailure - a.scoreFailure);
    } else {
      ordered = rawItems.sort((a,b) => b.scoreSuccess - a.scoreSuccess);
    }

    // format chain items with percent indications (rounded)
    const chainItems = ordered.map(it => {
      const pct = Math.round(it.scoreSuccess * 100);
      let tag = "";
      if (status === "Admis" && pct > 50) tag = " · Contribue";
      else if (status === "Echec" && pct < 50) tag = " · Cause";
      return { icon: it.icon, label: `${it.key} (${pct}%)${tag}`, raw: it };
    });

    // radar data
    const predAttEl = document.getElementById("predAttendance");
    let attendanceVal = null;
    if (anPresenceEl && anPresenceEl.value) attendanceVal = parseFloat(anPresenceEl.value);
    else if (predAttEl && predAttEl.value) attendanceVal = parseFloat(predAttEl.value);
    const motivationScore = attendanceVal !== null ? Math.round(Math.min(100, Math.max(0, attendanceVal)) / 10) : 6;
    const radarData = {
      "Moyenne": Math.round(Math.max(0,Math.min(20,avg))/2),
      "Motivation": motivationScore,
      "Projets": Math.min(10, projects),
      "Distance": mapDistanceToScore(dist),
    };

    // Build interpretation + recommendation layout and inject into analysisCards container
    const container = document.getElementById("analysisCards");
    container.innerHTML = ""; // clear previous

    // Interpretation section (separate)
    const interpSection = document.createElement("div");
    interpSection.style.marginBottom = "12px";
    interpSection.innerHTML = `<h2 style="margin:0 0 8px 0;color:var(--blue-main);">Interprétation</h2>`;
    container.appendChild(interpSection);

    // Interpretation: textual summary
    const interpTextCard = document.createElement("div");
    interpTextCard.className = "analysis-card";
    const findings = [];
    findings.push(impression.join(" "));
    const facts = [
      `Moyenne annuelle : ${avg.toFixed(1)} / 20.`,
      `Taux de présence : ${presence !== null ? presence + "%" : "non renseigné"}.`,
      `Projets : ${projects} projet(s).`,
      `Distance domicile–école : ${dist || "non renseignée"}.`,
      `Travaille : ${travaille && travaille !== "" ? travaille : (projects>0 ? "Oui" : "Non")}.`,
      `Statut : ${status}.`,
    ];
    const findingsParagraph = `${findings.join(" ")} ${facts.join(" ")}`;
    interpTextCard.innerHTML = `
      <h3>Résumé</h3>
      <div class="analysis-text">
        <p><strong>${name}</strong> — synthèse basée sur les données fournies.</p>
        <p>${findingsParagraph}</p>
      </div>
    `;
    interpSection.appendChild(interpTextCard);

    // Interpretation: radar chart visualisation + mallet showing 'Travaille' state
    const interpChartCard = document.createElement("div");
    interpChartCard.className = "analysis-card";
    interpChartCard.innerHTML = `
      <h3>Visualisation du profil</h3>
      <div style="display:flex;gap:12px;align-items:flex-start;">
        <div class="analysis-chart-placeholder" style="flex:1;min-width:260px;">
          <canvas width="420" height="260"></canvas>
        </div>
        <div style="width:220px;display:flex;flex-direction:column;align-items:center;gap:8px;">
          <div title="Travaille (job) - indique si l'étudiant travaille en parallèle" style="display:flex;flex-direction:column;align-items:center;gap:6px;padding:8px;border-radius:8px;background:#fffef6;border:1px solid rgba(247,166,0,0.08);width:100%;">
            <div style="font-size:28px;line-height:1;">🔨</div>
            <div style="font-size:13px;color:var(--text-muted);text-align:center;">Travaille</div>
            <div id="travailleValue" style="font-weight:700;color:var(--blue-muted);font-size:14px;">—</div>
          </div>

          <div title="Statut de l'étudiant" style="display:flex;flex-direction:column;align-items:center;gap:6px;padding:8px;border-radius:8px;background:#fff;border:1px solid rgba(148,163,184,0.06);width:100%;">
            <div id="statusSquare" class="status-badge neutral" style="width:48px;height:48px;border-radius:8px;font-size:20px;display:flex;align-items:center;justify-content:center;">—</div>
            <div style="font-size:13px;color:var(--text-muted);text-align:center;">Statut</div>
            <div id="statusValue" style="font-weight:700;color:var(--blue-muted);font-size:14px;">—</div>
          </div>

        </div>
      </div>
    `;
    interpSection.appendChild(interpChartCard);

    // draw radar into interpretation canvas
    (function drawRadarOnCanvas(cnv, data) {
      const ctx = cnv.getContext("2d");
      ctx.clearRect(0,0,cnv.width,cnv.height);
      const w = cnv.width;
      const h = cnv.height;
      const cx = w/2;
      const cy = h/2 + 10;
      const radius = Math.min(w,h)/3.2;
      const axes = Object.keys(data);
      const steps = 5;
      ctx.strokeStyle = "#e6eef9";
      ctx.lineWidth = 1;
      for (let s=steps; s>=1; s--) {
        ctx.beginPath();
        axes.forEach((a,i) => {
          const angle = (Math.PI * 2 * i / axes.length) - Math.PI/2;
          const r = (radius * s / steps);
          const x = cx + Math.cos(angle)*r;
          const y = cy + Math.sin(angle)*r;
          if (i===0) ctx.moveTo(x,y); else ctx.lineTo(x,y);
        });
        ctx.closePath();
        ctx.stroke();
      }
      ctx.fillStyle = "#0b3b66";
      ctx.font = "12px sans-serif";
      axes.forEach((a,i) => {
        const angle = (Math.PI * 2 * i / axes.length) - Math.PI/2;
        const x = cx + Math.cos(angle)*(radius+28);
        const y = cy + Math.sin(angle)*(radius+28);
        ctx.fillText(a, x-12, y+4);
      });
      ctx.beginPath();
      axes.forEach((a,i) => {
        const val = Math.max(0, Math.min(10, data[a]));
        const angle = (Math.PI * 2 * i / axes.length) - Math.PI/2;
        const r = (radius * val / 10);
        const x = cx + Math.cos(angle)*r;
        const y = cy + Math.sin(angle)*r;
        if (i===0) ctx.moveTo(x,y); else ctx.lineTo(x,y);
      });
      ctx.closePath();
      ctx.fillStyle = "rgba(0,119,194,0.18)";
      ctx.fill();
      ctx.strokeStyle = "#0077c2";
      ctx.lineWidth = 2;
      ctx.stroke();
    })(interpChartCard.querySelector("canvas"), radarData);

    // populate the mallet panel with the 'Travaille' value (use same inference as elsewhere)
    const travailleDisplay = interpChartCard.querySelector("#travailleValue");
    const travailleDisplayValue = travaille && travaille !== "" ? travaille : (projects > 0 ? "Oui" : "Non");
    if (travailleDisplay) travailleDisplay.textContent = travailleDisplayValue;

    // populate the status panel: label and choose an image or styling based on status
    const statusDisplay = interpChartCard.querySelector("#statusValue");
    const statusImg = interpChartCard.querySelector("#statusImage");
    const statusLabel = status && status !== "" ? status : "—";
    if (statusDisplay) statusDisplay.textContent = statusLabel;

    // Choose an adequate image for status: use existing /enspd.jpg as fallback and adjust border color
    // update the status square badge instead of the image
    const statusSquareEl = interpChartCard.querySelector("#statusSquare");
    if (statusSquareEl) {
      if (status === "Admis") {
        statusSquareEl.classList.add("admis");
        statusSquareEl.classList.remove("echec", "neutral");
        statusSquareEl.textContent = "✔";
        statusSquareEl.title = "Admis";
      } else if (status === "Echec") {
        statusSquareEl.classList.add("echec");
        statusSquareEl.classList.remove("admis", "neutral");
        statusSquareEl.textContent = "✖";
        statusSquareEl.title = "Échec";
      } else {
        statusSquareEl.classList.remove("admis", "echec");
        statusSquareEl.classList.add("neutral");
        statusSquareEl.textContent = "—";
        statusSquareEl.title = statusLabel;
      }
    }

    // Recommendation section (separate)
    const recSection = document.createElement("div");
    recSection.style.marginTop = "8px";
    recSection.innerHTML = `<h2 style="margin:12px 0 8px 0;color:var(--blue-main);">Recommandations</h2>`;
    container.appendChild(recSection);

    // Recommendation: explanation text
    const recTextCard = document.createElement("div");
    recTextCard.className = "analysis-card";
    const tipsSentences = tips.map(t => (t.trim().endsWith(".") ? t.trim() : t.trim() + ".")).join(" ");
    recTextCard.innerHTML = `
      <h3>Explication des recommandations</h3>
      <p style="color:var(--text-muted);">${tipsSentences}</p>
      <p style="color:var(--text-muted);">La hiérarchie ci‑dessous présente les facteurs qui ont guidé ces recommandations (pourcentage = contribution à la réussite selon le modèle).</p>
    `;
    recSection.appendChild(recTextCard);

    // Recommendation: impact chain visual (ordered factors with tags)
    const recChainCard = document.createElement("div");
    recChainCard.className = "analysis-card";
    recChainCard.innerHTML = `<h3>Facteurs déterminants</h3><div style="margin-top:8px;" id="recImpactLocal"></div>`;
    recSection.appendChild(recChainCard);

    const recImpactLocal = recChainCard.querySelector("#recImpactLocal");
    chainItems.forEach((it, idx) => {
      const el = document.createElement("div");
      el.style.display = "inline-flex";
      el.style.alignItems = "center";
      el.style.gap = "8px";
      el.style.marginRight = "8px";
      el.style.background = "#fff7ed";
      el.style.padding = "8px 10px";
      el.style.borderRadius = "8px";
      el.style.border = "1px solid rgba(247,166,0,0.08)";
      el.innerHTML = `<div style="font-size:18px;">${it.icon}</div><div style="font-size:13px;color:var(--text-muted)">${it.label}</div>`;
      recImpactLocal.appendChild(el);
      if (idx < chainItems.length - 1) {
        const arrow = document.createElement("span");
        arrow.textContent = "→";
        arrow.style.margin = "0 6px";
        arrow.style.color = "var(--text-muted)";
        recImpactLocal.appendChild(arrow);
      }
    });

    // Recommendation: small explanatory bar chart that links metrics to suggested actions
    const recChartCard = document.createElement("div");
    recChartCard.className = "analysis-card";
    recChartCard.innerHTML = `
      <h3>Visuel explicatif des indicateurs</h3>
      <div class="analysis-chart-placeholder">
        <canvas width="420" height="120"></canvas>
      </div>
    `;
    recSection.appendChild(recChartCard);

    const recCanvas = recChartCard.querySelector("canvas");
    if (recCanvas) {
      const ctx = recCanvas.getContext("2d");
      ctx.clearRect(0,0,recCanvas.width,recCanvas.height);
      const keys = ["Moyenne","Présence","Projets","Travaille"];
      const vals = [
        Math.round((avg/20)*100),
        Math.round((presence||0)/100*100),
        Math.round(Math.min(10,projects)/10*100),
        Math.round((scoreTravailleSuccess)*100),
      ];
      const wpad = 20;
      const barW = (recCanvas.width - wpad*2) / keys.length;
      keys.forEach((k,i) => {
        const h = (vals[i]/100) * (recCanvas.height - 30);
        ctx.fillStyle = "#f59e0b";
        ctx.fillRect(wpad + i*barW + 10, recCanvas.height - 20 - h, barW - 20, h);
        ctx.fillStyle = "#111827";
        ctx.font = "12px sans-serif";
        ctx.fillText(k, wpad + i*barW + 8, recCanvas.height - 4);
      });
    }

    // Finally show the analysisResults card and switch to the analysis page
    analysisResultsCard.hidden = false;
    activatePage("analysis");
  });
}

// Initialisation ---------------------------------------------------------------

function init() {
  initNavigation();  // Initialize navigation buttons and sidebar
  initRecommendationForm();  // Initialize recommendation form
  attachRecommendationFormListener();  // Attach form listeners
  populateFiliereSelects();
  // Do not render dashboard data until a student file is imported.
  refreshTimetable();
  refreshTeachersTable();
  activatePage("dashboard");

  // Setup analysis scroll slider if present
  const analysisScrollable = document.getElementById("analysisCards");
  const analysisRange = document.getElementById("analysisScrollRange");
  const sliderContainer = document.querySelector(".vertical-slider");

  if (analysisScrollable && analysisRange && sliderContainer) {
    // Update range position when area scrolls
    function syncRangeToScroll() {
      const maxScroll = Math.max(1, analysisScrollable.scrollHeight - analysisScrollable.clientHeight);
      const pct = Math.round((analysisScrollable.scrollTop / maxScroll) * 100);
      analysisRange.value = isFinite(pct) ? pct : 0;
    }

    // Move scroll position when range changes
    function onRangeInput() {
      const maxScroll = Math.max(1, analysisScrollable.scrollHeight - analysisScrollable.clientHeight);
      const target = (parseInt(analysisRange.value, 10) / 100) * maxScroll;
      analysisScrollable.scrollTop = target;
    }

    // Show or hide the slider depending on whether content overflows
    function updateSliderVisibility() {
      // if the content height is less than or equal to visible height, hide the slider
      if (analysisScrollable.scrollHeight <= analysisScrollable.clientHeight + 2) {
        sliderContainer.style.display = "none";
      } else {
        sliderContainer.style.display = "flex";
      }
    }

    // Attach events
    analysisScrollable.addEventListener("scroll", syncRangeToScroll, { passive: true });
    analysisRange.addEventListener("input", onRangeInput);

    // When content changes size (cards injected), keep range in sync and toggle visibility
    const ro = new ResizeObserver(() => {
      // ensure range value stays correct relative to content height
      syncRangeToScroll();
      updateSliderVisibility();
    });
    ro.observe(analysisScrollable);

    // initial sync and visibility check (delay to allow injected content to render)
    setTimeout(() => {
      syncRangeToScroll();
      updateSliderVisibility();
    }, 200);
  }

  // make sure prediction button state is correct on initial load
  if (typeof checkPredictionFormValidity === "function") {
    checkPredictionFormValidity();
  }
}

document.addEventListener("DOMContentLoaded", init);