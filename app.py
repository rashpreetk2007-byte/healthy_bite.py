import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from io import StringIO

# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="HealthyBite AI",
    page_icon="🥗",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================================
# CUSTOM CSS
# ============================================================

st.markdown("""
<style>

@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;500;600;700;800&display=swap');

html, body, [class*="css"] {
    font-family: 'Poppins', sans-serif;
}

.stApp {
    background: linear-gradient(135deg, #f8fff8 0%, #fffdf5 50%, #f2fbff 100%);
}

.main-title {
    font-size: 45px;
    font-weight: 800;
    text-align: center;
    margin-bottom: 0;
}

.subtitle {
    text-align: center;
    font-size: 18px;
    color: #666;
    margin-bottom: 30px;
}

.hero {
    padding: 35px;
    border-radius: 25px;
    background: linear-gradient(135deg, #dff8e8, #fff6cc);
    box-shadow: 0 8px 25px rgba(0,0,0,0.08);
    text-align: center;
    margin-bottom: 25px;
}

.card {
    padding: 22px;
    border-radius: 20px;
    background: white;
    box-shadow: 0 5px 20px rgba(0,0,0,0.07);
    margin-bottom: 15px;
}

.metric-card {
    padding: 20px;
    border-radius: 18px;
    background: white;
    text-align: center;
    box-shadow: 0 5px 18px rgba(0,0,0,0.07);
}

.metric-title {
    font-size: 15px;
    color: #777;
}

.metric-value {
    font-size: 30px;
    font-weight: 700;
}

.section-title {
    font-size: 28px;
    font-weight: 700;
    margin-top: 25px;
    margin-bottom: 15px;
}

.food-card {
    padding: 18px;
    border-radius: 18px;
    background: white;
    box-shadow: 0 4px 15px rgba(0,0,0,0.06);
    min-height: 125px;
}

.tip-card {
    padding: 18px;
    border-radius: 18px;
    background: linear-gradient(135deg, #fffdf1, #f1fff5);
    margin-bottom: 12px;
}

.warning-card {
    padding: 18px;
    border-radius: 18px;
    background: #fff4e5;
    border-left: 5px solid #f59e0b;
}

.success-card {
    padding: 18px;
    border-radius: 18px;
    background: #ecfff2;
    border-left: 5px solid #22c55e;
}

.footer {
    text-align: center;
    color: #777;
    padding: 30px;
    margin-top: 40px;
}

</style>
""", unsafe_allow_html=True)

# ============================================================
# FUNCTIONS
# ============================================================

def calculate_bmi(weight, height):
    height_m = height / 100
    return weight / (height_m ** 2)


def bmi_category(bmi):
    if bmi < 18.5:
        return "Underweight"
    elif bmi < 25:
        return "Healthy Range"
    elif bmi < 30:
        return "Overweight"
    else:
        return "Obesity Range"


def bmi_color(category):
    if category == "Underweight":
        return "orange"
    elif category == "Healthy Range":
        return "green"
    elif category == "Overweight":
        return "orange"
    else:
        return "red"


def get_food_recommendations(diet):
    if diet == "Vegetarian":
        return [
            "🥛 Milk / Curd",
            "🥜 Nuts & Seeds",
            "🫘 Dal & Beans",
            "🧀 Paneer",
            "🌾 Whole Grains",
            "🥦 Vegetables",
            "🍎 Fruits"
        ]

    elif diet == "Vegan":
        return [
            "🥜 Nuts & Seeds",
            "🫘 Lentils & Beans",
            "🌱 Tofu",
            "🥑 Avocado",
            "🌾 Whole Grains",
            "🥦 Vegetables",
            "🍎 Fruits"
        ]

    else:
        return [
            "🥚 Eggs",
            "🐟 Fish",
            "🍗 Lean Chicken",
            "🥛 Milk / Curd",
            "🫘 Dal & Beans",
            "🥦 Vegetables",
            "🍎 Fruits"
        ]


def get_meal_plan(diet):
    if diet == "Vegetarian":
        return {
            "🌅 Breakfast": "Oats + milk + banana / vegetable poha",
            "☀️ Mid-Morning": "Fruit + handful of nuts",
            "🍛 Lunch": "Dal + roti/rice + vegetables + curd",
            "🌆 Evening Snack": "Roasted chana / sprouts",
            "🌙 Dinner": "Paneer/tofu + vegetables + roti",
            "💧 Water": "Drink water regularly according to thirst and individual needs"
        }

    elif diet == "Vegan":
        return {
            "🌅 Breakfast": "Oats with plant-based milk + fruit",
            "☀️ Mid-Morning": "Fruit + nuts",
            "🍛 Lunch": "Dal + rice/roti + vegetables",
            "🌆 Evening Snack": "Roasted chana / sprouts",
            "🌙 Dinner": "Tofu + vegetables + whole grains",
            "💧 Water": "Drink water regularly according to thirst and individual needs"
        }

    else:
        return {
            "🌅 Breakfast": "Eggs + whole-grain toast + fruit",
            "☀️ Mid-Morning": "Fruit + nuts",
            "🍛 Lunch": "Dal + rice/roti + vegetables + curd",
            "🌆 Evening Snack": "Boiled egg / roasted chana",
            "🌙 Dinner": "Lean protein + vegetables + roti",
            "💧 Water": "Drink water regularly according to thirst and individual needs"
        }


def get_month_plan(months):
    plans = {
        1: [
            "Week 1 — Establish regular meal timing",
            "Week 2 — Increase fruits and vegetables",
            "Week 3 — Add balanced protein sources",
            "Week 4 — Review eating consistency"
        ],

        2: [
            "Month 1 — Establish regular meal timing",
            "Month 2 — Improve food quality and meal balance"
        ],

        3: [
            "Month 1 — Establish healthy routines",
            "Month 2 — Improve food variety",
            "Month 3 — Build consistent lifestyle habits"
        ],

        4: [
            "Month 1 — Establish healthy routines",
            "Month 2 — Improve food variety",
            "Month 3 — Focus on consistency",
            "Month 4 — Review progress"
        ],

        5: [
            "Month 1 — Establish healthy routines",
            "Month 2 — Improve food quality",
            "Month 3 — Improve protein and fiber intake",
            "Month 4 — Build consistency",
            "Month 5 — Review overall progress"
        ]
    }

    return plans.get(months, plans[1])


# ============================================================
# HEADER
# ============================================================

st.markdown("""
<div class="hero">

<h1 class="main-title">🥗 HealthyBite AI</h1>

<p class="subtitle">
Smart Health Analysis & Personalized Diet Planner
</p>

<p>
Plan better meals • Understand your BMI • Track your progress • Build healthier habits
</p>

</div>
""", unsafe_allow_html=True)

# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:

    st.header("🥗 HealthyBite AI")

    st.write("Navigation")

    page = st.radio(
        "Go to",
        [
            "🏠 Home",
            "👤 Health Analysis",
            "📊 Dashboard",
            "🍎 Food & Diet",
            "🏃 Exercise",
            "📈 Progress Tracker",
            "💡 Health Tips",
            "📄 Report"
        ]
    )

    st.divider()

    st.info(
        "Educational student project.\n\n"
        "This application does not provide medical diagnosis or treatment."
    )

# ============================================================
# SESSION STATE
# ============================================================

if "analysed" not in st.session_state:
    st.session_state.analysed = False

if "user_data" not in st.session_state:
    st.session_state.user_data = {}

# ============================================================
# HOME
# ============================================================

if page == "🏠 Home":

    st.markdown("## 🌱 Welcome to HealthyBite AI")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown("""
        <div class="card">
        <h2>🧮</h2>
        <h3>BMI Analysis</h3>
        <p>Calculate BMI and understand the basic category.</p>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("""
        <div class="card">
        <h2>🍎</h2>
        <h3>Diet Planner</h3>
        <p>Get general food and meal-planning suggestions.</p>
        </div>
        """, unsafe_allow_html=True)

    with col3:
        st.markdown("""
        <div class="card">
        <h2>📊</h2>
        <h3>Progress Dashboard</h3>
        <p>Visualize your entered progress with charts.</p>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("## 🚀 How it works")

    steps = [
        ("1️⃣", "Enter Information"),
        ("2️⃣", "Analyse Health"),
        ("3️⃣", "View Dashboard"),
        ("4️⃣", "Get Diet Plan"),
        ("5️⃣", "Track Progress")
    ]

    cols = st.columns(5)

    for col, (number, text) in zip(cols, steps):
        with col:
            st.markdown(f"""
            <div class="metric-card">
            <h2>{number}</h2>
            <b>{text}</b>
            </div>
            """, unsafe_allow_html=True)

# ============================================================
# HEALTH ANALYSIS
# ============================================================

elif page == "👤 Health Analysis":

    st.markdown("## 👤 Personal Information")

    col1, col2, col3 = st.columns(3)

    with col1:
        name = st.text_input(
            "Name",
            value="Palak"
        )

        age = st.number_input(
            "Age",
            min_value=1,
            max_value=120,
            value=19
        )

    with col2:
        height = st.number_input(
            "Height (cm)",
            min_value=50.0,
            max_value=250.0,
            value=165.0,
            step=0.5
        )

        weight = st.number_input(
            "Weight (kg)",
            min_value=10.0,
            max_value=300.0,
            value=60.0,
            step=0.5
        )

    with col3:
        diet = st.selectbox(
            "Diet Preference",
            [
                "Vegetarian",
                "Non-Vegetarian",
                "Vegan"
            ]
        )

        activity = st.selectbox(
            "Activity Level",
            [
                "Low",
                "Moderate",
                "Active"
            ]
        )

    st.markdown("## 🩺 Health Update")

    health_update = st.text_area(
        "Tell us about your current health goal or concern",
        placeholder="Example: I want healthier food options..."
    )

    st.markdown("## 🎯 Your Goal")

    goal = st.selectbox(
        "Select your main goal",
        [
            "Healthy Eating",
            "Fitness",
            "General Wellness",
            "Weight Management"
        ]
    )

    st.markdown("## 📅 Diet Plan Duration")

    duration = st.selectbox(
        "Choose plan duration",
        [1, 2, 3, 4, 5],
        format_func=lambda x: f"{x} Month{'s' if x > 1 else ''}"
    )

    analyse = st.button(
        "🔍 ANALYSE MY HEALTH",
        use_container_width=True,
        type="primary"
    )

    if analyse:

        bmi = calculate_bmi(weight, height)
        category = bmi_category(bmi)

        st.session_state.user_data = {
            "name": name,
            "age": age,
            "height": height,
            "weight": weight,
            "diet": diet,
            "activity": activity,
            "health_update": health_update,
            "goal": goal,
            "duration": duration,
            "bmi": bmi,
            "category": category
        }

        st.session_state.analysed = True

        st.success("✅ Health analysis completed.")

    if st.session_state.analysed:

        data = st.session_state.user_data

        st.markdown("## 📊 Your HealthyBite Result")

        st.markdown(
            f"""
            <div class="success-card">
            <h2>🥗 HEALTHYBITE AI</h2>
            <h3>Personalized Health Analysis</h3>
            Hello, <b>{data['name']}</b> 👋<br>
            Here is your educational health analysis.
            </div>
            """,
            unsafe_allow_html=True
        )

        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.metric("⚖️ Weight", f"{data['weight']:.1f} kg")

        with col2:
            st.metric("📏 Height", f"{data['height']:.1f} cm")

        with col3:
            st.metric("🎂 Age", data["age"])

        with col4:
            st.metric("🧮 BMI", f"{data['bmi']:.1f}")

        st.markdown("## 🧮 BMI Analysis")

        bmi_col1, bmi_col2 = st.columns(2)

        with bmi_col1:

            st.markdown(
                f"""
                <div class="metric-card">
                <div class="metric-title">YOUR BMI</div>
                <div class="metric-value">{data['bmi']:.1f}</div>
                <h3>{data['category']}</h3>
                </div>
                """,
                unsafe_allow_html=True
            )

        with bmi_col2:

            fig = go.Figure(
                go.Indicator(
                    mode="gauge+number",
                    value=data["bmi"],
                    title={"text": "BMI Indicator"},
                    gauge={
                        "axis": {
                            "range": [10, 40]
                        },
                        "steps": [
                            {"range": [10, 18.5], "color": "#FFE0B2"},
                            {"range": [18.5, 25], "color": "#C8E6C9"},
                            {"range": [25, 30], "color": "#FFE0B2"},
                            {"range": [30, 40], "color": "#FFCDD2"}
                        ],
                        "threshold": {
                            "line": {"color": "black", "width": 4},
                            "thickness": 0.75,
                            "value": data["bmi"]
                        }
                    }
                )
            )

            fig.update_layout(height=300)

            st.plotly_chart(
                fig,
                use_container_width=True
            )

        st.caption(
            "BMI is a screening metric and should not be treated as a medical diagnosis."
          )
      # ============================================================
# DASHBOARD
# ============================================================

elif page == "📊 Dashboard":

    if not st.session_state.analysed:

        st.warning(
            "Please complete Health Analysis first."
        )

    else:

        data = st.session_state.user_data

        st.markdown("## 📊 HealthyBite Health Dashboard")

        st.markdown(
            f"""
            <div class="hero">
            <h2>Hello {data['name']} 👋</h2>
            <p>Here is your personalized educational dashboard.</p>
            </div>
            """,
            unsafe_allow_html=True
        )

        # ----------------------------------------------------
        # METRICS
        # ----------------------------------------------------

        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.metric(
                "BMI",
                f"{data['bmi']:.1f}"
            )

        with col2:
            st.metric(
                "Age",
                data["age"]
            )

        with col3:
            st.metric(
                "Weight",
                f"{data['weight']:.1f} kg"
            )

        with col4:
            st.metric(
                "Plan",
                f"{data['duration']} Month"
            )

        # ----------------------------------------------------
        # PIE CHART
        # ----------------------------------------------------

        st.markdown("## 🥧 Food Category Distribution")

        food_categories = pd.DataFrame({
            "Category": [
                "Vegetables",
                "Fruits",
                "Protein",
                "Whole Grains",
                "Healthy Fats"
            ],
            "Value": [
                25,
                20,
                20,
                20,
                15
            ]
        })

        fig_pie = px.pie(
            food_categories,
            names="Category",
            values="Value",
            hole=0.25,
            title="Balanced Food Categories"
        )

        st.plotly_chart(
            fig_pie,
            use_container_width=True
        )

        # ----------------------------------------------------
        # BAR CHART
        # ----------------------------------------------------

        st.markdown("## 📊 Nutrition Category Chart")

        nutrition = pd.DataFrame({
            "Nutrition": [
                "Protein",
                "Fiber",
                "Fruits",
                "Vegetables",
                "Whole Grains",
                "Healthy Fats"
            ],
            "Score": [
                80,
                85,
                75,
                90,
                78,
                70
            ]
        })

        fig_bar = px.bar(
            nutrition,
            x="Nutrition",
            y="Score",
            title="General Nutrition Focus",
            text="Score"
        )

        fig_bar.update_traces(
            textposition="outside"
        )

        st.plotly_chart(
            fig_bar,
            use_container_width=True
        )

        # ----------------------------------------------------
        # LINE CHART
        # ----------------------------------------------------

        st.markdown("## 📈 Example Progress Trend")

        weeks = list(range(1, 9))

        trend = pd.DataFrame({
            "Week": weeks,
            "Weight": [
                data["weight"],
                data["weight"] * 0.998,
                data["weight"] * 0.996,
                data["weight"] * 0.995,
                data["weight"] * 0.994,
                data["weight"] * 0.993,
                data["weight"] * 0.992,
                data["weight"] * 0.991
            ]
        })

        fig_line = px.line(
            trend,
            x="Week",
            y="Weight",
            markers=True,
            title="Illustrative Weight Trend"
        )

        st.plotly_chart(
            fig_line,
            use_container_width=True
        )

        st.caption(
            "This is an illustrative visualization, not a prediction or prescribed weight-loss target."
        )

        # ----------------------------------------------------
        # DONUT CHART
        # ----------------------------------------------------

        st.markdown("## 🍩 Daily Meal Distribution")

        meals = pd.DataFrame({
            "Meal": [
                "Breakfast",
                "Lunch",
                "Snack",
                "Dinner"
            ],
            "Percentage": [
                25,
                35,
                15,
                25
            ]
        })

        fig_donut = px.pie(
            meals,
            names="Meal",
            values="Percentage",
            hole=0.60,
            title="Daily Meal Distribution"
        )

        st.plotly_chart(
            fig_donut,
            use_container_width=True
        )

        # ----------------------------------------------------
        # RADAR CHART
        # ----------------------------------------------------

        st.markdown("## 🕸️ Lifestyle Profile")

        activity_scores = {
            "Low": 40,
            "Moderate": 65,
            "Active": 85
        }

        selected_activity_score = activity_scores[data["activity"]]

        categories = [
            "Nutrition",
            "Activity",
            "Hydration",
            "Sleep",
            "Consistency"
        ]

        values = [
            75,
            selected_activity_score,
            70,
            75,
            65
        ]

        fig_radar = go.Figure()

        fig_radar.add_trace(
            go.Scatterpolar(
                r=values,
                theta=categories,
                fill="toself",
                name="Lifestyle Profile"
            )
        )

        fig_radar.update_layout(
            polar=dict(
                radialaxis=dict(
                    visible=True,
                    range=[0, 100]
                )
            ),
            title="Lifestyle Profile"
        )

        st.plotly_chart(
            fig_radar,
            use_container_width=True
      )
      # ============================================================
# FOOD & DIET
# ============================================================

elif page == "🍎 Food & Diet":

    if not st.session_state.analysed:

        st.warning(
            "Please complete Health Analysis first."
        )

    else:

        data = st.session_state.user_data

        st.markdown("## 🍎 Food Recommendations")

        foods = get_food_recommendations(
            data["diet"]
        )

        cols = st.columns(3)

        for i, food in enumerate(foods):

            with cols[i % 3]:

                st.markdown(
                    f"""
                    <div class="food-card">
                    <h3>{food}</h3>
                    <p>General healthy food option.</p>
                    </div>
                    """,
                    unsafe_allow_html=True
                )

        st.markdown("## 🚫 Foods to Limit")

        limit_foods = [
            "⚠️ Highly processed snacks",
            "⚠️ Excess sugary drinks",
            "⚠️ Frequent deep-fried foods",
            "⚠️ Excessively salty foods",
            "⚠️ Skipping regular meals"
        ]

        for item in limit_foods:
            st.write(item)

        st.markdown("## 🍽️ Daily Meal Planner")

        meal_plan = get_meal_plan(
            data["diet"]
        )

        for meal, description in meal_plan.items():

            st.markdown(
                f"""
                <div class="card">
                <h3>{meal}</h3>
                <p>{description}</p>
                </div>
                """,
                unsafe_allow_html=True
            )

        st.markdown("## 📅 Your Plan")

        plans = get_month_plan(
            data["duration"]
        )

        for plan in plans:
            st.success(plan)

# ============================================================
# EXERCISE
# ============================================================

elif page == "🏃 Exercise":

    if not st.session_state.analysed:

        st.warning(
            "Please complete Health Analysis first."
        )

    else:

        data = st.session_state.user_data

        st.markdown("## 🏃 Healthy Activity Plan")

        activities = [
            ("🚶 Walking", "Comfortable walking as appropriate for your fitness level."),
            ("🧘 Stretching", "Gentle mobility and stretching."),
            ("🏋️ Strength", "Basic strength exercises when appropriate."),
            ("🧘‍♀️ Flexibility", "Gentle flexibility work."),
            ("🚴 Cardio", "Choose an enjoyable cardiovascular activity.")
        ]

        cols = st.columns(2)

        for i, (title, description) in enumerate(activities):

            with cols[i % 2]:

                st.markdown(
                    f"""
                    <div class="card">
                    <h3>{title}</h3>
                    <p>{description}</p>
                    </div>
                    """,
                    unsafe_allow_html=True
                )

        st.markdown("## 🎯 Activity Level")

        st.info(
            f"Your selected activity level: {data['activity']}"
        )

        st.warning(
            "Exercise recommendations here are general educational suggestions. "
            "Choose activities appropriate for your abilities and seek professional "
            "advice when you have medical concerns or exercise limitations."
        )

# ============================================================
# PROGRESS TRACKER
# ============================================================

elif page == "📈 Progress Tracker":

    st.markdown("## 📈 Weekly Progress Tracker")

    st.write(
        "Enter your own measurements. The charts below will use the data you enter."
    )

    progress_data = []

    for week in range(1, 9):

        st.markdown(f"### Week {week}")

        col1, col2, col3, col4 = st.columns(4)

        with col1:
            week_weight = st.number_input(
                f"Weight {week} (kg)",
                min_value=0.0,
                max_value=300.0,
                value=0.0,
                key=f"weight_{week}"
            )

        with col2:
            water = st.number_input(
                f"Water {week} (glasses)",
                min_value=0,
                max_value=30,
                value=0,
                key=f"water_{week}"
            )

        with col3:
            exercise = st.number_input(
                f"Exercise {week} (min)",
                min_value=0,
                max_value=1000,
                value=0,
                key=f"exercise_{week}"
            )

        with col4:
            consistency = st.slider(
                f"Meal consistency {week} (%)",
                0,
                100,
                0,
                key=f"consistency_{week}"
            )

        progress_data.append({
            "Week": week,
            "Weight": week_weight,
            "Water": water,
            "Exercise": exercise,
            "Consistency": consistency
        })

    df_progress = pd.DataFrame(progress_data)

    st.markdown("## 📊 Your Progress Charts")

    valid_weight = df_progress[
        df_progress["Weight"] > 0
    ]

    if not valid_weight.empty:

        fig_weight = px.line(
            valid_weight,
            x="Week",
            y="Weight",
            markers=True,
            title="Weight Progress"
        )

        st.plotly_chart(
            fig_weight,
            use_container_width=True
        )

    valid_exercise = df_progress[
        df_progress["Exercise"] > 0
    ]

    if not valid_exercise.empty:

        fig_exercise = px.bar(
            valid_exercise,
            x="Week",
            y="Exercise",
            title="Exercise Minutes"
        )

        st.plotly_chart(
            fig_exercise,
            use_container_width=True
        )

    fig_consistency = px.line(
        df_progress,
        x="Week",
        y="Consistency",
        markers=True,
        title="Meal Consistency"
    )

    st.plotly_chart(
        fig_consistency,
        use_container_width=True
    )

    st.markdown("## 📋 Progress Table")

    st.dataframe(
        df_progress,
        use_container_width=True
    )

    csv = df_progress.to_csv(
        index=False
    )

    st.download_button(
        "⬇️ Download Progress CSV",
        data=csv,
        file_name="healthy_bite_progress.csv",
        mime="text/csv",
        use_container_width=True
    )

# ============================================================
# HEALTH TIPS
# ============================================================

elif page == "💡 Health Tips":

    st.markdown("## 💡 HealthyBite Health Tips")

    tips = [
        ("🥗 Balanced Meals",
         "Try to include a variety of food groups across your meals."),

        ("💧 Hydration",
         "Drink fluids regularly and adjust intake for your environment and activity."),

        ("🍎 Fruits & Vegetables",
         "Include a variety of fruits and vegetables in your eating pattern."),

        ("🌾 Whole Grains",
         "Choose whole-grain foods when suitable for your dietary needs."),

        ("🥜 Protein",
         "Include suitable protein sources such as beans, lentils, dairy, eggs, tofu or other foods that fit your diet."),

        ("😴 Sleep",
         "Maintain a regular sleep routine and prioritize adequate rest."),

        ("🏃 Physical Activity",
         "Choose regular physical activity that is appropriate for your abilities."),

        ("⏰ Meal Routine",
         "Avoid frequently skipping meals if a regular meal pattern works better for you."),

        ("🍟 Processed Foods",
         "Limit excessive intake of highly processed foods."),

        ("🧠 Mindful Eating",
         "Pay attention to hunger, fullness and the overall quality of your meals.")
    ]

    for title, text in tips:

        st.markdown(
            f"""
            <div class="tip-card">
            <h3>{title}</h3>
            <p>{text}</p>
            </div>
            """,
            unsafe_allow_html=True
        )

# ============================================================
# REPORT
# ============================================================

elif page == "📄 Report":

    if not st.session_state.analysed:

        st.warning(
            "Please complete Health Analysis first."
        )

    else:

        data = st.session_state.user_data

        st.markdown("## 📄 HealthyBite Report")

        report = f"""
HEALTHYBITE AI
Smart Health Analysis & Personalized Diet Planner

----------------------------------------

PERSONAL INFORMATION

Name: {data['name']}
Age: {data['age']}
Height: {data['height']} cm
Weight: {data['weight']} kg

Diet Preference: {data['diet']}
Activity Level: {data['activity']}
Goal: {data['goal']}
Plan Duration: {data['duration']} Month(s)

----------------------------------------

BMI ANALYSIS

BMI: {data['bmi']:.1f}
Category: {data['category']}

BMI is a screening metric and is not a medical diagnosis.

----------------------------------------

HEALTH UPDATE

{data['health_update'] if data['health_update'] else 'No additional health information provided.'}

----------------------------------------

RECOMMENDED FOODS

"""

        for food in get_food_recommendations(
            data["diet"]
        ):
            report += f"{food}\n"

        report += """

----------------------------------------

FOODS TO LIMIT

Highly processed snacks
Excess sugary drinks
Frequent deep-fried foods
Excessively salty foods
Skipping regular meals

----------------------------------------

DAILY MEAL PLAN

"""

        for meal, description in get_meal_plan(
            data["diet"]
        ).items():
            report += f"{meal}: {description}\n"

        report += """

----------------------------------------

HEALTH TIPS

Balanced meals
Hydration
Fruits and vegetables
Whole grains
Suitable protein sources
Adequate sleep
Regular physical activity
Mindful eating

----------------------------------------

IMPORTANT NOTICE

This is an educational student project.
HealthyBite AI does not provide medical diagnosis,
treatment, or individualized medical advice.

For medical, nutritional, or weight-management
decisions, consult a qualified healthcare professional.
"""

        st.text_area(
            "Generated Report",
            report,
            height=600
        )

        st.download_button(
            "⬇️ Download HealthyBite Report",
            data=report,
            file_name="HealthyBite_AI_Report.txt",
            mime="text/plain",
            use_container_width=True
        )

# ============================================================
# FOOTER
# ============================================================

st.markdown("""
<div class="footer">

<hr>

🥗 <b>HealthyBite AI</b>

<p>
Python • Streamlit • Pandas • NumPy • Plotly
</p>

<p>
Educational Student Project
</p>

<p>
⚠️ This application does not provide medical diagnosis or treatment.
</p>

</div>
""", unsafe_allow_html=True)
