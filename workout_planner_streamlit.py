
import streamlit as st
from dataclasses import dataclass
from typing import List, Dict, Tuple
import random
from datetime import datetime, timedelta
from PIL import Image, ImageDraw, ImageFont
import io
import textwrap

# -----------------------
# 🎨 Global Page Settings
# -----------------------
st.set_page_config(
    page_title="ForgeFitness",
    page_icon="💪"
)
# -----------------------
# 🌈 Aesthetic CSS
# -----------------------
CUSTOM_CSS = """
<style>
/* Background gradient */
.stApp {
  background: linear-gradient(135deg, #0f172a 0%, #111827 60%, #1f2937 100%);
  color: #e5e7eb;
  font-family: ui-sans-serif, system-ui, -apple-system, Segoe UI, Roboto, Ubuntu, Cantarell, 'Helvetica Neue', Arial;
}
h1, h2, h3, h4, h5 { color: #f8fafc; }
small, p, li, div { color: #e5e7eb; }

/* Card style */
.card {
  background: rgba(31, 41, 55, 0.75);
  border: 1px solid rgba(148, 163, 184, 0.15);
  border-radius: 16px;
  padding: 18px;
  box-shadow: 0 6px 20px rgba(0,0,0,0.25);
  backdrop-filter: blur(8px);
}

/* Pill buttons */
.pill {
  display: inline-block;
  padding: 6px 12px;
  margin: 4px 6px 0 0;
  border-radius: 999px;
  background: rgba(99, 102, 241, 0.15);
  border: 1px solid rgba(99,102,241,0.35);
  color: #c7d2fe;
  font-size: 12px;
}

/* Subtle separators */
.hr {
  height: 1px;
  background: linear-gradient(90deg, transparent, rgba(148,163,184,0.3), transparent);
  margin: 12px 0 16px 0;
}

/* Day cards */
.day-card {
  border-radius: 18px;
  border: 1px solid rgba(148,163,184,0.15);
  background: rgba(17, 24, 39, 0.65);
  padding: 16px;
}
</style>
"""
st.markdown(CUSTOM_CSS, unsafe_allow_html=True)

# -----------------------
# 🧠 Exercise Library
# -----------------------
@dataclass
class Exercise:
    name: str
    muscle: str
    difficulty: str  # "Beginner" | "Intermediate" | "Advanced"
    tags: List[str]

EXERCISES: List[Exercise] = [
    # Chest
    Exercise("Push-Up", "Chest", "Beginner", ["bodyweight", "shoulder", "wrist"]),
    Exercise("Incline Dumbbell Press", "Chest", "Intermediate", ["shoulder"]),
    Exercise("Barbell Bench Press", "Chest", "Intermediate", ["shoulder", "barbell"]),
    Exercise("Machine Chest Press", "Chest", "Beginner", ["machine", "shoulder"]),
    Exercise("Cable Fly", "Chest", "Intermediate", ["shoulder", "cable"]),

    # Back
    Exercise("Lat Pulldown", "Back", "Beginner", ["shoulder", "machine"]),
    Exercise("Seated Cable Row", "Back", "Beginner", ["lower-back", "cable"]),
    Exercise("Pull-Up", "Back", "Advanced", ["shoulder", "grip"]),
    Exercise("Barbell Bent-Over Row", "Back", "Intermediate", ["lower-back", "barbell"]),
    Exercise("Single-Arm Dumbbell Row", "Back", "Beginner", ["lower-back", "dumbbell"]),

    # Shoulders
    Exercise("Dumbbell Shoulder Press", "Shoulders", "Intermediate", ["shoulder", "spine"]),
    Exercise("Lateral Raise", "Shoulders", "Beginner", ["shoulder"]),
    Exercise("Face Pull", "Shoulders", "Beginner", ["shoulder", "cable"]),
    Exercise("Arnold Press", "Shoulders", "Advanced", ["shoulder"]),

    # Biceps
    Exercise("EZ-Bar Curl", "Biceps", "Beginner", ["elbow", "barbell"]),
    Exercise("Dumbbell Curl", "Biceps", "Beginner", ["elbow", "dumbbell"]),
    Exercise("Incline Dumbbell Curl", "Biceps", "Intermediate", ["elbow"]),
    Exercise("Cable Curl", "Biceps", "Intermediate", ["elbow", "cable"]),

    # Triceps
    Exercise("Cable Triceps Pushdown", "Triceps", "Beginner", ["elbow", "cable"]),
    Exercise("Overhead Triceps Extension", "Triceps", "Intermediate", ["shoulder", "elbow"]),
    Exercise("Close-Grip Bench Press", "Triceps", "Advanced", ["shoulder", "elbow", "barbell"]),

    # Legs: Quads, Hamstrings, Calves, Glutes
    Exercise("Back Squat", "Quads", "Advanced", ["knee", "spine", "barbell"]),
    Exercise("Front Squat", "Quads", "Advanced", ["knee", "spine", "barbell"]),
    Exercise("Leg Press", "Quads", "Beginner", ["knee", "machine"]),
    Exercise("Walking Lunges", "Quads", "Intermediate", ["knee", "balance"]),
    Exercise("Romanian Deadlift", "Hamstrings", "Intermediate", ["hamstrings", "hip-hinge", "spine", "barbell"]),
    Exercise("Hamstring Curl (Machine)", "Hamstrings", "Beginner", ["machine", "knee"]),
    Exercise("Hip Thrust", "Glutes", "Beginner", ["hip"]),
    Exercise("Calf Raise (Standing)", "Calves", "Beginner", ["ankle"]),
    Exercise("Seated Calf Raise", "Calves", "Beginner", ["ankle", "machine"]),

    # Core
    Exercise("Plank", "Abs", "Beginner", ["wrist", "shoulder"]),
    Exercise("Hanging Knee Raise", "Abs", "Intermediate", ["shoulder", "grip"]),
    Exercise("Cable Woodchop", "Abs", "Intermediate", ["spine", "cable"]),
    Exercise("Bicycle Crunch", "Abs", "Beginner", []),

    # Forearms
    Exercise("Reverse Curl", "Forearms", "Beginner", ["wrist", "elbow"]),
    Exercise("Farmer's Carry", "Forearms", "Intermediate", ["grip"]),

    # Cardio / Weight loss helpers
    Exercise("Treadmill Intervals", "Cardio", "Beginner", ["cardio", "knee"]),
    Exercise("Stationary Bike", "Cardio", "Beginner", ["cardio", "knee-friendly"]),
    Exercise("Rowing Machine", "Cardio", "Intermediate", ["cardio", "back", "shoulder"]),
    Exercise("Jump Rope", "Cardio", "Intermediate", ["cardio", "ankle"]),
]

MUSCLE_GROUPS = ["Chest","Back","Shoulders","Biceps","Triceps","Abs","Calves","Quads","Hamstrings","Glutes","Forearms","Cardio"]
DIFFICULTIES = ["Beginner","Intermediate","Advanced"]

# Injury keyword map -> tags to avoid
INJURY_TAGS = {
    "shoulder": ["shoulder","overhead"],
    "elbow": ["elbow"],
    "wrist": ["wrist"],
    "knee": ["knee"],
    "ankle": ["ankle"],
    "lower back": ["lower-back","spine","deadlift","hip-hinge"],
    "back": ["lower-back","spine","back"],
    "neck": ["neck","overhead"],
    "hip": ["hip","hip-hinge"],
    "hamstring": ["hamstrings"],
    "achilles": ["ankle"],
}

# -----------------------
# 🧮 Helper Functions
# -----------------------
def estimate_set_minutes(difficulty: str) -> float:
    # Harder = slightly longer sets & rests
    if difficulty == "Beginner":
        return 0.5 + 1.0  # 0.5 set + 1.0 rest = 1.5
    if difficulty == "Intermediate":
        return 0.6 + 1.2  # 1.8
    return 0.7 + 1.5      # 2.2

def warmup_cooldown_minutes(difficulty: str) -> Tuple[int, int]:
    if difficulty == "Beginner":
        return (8, 8)
    if difficulty == "Intermediate":
        return (10, 10)
    return (12, 12)

def choose_exercises(targets: List[str], difficulty: str, avoid_tags: List[str], n: int) -> List[Exercise]:
    pool = [ex for ex in EXERCISES if (ex.muscle in targets or ("Cardio" in targets and ex.muscle=="Cardio"))]
    # Filter difficulty upwards (beginner can use beginner+intermediate, advanced can use all)
    if difficulty == "Beginner":
        pool = [ex for ex in pool if ex.difficulty in ["Beginner","Intermediate"]]
    elif difficulty == "Intermediate":
        pool = [ex for ex in pool if ex.difficulty in ["Beginner","Intermediate","Advanced"]]
    else:
        pool = pool  # all

    # Avoid exercises with risky tags
    if avoid_tags:
        pool = [ex for ex in pool if not any(tag in avoid_tags for tag in ex.tags)]

    # Ensure diversity by muscle
    by_muscle: Dict[str, List[Exercise]] = {}
    for ex in pool:
        by_muscle.setdefault(ex.muscle, []).append(ex)

    # Round-robin pick across muscles
    selected = []
    muscles = [m for m in targets if m in by_muscle]
    if not muscles and pool:
        muscles = [pool[0].muscle]
    idx = 0
    while len(selected) < n and muscles:
        m = muscles[idx % len(muscles)]
        if by_muscle.get(m):
            choice = random.choice(by_muscle[m])
            # prevent duplicates by name
            if choice.name not in [s.name for s in selected]:
                selected.append(choice)
        idx += 1
        if idx > 100:  # safety
            break
    # If still short, fill randomly
    if len(selected) < n:
        remainder = [ex for ex in pool if ex.name not in [s.name for s in selected]]
        random.shuffle(remainder)
        selected += remainder[: (n - len(selected))]
    return selected[:n]

def build_day_plan(targets: List[str], difficulty: str, duration_min: int, avoid_tags: List[str]):
    # Choose 3-5 exercises; 2-3 sets of 8-12 reps
    warm, cool = warmup_cooldown_minutes(difficulty)
    remaining = max(duration_min - (warm + cool), 30)
    per_set = estimate_set_minutes(difficulty)  # minutes per set incl. rest

    # Decide number of exercises initially
    n_ex = 4
    if remaining < 60: n_ex = 3
    if remaining > 80: n_ex = 5
    exercises = choose_exercises(targets, difficulty, avoid_tags, n_ex)

    # Start with baseline sets/reps
    plan = []
    total_minutes = warm + cool
    for ex in exercises:
        sets = 2 if difficulty == "Beginner" else 3
        reps = 10
        # Slight variation by difficulty
        if difficulty == "Beginner":
            reps = random.choice([8,10,12])
        elif difficulty == "Intermediate":
            reps = random.choice([8,10,12])
        else:
            reps = random.choice([8,10,12])
        est = sets * per_set
        total_minutes += est
        plan.append({"exercise": ex, "sets": sets, "reps": reps, "est_min": est})

    # Adjust sets to better match target duration
    # If under target by >10 min, try to add one set to some exercises (up to 3)
    def current_total():
        return warm + cool + sum(item["est_min"] for item in plan)
    tries = 0
    while current_total() < duration_min - 8 and tries < 20:
        for item in plan:
            if item["sets"] < 3:
                item["sets"] += 1
                item["est_min"] += per_set
                if current_total() >= duration_min - 4:
                    break
        tries += 1

    # If over target by >10 min, remove some sets (down to 2)
    tries = 0
    while current_total() > duration_min + 8 and tries < 20:
        for item in plan:
            if item["sets"] > 2:
                item["sets"] -= 1
                item["est_min"] -= per_set
                if current_total() <= duration_min + 4:
                    break
        tries += 1

    # Build textual steps
    steps = []
    steps.append(f"Stretch & Warm-up • {warm} min (dynamic warm-up for: {', '.join(targets)})")
    for item in plan:
        name = item["exercise"].name
        m = item["exercise"].muscle
        sets = item["sets"]
        reps = item["reps"]
        steps.append(f"{sets} sets × {reps} reps • {name} ({m})")
        # Rest guidance by difficulty
        if difficulty == "Beginner":
            rest = 60
        elif difficulty == "Intermediate":
            rest = 75
        else:
            rest = 90
        steps.append(f"Rest • {int(rest/60)}–{int((rest+30)/60)} min")
    steps.append(f"Cool-down & Stretch • {cool} min (static stretching for: {', '.join(targets)})")

    return {
        "targets": targets,
        "difficulty": difficulty,
        "duration": duration_min,
        "warm": warm,
        "cool": cool,
        "items": plan,
        "steps": steps,
        "estimated_total": round(current_total())
    }

def plan_week(start_date: datetime, selected_days: List[str], targets_by_day: Dict[str, List[str]], difficulty: str, daily_duration: int, avoid_tags: List[str]):
    day_names = ["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday"]
    week = {}
    for i, day in enumerate(day_names):
        if day in selected_days:
            targets = targets_by_day.get(day, [])
            if not targets:
                targets = ["Cardio"]  # default if none chosen
            week[day] = build_day_plan(targets, difficulty, daily_duration, avoid_tags)
        else:
            week[day] = None
    return week

def tags_from_injury_text(txt: str) -> List[str]:
    txt = (txt or "").lower()
    avoid = set()
    for key, vals in INJURY_TAGS.items():
        if key in txt:
            avoid.update(vals)
    # also collect raw words like 'shoulder', 'knee'
    for word in ["shoulder","elbow","wrist","knee","ankle","back","lower back","neck","hip","hamstring","achilles"]:
        if word in txt:
            avoid.add(word if word!="lower back" else "lower-back")
    return list(avoid)

def render_plan_text(week, show_details: bool = False) -> str:
    out = []
    for day, plan in week.items():
        out.append(f"=== {day} ===")
        if plan is None:
            out.append("Rest Day")
        else:
            out.append(f"Difficulty: {plan['difficulty']} • Target Duration: {plan['duration']} min • Estimated: {plan['estimated_total']} min")
            out.append(f"Targets: {', '.join(plan['targets'])}")
            if show_details:
                for step in plan["steps"]:
                    out.append(f"- {step}")
            else:
                # summary
                for item in plan["items"]:
                    ex = item["exercise"]
                    out.append(f"- {ex.name} ({ex.muscle}): {item['sets']} × {item['reps']}")
        out.append("")
    return "\n".join(out).strip()

def plan_to_png(text: str, title: str = "Workout Plan") -> bytes:
    # Render a simple image from text for easy saving/sharing
    padding = 40
    line_width = 70
    wrapped = []
    for line in text.split("\n"):
        if len(line) > line_width:
            wrapped.extend(textwrap.wrap(line, width=line_width))
        else:
            wrapped.append(line)

    # Basic font
    try:
        font = ImageFont.truetype("DejaVuSans.ttf", 20)
        title_font = ImageFont.truetype("DejaVuSans-Bold.ttf", 26)
    except:
        font = ImageFont.load_default()
        title_font = ImageFont.load_default()

    line_height = 28
    height = padding*2 + line_height*(len(wrapped)+2)
    width = 1100
    img = Image.new("RGB", (width, height), color=(18, 24, 38))
    draw = ImageDraw.Draw(img)

    # Title
    draw.text((padding, padding-10), f"💪 {title}", font=title_font, fill=(240, 240, 255))

    # Body
    y = padding + 28
    for line in wrapped:
        draw.text((padding, y), line, font=font, fill=(220, 225, 235))
        y += line_height

    buf = io.BytesIO()
    img.save(buf, format="PNG")
    return buf.getvalue()

# -----------------------
# 🧭 Sidebar Controls
# -----------------------
with st.sidebar:
    st.markdown("## 💪 Smart Workout Planner")
    st.caption("Plan your week with difficulty, duration, target muscles & safety filters.")
    st.markdown("<div class='hr'></div>", unsafe_allow_html=True)
    week_start = st.date_input("Week starting", value=datetime.today())
    difficulty = st.select_slider("Difficulty", DIFFICULTIES, value="Intermediate")
    duration = st.slider("Daily target duration (minutes)", min_value=60, max_value=120, value=75, step=5)
    st.markdown("<div class='hr'></div>", unsafe_allow_html=True)

    st.markdown("### Targeted muscle groups")
    targets_global = st.multiselect(
        "Pick overall targets (you can refine by day below)",
        MUSCLE_GROUPS, default=["Chest","Back","Quads","Hamstrings","Abs"]
    )

    st.markdown("<div class='hr'></div>", unsafe_allow_html=True)
    st.markdown("### Safety: injuries or fatigue")
    injuries_text = st.text_area("List injuries/fatigue (e.g., 'knee pain, shoulder')", height=80, placeholder="knee pain, lower back, wrist...")
    avoid_tags = tags_from_injury_text(injuries_text)
    if avoid_tags:
        st.markdown("**Exercises will avoid tags:** " + ", ".join([f"<span class='pill'>{t}</span>" for t in avoid_tags]), unsafe_allow_html=True)
    else:
        st.caption("No restrictions detected.")

    st.markdown("<div class='hr'></div>", unsafe_allow_html=True)
    st.markdown("### Days you plan to train")
    planned_days = st.multiselect("Choose training days", ["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday"],
                                  default=["Monday","Wednesday","Friday"])

# -----------------------
# 📅 Per-day target selection
# -----------------------
st.title("🏋️‍♀️ Smart Workout Planner")
st.caption("Plan a balanced week. Click a day to view full session details, export as image, or copy text.")

with st.expander("Optional: customize targets per day"):
    cols = st.columns(4)
    targets_by_day = {}
    all_days = ["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday"]
    for idx, day in enumerate(all_days):
        with cols[idx % 4]:
            targets_by_day[day] = st.multiselect(f"{day} targets", MUSCLE_GROUPS, default=targets_global, key=f"tg_{day}")

# -----------------------
# 🧩 Generate Plan
# -----------------------
if "week_plan" not in st.session_state:
    st.session_state.week_plan = {}

if st.button("✨ Generate Weekly Plan", type="primary", use_container_width=True):
    week_dt = datetime.combine(week_start, datetime.min.time())
    st.session_state.week_plan = plan_week(week_dt, planned_days, targets_by_day, difficulty, duration, avoid_tags)
    st.session_state.selected_day = None

week_plan = st.session_state.get("week_plan", {})

# -----------------------
# 🗓️ Weekly Overview Grid
# -----------------------
if week_plan:
    st.subheader("Your Week at a Glance")
    grid_cols = st.columns(7)
    days = ["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday"]
    for i, day in enumerate(days):
        with grid_cols[i]:
            st.markdown(f"#### {day}")
            card = st.container()
            with card:
                st.markdown("<div class='day-card'>", unsafe_allow_html=True)
                if week_plan.get(day) is None:
                    st.markdown("**Rest Day**")
                else:
                    p = week_plan[day]
                    st.markdown(f"**{', '.join(p['targets'])}**")
                    st.caption(f"~{p['estimated_total']} min • {p['difficulty']}")
                    for item in p["items"]:
                        ex = item["exercise"]
                        st.markdown(f"- {ex.name}: {item['sets']}×{item['reps']}")
                view = st.button(f"View {day}", key=f"view_{day}", use_container_width=True)
                st.markdown("</div>", unsafe_allow_html=True)
                if view:
                    st.session_state.selected_day = day

    # Weekly export options
    st.markdown("<div class='hr'></div>", unsafe_allow_html=True)
    st.subheader("Export Weekly Plan")
    weekly_text = render_plan_text(week_plan, show_details=False)
    colW1, colW2 = st.columns([1,1])
    with colW1:
        st.text_area("Copy weekly summary", weekly_text, height=240)
    with colW2:
        png_bytes = plan_to_png(weekly_text, title="Weekly Workout Plan")
        st.download_button("📥 Download Weekly Plan (PNG)", data=png_bytes, file_name="weekly_workout_plan.png", mime="image/png", use_container_width=True)

# -----------------------
# 🔎 Day Detail View
# -----------------------
selected_day = st.session_state.get("selected_day")
if selected_day:
    st.markdown("<div class='hr'></div>", unsafe_allow_html=True)
    st.header(f"📘 {selected_day} — Full Session")
    plan = week_plan.get(selected_day)
    if plan is None:
        st.info("This is a Rest Day. Consider light mobility, walking, or yoga.")
    else:
        # Steps
        st.markdown("**Session Steps**")
        for step in plan["steps"]:
            st.markdown(f"- {step}")

        # Copyable text + PNG export
        st.markdown("<div class='hr'></div>", unsafe_allow_html=True)
        st.subheader("Export This Session")
        day_text = "\n".join([f"{selected_day} Session ({plan['difficulty']} • {plan['estimated_total']} min)",
                              f"Targets: {', '.join(plan['targets'])}",
                              ""] + [f"- {s}" for s in plan["steps"]])
        c1, c2 = st.columns([1,1])
        with c1:
            st.text_area("Copy text plan", day_text, height=280)
        with c2:
            img_bytes = plan_to_png(day_text, title=f"{selected_day} Workout")
            st.download_button("📥 Download Session (PNG)", data=img_bytes, file_name=f"{selected_day.lower()}_session.png", mime="image/png", use_container_width=True)

        st.caption("Tip: Save images to share with friends or keep them in your photo gallery.")

# -----------------------
# ℹ️ Footer
# -----------------------
st.markdown("<div class='hr'></div>", unsafe_allow_html=True)
with st.expander("ℹ️ How the planner is built"):
    st.write(
        """
        - Exercises are filtered by your selected **targets**, **difficulty**, and inferred **injury/fatigue** tags.
        - Each day includes a **warm-up**, **3–5 exercises** (each **2–3 sets** of **8–12 reps**), appropriate **rests**, and a **cool-down**.
        - The planner adjusts sets to fit your chosen **duration** (1–2 hours).
        - Export options let you **copy** the plan or **download** a tidy **PNG** image.
        """
    )
