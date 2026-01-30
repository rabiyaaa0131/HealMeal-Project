import streamlit as st
import io
import time
import matplotlib.pyplot as plt
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors

# -------------------------------------------------
# PAGE CONFIG
# -------------------------------------------------
st.set_page_config(
    page_title="HealMeal – Data Driven Meal Recommendation System",
    page_icon="🥗",
    layout="centered"
)

# -------------------------------------------------
# BACKGROUND + HERO
# -------------------------------------------------
st.markdown("""
<style>
.stApp {
    background-image:
        linear-gradient(rgba(255,255,255,0.95), rgba(255,255,255,0.95)),
        url("https://images.unsplash.com/photo-1498837167922-ddd27525d352");
    background-size: cover;
}
.hero { text-align:center; padding:25px; }
.hero h1 { font-size:42px; font-weight:800; }
</style>

<div class="hero">
<h1>🥗 HealMeal</h1>
<h3>Data Driven Meal Recommendation System</h3>
<p>Personalized • Condition-Aware • Dataset-Based</p>
</div>
<hr>
""", unsafe_allow_html=True)

# -------------------------------------------------
# USER INPUT
# -------------------------------------------------
with st.form("user_form"):
    name = st.text_input("Name")
    age = st.number_input("Age", 1, 100, 30)

    food_pref = st.selectbox("Food Preference", ["Veg", "Non-Veg"])

    conditions = st.multiselect(
        "Select Health Conditions (optional)",
        [
            # Metabolic & Lifestyle
            "Diabetes", "Pre-diabetes", "Cholesterol", "Obesity", "Underweight",
            "Weight Maintenance", "Sedentary Lifestyle",

            # Deficiency related
            "Anemia", "Iron Deficiency", "Vitamin D Deficiency",
            "Vitamin B12 Deficiency", "Calcium Deficiency",

            # Digestive
            "Acidity", "Constipation", "Indigestion", "Gastritis",
            "Acid Reflux (GERD)", "IBS", "Bloating",

            # Cardiovascular
            "Hypertension (High BP)", "Low Blood Pressure",
            "Heart Health Concern",

            # Hormonal
            "Thyroid Disorder", "PCOS / PCOD",

            # Immunity & Infection
            "Weak Immunity", "Cold", "Cough", "Fever",
            "Post-Illness Recovery", "Post-COVID Recovery",

            # Neurological & Mental
            "Stress / Anxiety", "Poor Sleep (Insomnia)",
            "Migraine", "Headache", "Mental Fatigue",

            # Musculoskeletal
            "Joint Pain / Arthritis", "Muscle Weakness",

            # Food tolerance
            "Lactose Intolerance", "Gluten Sensitivity",

            # General
            "Poor Appetite", "Dehydration", "General Wellness",
            "Elderly Nutrition"
        ],
        max_selections=5
    )

    bp_level = st.selectbox("BP Level", ["Normal", "High", "Low"])
    sugar_level = st.selectbox("Sugar Level", ["Normal", "High", "Low"])

    submit = st.form_submit_button("Generate Meal Plan")

# -------------------------------------------------
# AI DECISION LOGIC
# -------------------------------------------------
def decide_plan(bp, sugar, conditions):
    reasons = []
    if bp != "Normal":
        reasons.append(f"Blood Pressure is {bp}")
    if sugar != "Normal":
        reasons.append(f"Sugar level is {sugar}")
    if {"Diabetes", "Heart Health Concern"} & set(conditions):
        reasons.append("Presence of health-related risk conditions")

    if reasons:
        return "Modified Meal Plan", reasons
    return "Suggested Meal Plan", []

# -------------------------------------------------
# DATASET (FULL VEG + NON-VEG)
# -------------------------------------------------
def get_meals(food_type):
    if food_type == "Veg":
        return {
            "Breakfast (7:00–8:00 AM)": [
                ("1 cup milk", 120, 12, 8, 5),
                ("Vegetable omelette", 180, 6, 10, 12),
                ("2 brown bread slices", 140, 24, 6, 2),
                ("3 dates", 70, 18, 1, 0)
            ],
            "Lunch (1:00–2:00 PM)": [
                ("1 cup rice", 200, 45, 4, 1),
                ("Dal", 220, 30, 12, 4),
                ("Mixed vegetable curry", 150, 18, 5, 6),
                ("Salad", 50, 10, 2, 0)
            ],
            "Dinner (7:30–8:30 PM)": [
                ("2 chapati", 180, 30, 6, 4),
                ("Vegetable curry", 200, 18, 6, 8),
                ("Curd", 90, 5, 5, 3)
            ]
        }

    else:
        return {
            "Breakfast (7:00–8:00 AM)": [
                ("1 cup milk", 120, 12, 8, 5),
                ("Bread omelette", 220, 24, 12, 10),
                ("2 brown bread slices", 140, 24, 6, 2),
                ("3 dates", 70, 18, 1, 0)
            ],
            "Lunch (1:00–2:00 PM)": [
                ("1 cup rice", 200, 45, 4, 1),
                ("Chicken curry", 300, 8, 25, 18),
                ("Dal", 180, 28, 10, 3),
                ("Salad", 50, 10, 2, 0)
            ],
            "Dinner (7:30–8:30 PM)": [
                ("2 chapati", 180, 30, 6, 4),
                ("Grilled fish / chicken", 250, 0, 28, 12),
                ("Vegetable curry", 150, 18, 5, 6)
            ]
        }

# -------------------------------------------------
# MAIN OUTPUT
# -------------------------------------------------
if submit:
    with st.spinner("🍽️ Generating your diet plan..."):
        time.sleep(1.5)

    plan_type, reasons = decide_plan(bp_level, sugar_level, conditions)
    meals = get_meals(food_pref)

    # ---------------- AI SUMMARY ----------------
    st.markdown("## 🧠 Meal Plan Decision")

    if plan_type == "Modified Meal Plan":
        st.error(plan_type)
        st.write("**Reason for modification:**")
        for r in reasons:
            st.write("•", r)
    else:
        st.success(plan_type)
        st.write("All health parameters are within normal range.")

    # ---------------- MEAL PLAN UI ----------------
    st.markdown("## 🍽️ One-Day Detailed Meal Plan")

    for meal, items in meals.items():
        st.markdown(f"### {meal}")
        meal_cal = 0
        for item, kcal, carbs, protein, fat in items:
            meal_cal += kcal
            st.write(
                f"- **{item}** → {kcal} kcal "
                f"(Carbs: {carbs}g | Protein: {protein}g | Fat: {fat}g)"
            )
        st.info(f"Total {meal.split()[0]} Calories: {meal_cal} kcal")

    # ---------------- CALORIE PIE CHART ----------------
    st.markdown("## 📊 Calorie Distribution")
    labels = list(meals.keys())
    values = [sum(k for _, k, _, _, _ in m) for m in meals.values()]

    fig, ax = plt.subplots()
    ax.pie(values, labels=labels, autopct="%1.1f%%", startangle=90)
    ax.axis("equal")
    st.pyplot(fig)

    # ---------------- PDF ----------------
    def generate_pdf():
        buffer = io.BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=A4)
        styles = getSampleStyleSheet()
        elements = []

        title = ParagraphStyle(
            "title", fontSize=18, alignment=1, spaceAfter=12
        )

        elements.append(Paragraph("HealMeal – One Day Diet Plan", title))
        elements.append(Paragraph(f"Name: {name}", styles["Normal"]))
        elements.append(Paragraph(f"Age: {age}", styles["Normal"]))
        elements.append(Paragraph(f"Food Preference: {food_pref}", styles["Normal"]))
        elements.append(Spacer(1, 10))

        elements.append(Paragraph(f"<b>{plan_type}</b>", styles["Normal"]))

        if reasons:
            elements.append(Paragraph("Reason for modification:", styles["Normal"]))
            for r in reasons:
                elements.append(Paragraph(f"- {r}", styles["Normal"]))

        elements.append(Spacer(1, 12))

        table_data = [["Meal Timing", "Diet Plan"]]
        for meal, items in meals.items():
            diet_items = ", ".join([item for item, _, _, _, _ in items])
            table_data.append([meal, diet_items])

        table = Table(table_data, colWidths=[160, 330])
        table.setStyle([
            ("GRID", (0,0), (-1,-1), 1, colors.grey),
            ("BACKGROUND", (0,0), (-1,0), colors.lightgrey)
        ])

        elements.append(table)
        elements.append(Spacer(1, 12))

        elements.append(Paragraph("<b>Additional Instructions</b>", styles["Heading3"]))
        elements.append(Paragraph(
            "- Avoid oily and fried food<br/>"
            "- Drink adequate water<br/>"
            "- Prefer freshly cooked meals<br/>"
            "- Limit sugar and salt intake",
            styles["Normal"]
        ))

        elements.append(Spacer(1, 10))
        elements.append(Paragraph(
            "<i>This is a student Data Science project and does not replace professional nutritional advice.</i>",
            styles["Italic"]
        ))

        doc.build(elements)
        buffer.seek(0)
        return buffer

    st.download_button(
        "📄 Download Meal Plan PDF",
        generate_pdf(),
        "HealMeal_OneDay_Plan.pdf",
        "application/pdf"
    )
