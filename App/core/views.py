from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
from .models import TimetableEntry, Teacher, Room
import json
from datetime import date
import csv
from io import TextIOWrapper
from ml_utils.data_prep import parse_planning_file


def index(request):
  # The SPA lives in index.html at project root
  # provide filieres/matieres context so the template JS can populate dropdowns
  try:
    matieres_by_filiere_level, matieres_map = parse_planning_file()
  except Exception:
    matieres_by_filiere_level, matieres_map = {}, {}

  context = {
    "filieres": sorted(matieres_map.keys()),
    "matieres_json": json.dumps(matieres_map, ensure_ascii=False),
    "matieres_by_level_json": json.dumps(matieres_by_filiere_level, ensure_ascii=False),
  }
  return render(request, "index.html", context)


@csrf_exempt
@require_POST
def api_recommend(request):
  """
  Example endpoint if you want to call a Django backend from JS.
  Currently only echoes back simple fake recommendations.
  """
  try:
    data = json.loads(request.body.decode("utf-8"))
  except Exception:
    return JsonResponse({"error": "Invalid JSON"}, status=400)

  effectif = int(data.get("effectif", 40))
  rooms_qs = Room.objects.order_by("capacity")
  rooms_ok = [r for r in rooms_qs if r.capacity >= effectif][:3]
  if not rooms_ok:
    rooms_ok = list(rooms_qs[:3])

  teachers_qs = Teacher.objects.all()[:3]

  return JsonResponse(
      {
          "rooms": [
              {"id": r.id, "name": r.name, "capacity": r.capacity}
              for r in rooms_ok
          ],
          "teachers": [
              {
                  "id": t.id,
                  "name": t.name,
                  "speciality": t.speciality,
                  "hours_planned": t.hours_planned,
                  "hours_done": t.hours_done,
                  "hours_remaining": t.hours_remaining,
              }
              for t in teachers_qs
          ],
      }
  )


@csrf_exempt
@require_POST
def api_program(request):
  """
  Simple endpoint to program a course into the timetable.
  Frontend logic already does similar checks;
  this is an example of the same on the backend.
  """
  try:
    data = json.loads(request.body.decode("utf-8"))
  except Exception:
    return JsonResponse({"error": "Invalid JSON"}, status=400)

  day = data.get("day")
  slot = data.get("slot")
  teacher_id = data.get("teacher_id")
  room_id = data.get("room_id")
  filiere = data.get("filiere")
  level = data.get("niveau")
  subject = data.get("matiere")
  session_type = data.get("type")
  effectif = int(data.get("effectif", 0))
  date_str = data.get("date")

  if not all([day, slot, teacher_id, room_id, filiere, level, subject, session_type]):
    return JsonResponse({"error": "Missing fields"}, status=400)

  teacher = Teacher.objects.get(id=teacher_id)
  room = Room.objects.get(id=room_id)

  # basic rules
  if room.capacity < effectif:
    return JsonResponse({"error": "Room capacity too small"}, status=400)

  duration_hours = 4.0
  if teacher.hours_remaining < duration_hours:
    return JsonResponse(
        {"error": "Teacher has not enough remaining hours"}, status=400
    )

  # schedule conflicts
  if TimetableEntry.objects.filter(day=day, slot=slot, room=room).exists():
    return JsonResponse({"error": "Room already booked"}, status=400)
  if TimetableEntry.objects.filter(day=day, slot=slot, teacher=teacher).exists():
    return JsonResponse({"error": "Teacher already booked"}, status=400)

  d = date.fromisoformat(date_str) if date_str else date.today()

  entry = TimetableEntry.objects.create(
      day=day,
      slot=slot,
      filiere=filiere,
      level=level,
      subject=subject,
      session_type=session_type,
      room=room,
      teacher=teacher,
      date=d,
      capacity=effectif,
  )

  teacher.hours_done += duration_hours
  teacher.save(update_fields=["hours_done"])

  return JsonResponse({"ok": True, "id": entry.id})


@csrf_exempt
@require_POST
def api_upload_students(request):
  """
  Accepts a multipart/form-data POST with a file field named 'file'.
  Parses the CSV and returns a filtered dataset containing only:
    Matricule, Annee_academique, Niveau, Cursus, Filiere, Age, Genre,
    Nb_matieres_validees, Nb_credits_obtenus, Nb_projets, Moyenne_annuelle

  Also computes aggregates:
    - counts by cursus
    - counts by filiere
    - counts by genre
    - success rate following rule:
        * if Niveau >= 3 -> success if Nb_credits_obtenus >= 60
        * if Niveau in [1,2] -> success if Nb_credits_obtenus >= 45
  """
  uploaded = request.FILES.get("file")
  if not uploaded:
    return JsonResponse({"error": "No file provided"}, status=400)

  try:
    # support files with utf-8 or latin-1 encoding by attempting utf-8 first
    text_wrapper = TextIOWrapper(uploaded.file, encoding="utf-8", errors="replace")
    reader = csv.DictReader(text_wrapper)
  except Exception:
    return JsonResponse({"error": "Failed to read uploaded file"}, status=400)

  filtered = []
  counts_cursus = {}
  counts_filiere = {}
  counts_genre = {}
  total = 0
  success_count = 0

  # expected CSV header columns (user-provided)
  # Matricule,Annee_academique,Niveau,Cursus,Filiere,Age,Annee_naissance,Genre,Distance_domicile_ecole,Travaille,Note_moy_CC_S1,Note_moy_SN_S1,Note_moy_CC_S2,Note_moy_SN_S2,Moyenne_S1,Moyenne_S2,Moyenne_annuelle,Nb_matieres_validees,Nb_credits_obtenus,Nb_matieres_non_validees,Nb_heures_cours_total,Nb_heures_presence,Nb_projets,Reussite

  for row in reader:
    if not row:
      continue
    total += 1
    # safe extraction with fallback keys (strip keys)
    def g(k):
      return row.get(k) if k in row else row.get(k.lower()) if k.lower() in row else row.get(k.upper()) if k.upper() in row else ""

    try:
      matricule = (g("Matricule") or "").strip()
      annee = (g("Annee_academique") or "").strip()
      niveau_raw = (g("Niveau") or "").strip()
      niveau = int(niveau_raw) if niveau_raw.isdigit() else None
      cursus = (g("Cursus") or "").strip()
      filiere = (g("Filiere") or "").strip()
      age_raw = (g("Age") or "").strip()
      age = int(age_raw) if age_raw.isdigit() else None
      genre = (g("Genre") or "").strip()
      nb_matieres_validees_raw = (g("Nb_matieres_validees") or "").strip()
      nb_matieres_validees = int(nb_matieres_validees_raw) if nb_matieres_validees_raw.isdigit() else 0
      nb_credits_raw = (g("Nb_credits_obtenus") or "").strip()
      nb_credits = int(nb_credits_raw) if nb_credits_raw.isdigit() else 0
      nb_projets_raw = (g("Nb_projets") or "").strip()
      nb_projets = int(nb_projets_raw) if nb_projets_raw.isdigit() else 0
      moyenne_raw = (g("Moyenne_annuelle") or "").strip().replace(",", ".")
      moyenne = float(moyenne_raw) if moyenne_raw.replace(".", "").isdigit() else None
    except Exception:
      # skip malformed row
      continue

    # determine success per rule
    is_success = False
    if niveau is not None:
      if niveau >= 3:
        is_success = nb_credits >= 60
      elif niveau in (1, 2):
        is_success = nb_credits >= 45

    if is_success:
      success_count += 1

    # accumulate counts
    counts_cursus[cursus] = counts_cursus.get(cursus, 0) + 1
    counts_filiere[filiere] = counts_filiere.get(filiere, 0) + 1
    counts_genre[genre] = counts_genre.get(genre, 0) + 1

    filtered.append(
      {
        "Matricule": matricule,
        "Annee_academique": annee,
        "Niveau": niveau,
        "Cursus": cursus,
        "Filiere": filiere,
        "Age": age,
        "Genre": genre,
        "Nb_matieres_validees": nb_matieres_validees,
        "Nb_credits_obtenus": nb_credits,
        "Nb_projets": nb_projets,
        "Moyenne_annuelle": moyenne,
      }
    )

  # compute success rate (percentage). protect divide by zero.
  success_rate = round((success_count / total) * 100, 1) if total > 0 else 0.0

  return JsonResponse(
    {
      "meta": {
        "total_rows": total,
        "success_count": success_count,
        "success_rate_percent": success_rate,
      },
      "counts": {
        "by_cursus": counts_cursus,
        "by_filiere": counts_filiere,
        "by_genre": counts_genre,
      },
      "students": filtered,
    }
  )