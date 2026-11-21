
import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import datetime

from integration import run_tournament

# =====================================================
# PAGE CONFIG
# =====================================================
st.set_page_config(
    page_title="        SPORTS TOURNAMENT | SCHEDULING SYSTEM",
    page_icon="🏆",
    layout="wide",
    initial_sidebar_state="expanded"
)

# =====================================================
# THEME / CSS
# =====================================================
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

:root {
    --bg: #090E1A;
    --panel: #111A2B;
    --panel2: #151F33;
    --border: #26334A;
    --text: #F1F5FC;
    --muted: #8795AD;
    --blue: #6D8EFF;
    --purple: #A78BFA;
    --cyan: #39C6D8;
    --green: #38D9A9;
}

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
}

.stApp {
    background:
        radial-gradient(ellipse at 15% 0%, rgba(75, 103, 210, .13), transparent 35%),
        radial-gradient(ellipse at 90% 15%, rgba(132, 82, 205, .10), transparent 30%),
        var(--bg);
    color: var(--text);
}

header[data-testid="stHeader"] {
    background: transparent;
}

.block-container {
    padding-top: 1.7rem;
    padding-bottom: 3rem;
    max-width: 1500px;
}

/* Sidebar */
section[data-testid="stSidebar"] {
    background: #0D1525;
    border-right: 1px solid var(--border);
}

section[data-testid="stSidebar"] > div {
    padding-top: 1.5rem;
}

section[data-testid="stSidebar"] * {
    color: #DCE5F5;
}

section[data-testid="stSidebar"] .stRadio > div {
    gap: 9px;
}

section[data-testid="stSidebar"] .stRadio label {
    background: transparent;
    border: 1px solid transparent;
    border-radius: 10px;
    padding: 9px 12px;
    transition: .2s;
}

section[data-testid="stSidebar"] .stRadio label:hover {
    background: #192640;
    border-color: #2C3C59;
}

section[data-testid="stSidebar"] .stRadio label:has(input:checked) {
    background: linear-gradient(100deg, #263B69, #222C50);
    border: 1px solid #526DC0;
}

/* Top bar */
.topbar {
    display: flex;
    justify-content: space-between;
    align-items: center;
    background: rgba(17, 26, 43, .85);
    border: 1px solid var(--border);
    border-radius: 16px;
    padding: 18px 24px;
    margin-bottom: 32px;
    box-shadow: 0 10px 35px rgba(0,0,0,.16);
}

.brand {
    font-size: 23px;
    font-weight: 800;
    letter-spacing: -.8px;
    color: #F5F7FF;
}

.brand span {
    color: var(--blue);
}

.brand-sub {
    color: var(--muted);
    font-size: 11px;
    letter-spacing: 1.2px;
    margin-top: 5px;
}

.live-status {
    color: #45D6A4;
    background: rgba(56,217,169,.10);
    border: 1px solid rgba(56,217,169,.25);
    border-radius: 30px;
    padding: 7px 13px;
    font-size: 11px;
    font-weight: 700;
}

/* Headings */
.page-title {
    font-size: 31px;
    font-weight: 800;
    letter-spacing: -1px;
    color: var(--text);
    margin-bottom: 5px;
}

.page-subtitle {
    font-size: 13px;
    color: var(--muted);
    margin-bottom: 25px;
}

.eyebrow {
    color: var(--blue);
    text-transform: uppercase;
    letter-spacing: 2px;
    font-size: 10px;
    font-weight: 800;
    margin-bottom: 8px;
}

/* Cards */
.metric-card {
    background: linear-gradient(145deg, #17243A, #111A2B);
    border: 1px solid #2A3A56;
    border-radius: 16px;
    padding: 19px;
    min-height: 142px;
    box-shadow: 0 8px 24px rgba(0,0,0,.13);
    transition: .25s;
}

.metric-card:hover {
    transform: translateY(-4px);
    border-color: #657ED0;
    box-shadow: 0 12px 30px rgba(56, 91, 180, .13);
}

.metric-top {
    display: flex;
    justify-content: space-between;
    align-items: center;
}

.metric-label {
    color: #98A8C1;
    font-size: 12px;
    font-weight: 600;
}

.metric-icon {
    width: 36px;
    height: 36px;
    display: flex;
    align-items: center;
    justify-content: center;
    border-radius: 11px;
    font-size: 17px;
    background: rgba(109,142,255,.14);
}

.metric-value {
    font-size: 30px;
    font-weight: 800;
    color: #F4F7FF;
    margin-top: 13px;
    letter-spacing: -1px;
}

.metric-note {
    color: #8795AD;
    font-size: 11px;
    margin-top: 5px;
}

.panel {
    background: linear-gradient(145deg, #141F32, #101827);
    border: 1px solid var(--border);
    border-radius: 16px;
    padding: 20px;
    margin-bottom: 18px;
    box-shadow: 0 8px 24px rgba(0,0,0,.10);
}

.panel-title {
    color: #F1F5FC;
    font-size: 15px;
    font-weight: 700;
    margin-bottom: 4px;
}

.panel-subtitle {
    color: #8291A9;
    font-size: 11px;
    margin-bottom: 15px;
}

.info-box {
    background: rgba(109,142,255,.08);
    border: 1px solid rgba(109,142,255,.22);
    border-radius: 12px;
    padding: 14px;
    color: #B9C8E8;
    font-size: 12px;
}

/* Streamlit widgets */
.stButton > button {
    background: linear-gradient(110deg, #5479E8, #8468E8);
    color: white !important;
    border: 1px solid #8194F1;
    border-radius: 10px;
    padding: 10px 20px;
    min-height: 43px;
    font-weight: 700;
    transition: .2s;
    box-shadow: 0 5px 18px rgba(93, 112, 220, .18);
}

.stButton > button:hover {
    transform: translateY(-2px);
    border-color: #B4C1FF;
    box-shadow: 0 8px 24px rgba(93, 112, 220, .30);
}

.stDownloadButton > button {
    background: #192941;
    color: #DCE8FF !important;
    border: 1px solid #405578;
    border-radius: 10px;
    font-weight: 600;
}

.stDownloadButton > button:hover {
    background: #263B5D;
    border-color: #6D8EFF;
}

.stTextInput input, .stNumberInput input {
    background: #101A2B !important;
    color: #F1F5FC !important;
    border: 1px solid #34445F !important;
    border-radius: 9px !important;
}

.stSelectbox div[data-baseweb="select"] > div {
    background: #101A2B;
    border-color: #34445F;
    border-radius: 9px;
    color: white;
}

.stCheckbox label, .stRadio label {
    color: #C9D3E4 !important;
}

label, .stMarkdown p {
    color: #C9D3E4;
}

div[data-testid="stMetric"] {
    background: #141F32;
    border: 1px solid #293952;
    padding: 15px;
    border-radius: 12px;
}

/* Dataframe */
[data-testid="stDataFrame"] {
    border: 1px solid #2B3A53;
    border-radius: 12px;
    overflow: hidden;
}

/* Tabs */
.stTabs [data-baseweb="tab-list"] {
    gap: 12px;
    background: transparent;
}

.stTabs [data-baseweb="tab"] {
    background: #141F32;
    border: 1px solid #2B3A53;
    border-radius: 9px;
    padding: 8px 17px;
    color: #AAB8CE;
}

.stTabs [aria-selected="true"] {
    background: #293D6C !important;
    color: white !important;
    border-color: #6D8EFF !important;
}

hr {
    border-color: #26334A;
}

div[data-testid="stAlert"] {
    border-radius: 11px;
}

footer {
    visibility: hidden;
}

/* Configuration Summary Metrics */
div[data-testid="stMetric"] {
    background: linear-gradient(145deg, #1B2B45, #17243A) !important;
    border: 1px solid #354968 !important;
    border-radius: 14px !important;
    padding: 18px 20px !important;
    box-shadow: 0 6px 18px rgba(0,0,0,.15);
}

/* Metric Labels: Teams, Venues, Available Days */
div[data-testid="stMetric"] label,
div[data-testid="stMetricLabel"],
div[data-testid="stMetricLabel"] p {
    color: #AFC1DF !important;
    font-size: 13px !important;
    font-weight: 600 !important;
}

/* Metric Values: 8, 2, 7 */
div[data-testid="stMetricValue"],
div[data-testid="stMetricValue"] div {
    color: #FFFFFF !important;
    font-size: 30px !important;
    font-weight: 800 !important;
}

/* Metric Hover Effect */
div[data-testid="stMetric"]:hover {
    border-color: #6D8EFF !important;
    transform: translateY(-3px);
    transition: .2s ease;
}

/* Algorithm Parameters - Input Labels */
.stTextInput label,
.stNumberInput label,
.stSelectbox label,
.stSlider label,
.stMultiSelect label,
.stDateInput label,
.stTimeInput label {
    color: #E2EAF8 !important;
    font-size: 13px !important;
    font-weight: 600 !important;
}

/* Input Help Text */
.stTextInput [data-testid="stWidgetLabel"] p,
.stNumberInput [data-testid="stWidgetLabel"] p,
.stSelectbox [data-testid="stWidgetLabel"] p,
.stSlider [data-testid="stWidgetLabel"] p {
    color: #AFC1DF !important;
}

/* Input Labels - Required Mark */
.stTextInput label span,
.stNumberInput label span,
.stSelectbox label span {
    color: #E2EAF8 !important;
}

/* ============================= */
/* INPUT FIELDS - DARK THEME     */
/* ============================= */

/* Text, Number, Date & Time Inputs */
.stTextInput input,
.stNumberInput input,
.stDateInput input,
.stTimeInput input,
.stTextArea textarea {
    background-color: #1E293B !important;
    color: #F8FAFC !important;
    -webkit-text-fill-color: #F8FAFC !important;
    border: 1px solid #475569 !important;
    caret-color: #F8FAFC !important;
}

/* Placeholder Text */
.stTextInput input::placeholder,
.stTextArea textarea::placeholder {
    color: #94A3B8 !important;
    -webkit-text-fill-color: #94A3B8 !important;
    opacity: 1 !important;
}

/* Selectbox */
.stSelectbox div[data-baseweb="select"] > div {
    background-color: #1E293B !important;
    color: #F8FAFC !important;
    border-color: #475569 !important;
}

/* Selected Values */
.stSelectbox div[data-baseweb="select"] span {
    color: #F8FAFC !important;
}

/* Input Labels */
.stTextInput label,
.stNumberInput label,
.stDateInput label,
.stTimeInput label,
.stTextArea label,
.stSelectbox label {
    color: #E2E8F0 !important;
}

/* Dropdown Options */
div[data-baseweb="popover"] {
    background-color: #1E293B !important;
}

div[data-baseweb="popover"] li {
    color: #F8FAFC !important;
}

/* Focus Effect */
.stTextInput input:focus,
.stNumberInput input:focus,
.stDateInput input:focus,
.stTimeInput input:focus,
.stTextArea textarea:focus {
    border-color: #3B82F6 !important;
    box-shadow: 0 0 0 1px #3B82F6 !important;
}

</style>
""", unsafe_allow_html=True)



# =====================================================
# CHART STYLE
# =====================================================
def style_chart(fig, height=330):
    fig.update_layout(
        height=height,
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(family="Inter", color="#AAB8CE", size=11),
        margin=dict(l=10, r=10, t=25, b=10),
        hoverlabel=dict(
            bgcolor="#1B2940",
            bordercolor="#526A99",
            font=dict(color="white", family="Inter")
        ),
        xaxis=dict(
            showgrid=False,
            zeroline=False,
            color="#8999B3"
        ),
        yaxis=dict(
            gridcolor="rgba(130,150,185,.12)",
            zeroline=False,
            color="#8999B3"
        )
    )
    return fig


# =====================================================
# REUSABLE COMPONENTS
# =====================================================
def metric_card(label, value, icon, note):
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-top">
            <div class="metric-label">{label}</div>
            <div class="metric-icon">{icon}</div>
        </div>
        <div class="metric-value">{value}</div>
        <div class="metric-note">{note}</div>
    </div>
    """, unsafe_allow_html=True)


def panel_heading(title, subtitle=""):
    st.markdown(f"""
    <div class="panel-title">{title}</div>
    <div class="panel-subtitle">{subtitle}</div>
    """, unsafe_allow_html=True)


def page_heading(eyebrow, title, subtitle):
    st.markdown(f"""
    <div class="eyebrow">{eyebrow}</div>
    <div class="page-title">{title}</div>
    <div class="page-subtitle">{subtitle}</div>
    """, unsafe_allow_html=True)


# =====================================================
# SIDEBAR
# =====================================================
with st.sidebar:
    st.markdown("""
    <div style="padding: 10px 5px 28px;">
        <div style="font-size:28px;font-weight:800;color:white;letter-spacing:-1px;">
            🏆 SPORTS TOURNAMENT
        </div>
        <div style="font-size:10px;color:#8193B0;letter-spacing:3px;margin-top:4px;">
            SCHEDULING SYSTEM
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown(
        "<div style='font-size:10px;color:#7587A5;font-weight:800;letter-spacing:2px;margin-bottom:12px;'>WORKSPACE</div>",
        unsafe_allow_html=True
    )

    page = st.radio(
        "Navigation",
        ["Overview", "Configuration", "Schedule", "Analytics"],
        format_func=lambda x: {
            "Overview": "◈   Overview",
            "Configuration": "⚙   Configuration",
            "Schedule": "▦   Schedule",
            "Analytics": "◉   Analytics"
        }[x],
        label_visibility="collapsed"
    )

    st.markdown("<br><hr>", unsafe_allow_html=True)

    st.markdown("""
    <div style="background:#15233A;border:1px solid #2B3D5A;padding:14px;border-radius:12px;">
        <div style="font-size:11px;color:#8EA1C0;">PROJECT STATUS</div>
        <div style="font-size:14px;color:#42D9AA;font-weight:700;margin-top:7px;">
            ● Ready
        </div>
        <div style="font-size:10px;color:#8293AD;margin-top:6px;">
            Optimization workspace
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div style="position:fixed;bottom:25px;color:#667A99;font-size:10px;">
        SPORTS TOURNAMENT v1.0 · Tournament System
    </div>
    """, unsafe_allow_html=True)


# =====================================================
# TOP BAR
# =====================================================
st.markdown("""
<div class="topbar">
    <div>
        <div class="brand">SPORTS TOURNAMENT <span>OPTIMIZER</span></div>
        <div class="brand-sub">SMART TOURNAMENT SCHEDULING PLATFORM</div>
    </div>
    <div class="live-status">● SYSTEM ONLINE</div>
</div>
""", unsafe_allow_html=True)


# =====================================================
# OVERVIEW
# =====================================================

# =====================================================
# OVERVIEW
# =====================================================
if page == "Overview":

    config = st.session_state.get("config", {})
    optimization_results = st.session_state.get(
        "optimization_results", {}
    )
    all_matches = st.session_state.get("all_matches", [])

    # -------------------------------------------------
    # PAGE HEADER
    # -------------------------------------------------

    page_heading(
        "DASHBOARD / OVERVIEW",
        "Welcome to SPORTS TOURNAMENT.",
        "Your tournament operations, scheduling insights and optimization performance in one place."
    )

    # -------------------------------------------------
    # CHECK OPTIMIZATION STATUS
    # -------------------------------------------------

    optimization_completed = (
        st.session_state.get("optimization_completed", False)
        and bool(optimization_results)
    )

    teams = config.get("teams", [])
    venues = config.get("venues", [])

    total_matches = (
        len(all_matches)
        if all_matches
        else len(teams) * (len(teams) - 1) // 2
    )

    # -------------------------------------------------
    # FIND BEST ALGORITHM
    # -------------------------------------------------

    best_algorithm = None
    best_result = None

    if optimization_completed:

        valid_results = {
            name: result
            for name, result in optimization_results.items()
            if isinstance(result, dict)
            and result.get("fitness") is not None
        }

        # The Baseline is only a reference schedule; the "best"
        # result should come from the algorithm(s) the user ran.

        optimized_results = {
            name: result
            for name, result in valid_results.items()
            if name != "Baseline"
        }

        candidates = optimized_results or valid_results

        if candidates:
            best_algorithm = max(
                candidates,
                key=lambda name: candidates[name]["fitness"]
            )

            best_result = candidates[best_algorithm]

    best_fitness = (
        best_result["fitness"]
        if best_result
        else None
    )

    # -------------------------------------------------
    # STATUS MESSAGE
    # -------------------------------------------------

    if optimization_completed and best_result:

        st.success(
            f"Optimization completed · Best result: {best_algorithm}"
        )

    else:

        st.info(
            "No optimization results available yet. "
            "Go to Configuration and run the optimization first."
        )

    # -------------------------------------------------
    # TOP METRICS
    # -------------------------------------------------

    c1, c2, c3, c4 = st.columns(4)

    with c1:
        metric_card(
            "TOTAL TEAMS",
            str(len(teams)) if config else "—",
            "👥",
            "Participating teams"
        )

    with c2:
        metric_card(
            "VENUES",
            str(len(venues)) if config else "—",
            "🏟️",
            "Available locations"
        )

    with c3:
        metric_card(
            "TOTAL MATCHES",
            str(total_matches) if config else "—",
            "⚽",
            "Round-robin fixtures"
        )

    with c4:
        metric_card(
            "BEST FITNESS",
            f"{best_fitness:.4f}" if best_fitness is not None else "—",
            "✦",
            best_algorithm if best_algorithm else "Awaiting optimization"
        )

    st.write("")

    # -------------------------------------------------
    # ALGORITHM PERFORMANCE
    # -------------------------------------------------

    left, right = st.columns([1.6, 1])

    with left:

        st.markdown('<div class="panel">', unsafe_allow_html=True)

        panel_heading(
            "Optimization Performance",
            "Actual fitness scores across scheduling algorithms"
        )

        if optimization_completed and optimization_results:

            chart_data = []

            for name, result in optimization_results.items():

                if result.get("fitness") is not None:

                    chart_data.append({
                        "Algorithm": name,
                        "Fitness": float(result["fitness"])
                    })

            if chart_data:

                chart_df = pd.DataFrame(chart_data)

                colors = {
                    "Baseline": "#8496B3",
                    "Genetic Algorithm": "#718BFF",
                    "Memetic Algorithm": "#42D9AA"
                }

                fig = go.Figure()

                fig.add_trace(go.Bar(
                    x=chart_df["Algorithm"],
                    y=chart_df["Fitness"],
                    marker=dict(
                        color=[
                            colors.get(name, "#718BFF")
                            for name in chart_df["Algorithm"]
                        ],
                        line=dict(width=0)
                    ),
                    text=[
                        f"{value:.4f}"
                        for value in chart_df["Fitness"]
                    ],
                    textposition="outside",
                    textfont=dict(
                        color="#EAF0FF",
                        size=13
                    ),
                    hovertemplate=(
                        "<b>%{x}</b><br>"
                        "Fitness: %{y:.4f}"
                        "<extra></extra>"
                    )
                ))

                max_fitness = max(
                    chart_df["Fitness"].max(),
                    0.1
                )

                fig.update_yaxes(
                    range=[0, max_fitness * 1.25]
                )

                fig.update_layout(
                    showlegend=False
                )

                fig = style_chart(fig, 345)

                st.plotly_chart(
                    fig,
                    use_container_width=True
                )

            else:
                st.info("No fitness values available.")

        else:
            st.info(
                "The performance chart will appear after running the optimization."
            )

        st.markdown('</div>', unsafe_allow_html=True)

    
    # -------------------------------------------------
    # OPTIMIZATION SNAPSHOT
    # -------------------------------------------------

    with right:

        st.markdown('<div class="panel">', unsafe_allow_html=True)

        panel_heading(
            "Optimization Snapshot",
            "Performance summary"
        )

        if optimization_completed and optimization_results:

            colors = {
                "Baseline": "#8496B3",
                "Genetic Algorithm": "#718BFF",
                "Memetic Algorithm": "#42D9AA"
            }

            valid_results = {
                name: result
                for name, result in optimization_results.items()
                if isinstance(result, dict)
                and result.get("fitness") is not None
            }

            max_score = max(
                (
                    float(result["fitness"])
                    for result in valid_results.values()
                ),
                default=0
            )

            
            for name, result in valid_results.items():

                score = float(result["fitness"])
                color = colors.get(name, "#718BFF")

                progress = (
                    min(score / max_score, 1.0)
                    if max_score > 0 else 0
                )

                col1, col2 = st.columns([4, 1])

                with col1:
                    st.markdown(f"**{name}**")

                with col2:
                    st.markdown(
                        f"<p style='color:{color}; font-weight:700; text-align:right;'>{score:.4f}</p>",
                        unsafe_allow_html=True
                    )

                st.progress(progress)


            if best_algorithm:
                st.markdown(
                    f"""
                    <div class="info-box" style="margin-top:22px;">
                        ✦ Best performing algorithm:
                        <b>{best_algorithm}</b>
                    </div>
                    """,
                    unsafe_allow_html=True
                )

        else:
            st.info(
                "Algorithm performance will be displayed here after optimization."
            )

        st.markdown('</div>', unsafe_allow_html=True)


    # -------------------------------------------------
    # RECENT FIXTURES
    # -------------------------------------------------

    st.markdown('<div class="panel">', unsafe_allow_html=True)

    panel_heading(
        "Recent Fixtures",
        "A quick look at matches from the best generated schedule"
    )

    if optimization_completed and best_result:

        best_schedule = best_result.get("schedule", [])

        # Convert the returned schedule into a DataFrame
        if isinstance(best_schedule, pd.DataFrame):

            schedule_df = best_schedule.copy()

        elif isinstance(best_schedule, list):

            schedule_df = pd.DataFrame(best_schedule)

        elif isinstance(best_schedule, dict):

            try:
                schedule_df = pd.DataFrame(best_schedule)
            except Exception:
                schedule_df = pd.DataFrame()

        else:

            schedule_df = pd.DataFrame()

        if not schedule_df.empty:

            st.dataframe(
                schedule_df.head(4),
                use_container_width=True,
                hide_index=True,
                height=210
            )

            st.caption(
                f"Showing 4 of {len(schedule_df)} scheduled matches."
            )

        else:

            st.warning(
                "The optimization completed, but no schedule entries were returned."
            )

    else:

        st.info(
            "Your generated fixtures will appear here after running the optimization."
        )

    st.markdown('</div>', unsafe_allow_html=True)

    # -------------------------------------------------
    # ADDITIONAL PERFORMANCE DETAILS
    # -------------------------------------------------

    if optimization_completed and optimization_results:

        st.write("")

        st.markdown('<div class="panel">', unsafe_allow_html=True)

        panel_heading(
            "Performance Details",
            "Detailed metrics for each algorithm"
        )

        performance_rows = []

        for name, result in optimization_results.items():

            performance_rows.append({
                "Algorithm": name,
                "Fitness": round(float(result.get("fitness", 0)), 4),
                "Conflicts": result.get("conflicts", 0),
                "Unscheduled Matches": result.get(
                    "unscheduled_matches", 0
                ),
                "Execution Time (s)": round(
                    float(result.get("execution_time", 0)), 4
                )
            })

        performance_df = pd.DataFrame(performance_rows)

        st.dataframe(
            performance_df,
            use_container_width=True,
            hide_index=True
        )

        st.markdown('</div>', unsafe_allow_html=True)




# =====================================================
# CONFIGURATION
# =====================================================
elif page == "Configuration":

        

        page_heading(
            "WORKSPACE / SETUP",
            "Tournament Configuration",
            "Customize your tournament structure and optimization parameters."
        )

        # =================================================
        # INITIALIZE SESSION STATE
        # =================================================

        if "team_rows" not in st.session_state:
            st.session_state.team_rows = [
                {"id": 1, "name": "Team 1"},
                {"id": 2, "name": "Team 2"}
            ]
            st.session_state.team_next_id = 3

        if "venue_rows" not in st.session_state:
            st.session_state.venue_rows = [
                {"id": 1, "name": "Venue 1"}
            ]
            st.session_state.venue_next_id = 2

        if "availability" not in st.session_state:
            st.session_state.availability = {}

        if "selected_date" not in st.session_state:
            st.session_state.selected_date = datetime.date.today()

        # =================================================
        # CALLBACK FUNCTIONS
        # =================================================

        def add_team():
            new_id = st.session_state.team_next_id
            st.session_state.team_rows.append(
                {"id": new_id, "name": f"Team {new_id}"}
            )
            st.session_state.team_next_id += 1

        def remove_team(team_id):
            st.session_state.team_rows = [
                x for x in st.session_state.team_rows
                if x["id"] != team_id
            ]

        def add_venue():
            new_id = st.session_state.venue_next_id
            st.session_state.venue_rows.append(
                {"id": new_id, "name": f"Venue {new_id}"}
            )
            st.session_state.venue_next_id += 1

        def remove_venue(venue_id):
            st.session_state.venue_rows = [
                x for x in st.session_state.venue_rows
                if x["id"] != venue_id
            ]

        def add_time_slot():
            selected_date = st.session_state.selected_date
            selected_time = st.session_state.new_time

            date_key = selected_date.strftime("%Y-%m-%d")
            time_value = selected_time.strftime("%H:%M")

            if date_key not in st.session_state.availability:
                st.session_state.availability[date_key] = []

            if time_value not in st.session_state.availability[date_key]:
                st.session_state.availability[date_key].append(time_value)
                st.session_state.availability[date_key].sort()
            else:
                st.session_state.slot_message = "This time slot already exists."

        def remove_time_slot(date_key, time_value):
            if date_key in st.session_state.availability:
                st.session_state.availability[date_key].remove(time_value)

                if not st.session_state.availability[date_key]:
                    del st.session_state.availability[date_key]

        # =================================================
        # 01 / TEAMS & VENUES
        # =================================================

        left, right = st.columns([1.1, 1])

        with left:

            st.markdown('<div class="panel">', unsafe_allow_html=True)

            panel_heading(
                "01 / Teams",
                "Add participating teams"
            )

            st.caption(
                f"Total Teams: {len(st.session_state.team_rows)}"
            )

            for item in st.session_state.team_rows:

                col1, col2 = st.columns([5, 1])

                with col1:
                    st.text_input(
                        f"Team {item['id']}",
                        value=item["name"],
                        key=f"team_name_{item['id']}",
                        placeholder="Enter team name"
                    )

                with col2:
                    if len(st.session_state.team_rows) > 2:
                        st.write("")
                        st.write("")
                        st.button(
                            "✕",
                            key=f"remove_team_{item['id']}",
                            on_click=remove_team,
                            args=(item["id"],)
                        )

            st.button(
                "＋ Add Team",
                key="add_team_button",
                on_click=add_team
            )

            st.markdown('</div>', unsafe_allow_html=True)

        with right:

            st.markdown('<div class="panel">', unsafe_allow_html=True)

            panel_heading(
                "02 / Venues",
                "Add available venues"
            )

            st.caption(
                f"Total Venues: {len(st.session_state.venue_rows)}"
            )

            for item in st.session_state.venue_rows:

                col1, col2 = st.columns([5, 1])

                with col1:
                    st.text_input(
                        f"Venue {item['id']}",
                        value=item["name"],
                        key=f"venue_name_{item['id']}",
                        placeholder="Enter venue name"
                    )

                with col2:
                    if len(st.session_state.venue_rows) > 1:
                        st.write("")
                        st.write("")
                        st.button(
                            "✕",
                            key=f"remove_venue_{item['id']}",
                            on_click=remove_venue,
                            args=(item["id"],)
                        )

            st.button(
                "＋ Add Venue",
                key="add_venue_button",
                on_click=add_venue
            )

            st.markdown('</div>', unsafe_allow_html=True)

        # Collect names
        teams = [
            st.session_state.get(f"team_name_{x['id']}", "").strip()
            for x in st.session_state.team_rows
        ]

        venues = [
            st.session_state.get(f"venue_name_{x['id']}", "").strip()
            for x in st.session_state.venue_rows
        ]

        teams_valid = (
            len(teams) >= 2
            and all(teams)
            and len(set(x.lower() for x in teams)) == len(teams)
        )

        venues_valid = (
            len(venues) >= 1
            and all(venues)
            and len(set(x.lower() for x in venues)) == len(venues)
        )

        st.divider()

        # =================================================
        # 03 / TOURNAMENT AVAILABILITY
        # =================================================

        st.markdown('<div class="panel">', unsafe_allow_html=True)

        panel_heading(
            "03 / Tournament Availability",
            "Choose dates and add available time slots"
        )

        date_col, time_col, button_col = st.columns([1.2, 1, 0.8])

        with date_col:
            selected_date = st.date_input(
                "Select Date",
                value=st.session_state.selected_date,
                key="selected_date",
                min_value=datetime.date.today()
            )

        with time_col:
            selected_time = st.time_input(
                "Available Time",
                value=datetime.time(10, 0),
                key="new_time"
            )

        with button_col:
            st.write("")
            st.write("")
            st.button(
                "＋ Add Slot",
                key="add_slot_button",
                on_click=add_time_slot,
                use_container_width=True
            )

        if "slot_message" in st.session_state:
            st.warning(st.session_state.slot_message)
            del st.session_state.slot_message

        st.markdown("#### Added Availability")

        if st.session_state.availability:

            for date_key in sorted(st.session_state.availability):

                slots = st.session_state.availability[date_key]

                with st.expander(
                    f"📅 {date_key}  |  {len(slots)} Time Slots",
                    expanded=True
                ):

                    for slot in slots:

                        slot_col, remove_col = st.columns([5, 1])

                        with slot_col:
                            st.write(f"🕒 {slot}")

                        with remove_col:
                            st.button(
                                "✕",
                                key=f"remove_slot_{date_key}_{slot}",
                                on_click=remove_time_slot,
                                args=(date_key, slot)
                            )

        else:
            st.info("No availability added yet. Choose a date and time, then click Add Slot.")

        st.markdown('</div>', unsafe_allow_html=True)

        # Convert availability to integration format
        days_and_slots = {
            date_key: sorted(slots)
            for date_key, slots in st.session_state.availability.items()
            if slots
        }

        st.divider()

        # =================================================
        # 04 / ALGORITHM PARAMETERS
        # =================================================

        left, right = st.columns([1.1, 1])

        with left:

            st.markdown('<div class="panel">', unsafe_allow_html=True)

            panel_heading(
                "04 / Algorithm Parameters",
                "Control optimization"
            )

            algorithm = st.selectbox(
                "Optimization Method",
                ["Genetic Algorithm", "Memetic Algorithm", "Both"]
            )

            population = st.number_input(
                "Population Size",
                min_value=10,
                max_value=500,
                value=50
            )

            generations = st.number_input(
                "Number of Generations",
                min_value=1,
                max_value=1000,
                value=100
            )

            mutation_rate = st.slider(
                "Mutation Rate",
                min_value=0.0,
                max_value=1.0,
                value=0.2,
                step=0.05
            )

            st.markdown('</div>', unsafe_allow_html=True)

        with right:

            st.markdown('<div class="panel">', unsafe_allow_html=True)

            panel_heading(
                "05 / Scheduling Constraints",
                "Scheduling rules"
            )

            rest_constraint = st.checkbox(
                "Minimum rest period",
                value=True
            )

            rest_hours = st.number_input(
                "Rest period (hours)",
                min_value=0,
                max_value=336,
                value=48,
                step=1,
                help="Minimum hours between two matches of the same team. "
                     "Used when 'Minimum rest period' is enabled."
            )

            venue_constraint = st.checkbox(
                "Avoid venue conflicts",
                value=True
            )

            team_constraint = st.checkbox(
                "Avoid team conflicts",
                value=True
            )

            balance_constraint = st.checkbox(
                "Balance number of games",
                value=True
            )

            # The four toggles are passed to the scheduling engine so the
            # algorithms only optimize for the rules the user enabled.
            constraints_config = {
                "rest": rest_constraint,
                "venue": venue_constraint,
                "team": team_constraint,
                "balance": balance_constraint
            }

            st.markdown('</div>', unsafe_allow_html=True)

        # =================================================
        # VALIDATION
        # =================================================

        valid_inputs = True

        if not teams_valid:
            st.error("Please enter at least 2 unique team names.")

            valid_inputs = False

        if not venues_valid:
            st.error("Please enter at least 1 unique venue name.")

            valid_inputs = False

        if not days_and_slots:
            st.error("Please add at least one available date and time slot.")

            valid_inputs = False

        # =================================================
        # 06 / CONFIGURATION SUMMARY
        # =================================================

        st.markdown('<div class="panel">', unsafe_allow_html=True)

        panel_heading(
            "Configuration Summary",
            "Review your setup"
        )

        a, b, c, d = st.columns(4)

        a.metric("Teams", len(teams))
        b.metric("Venues", len(venues))
        c.metric("Available Days", len(days_and_slots))
        d.metric(
            "Time Slots",
            sum(len(slots) for slots in days_and_slots.values())
        )

        total_matches = len(teams) * (len(teams) - 1) // 2

        st.caption(f"Total Round-Robin Matches: {total_matches}")

        active_constraints = [
            label for label, enabled in [
                (f"Min. rest {rest_hours}h", rest_constraint),
                ("No venue conflicts", venue_constraint),
                ("No team conflicts", team_constraint),
                ("Balanced games", balance_constraint)
            ] if enabled
        ]

        st.caption(
            "Active constraints: "
            + (", ".join(active_constraints) if active_constraints else "None")
        )

    
        # =================================================
        # SAVE CONFIGURATION
        # =================================================

        current_config = {
            "teams": teams,
            "venues": venues,
            "days_and_slots": days_and_slots,
            "algorithm": algorithm,
            "population": population,
            "generations": generations,
            "mutation_rate": mutation_rate,
            "constraints": constraints_config,
            "rest_hours": rest_hours
        }

        if st.button(
            "✦ Save Configuration",
            use_container_width=True
        ):

            if valid_inputs:

                st.session_state["config"] = current_config

                st.success("Configuration saved successfully!")

            else:
                st.error("Please fix the configuration errors first.")

        # =================================================
        # RUN OPTIMIZATION
        # =================================================

        if st.button(
            "▶ Run Optimization",
            use_container_width=True,
            type="primary"
        ):

            if not valid_inputs:
                st.error("Please fix the configuration errors first.")

            else:
                try:
                    # Always optimize with the CURRENT UI values (including
                    # the 05 / Scheduling Constraints toggles) and keep the
                    # saved configuration in sync.
                    st.session_state["config"] = current_config

                    with st.spinner(
                        "Running optimization algorithms... Please wait."
                    ):

                        output = run_tournament(
                            teams=teams,
                            venues=venues,
                            days_and_slots=days_and_slots,
                            population_size=population,
                            generations=generations,
                            mutation_rate=mutation_rate,
                            constraints=constraints_config,
                            min_rest_hours=rest_hours,
                            algorithm=algorithm
                        )

                        st.session_state["optimization_results"] = output["results"]
                        st.session_state["all_matches"] = output["all_matches"]
                        st.session_state["constraints_applied"] = output["constraints_applied"]
                        st.session_state["min_rest_hours"] = output["min_rest_hours"]
                        st.session_state["selected_algorithm"] = output["algorithm"]
                        st.session_state["optimization_completed"] = True

                    st.success("Optimization completed successfully!")

                except Exception as error:
                    st.session_state["optimization_completed"] = False
                    st.error(f"Optimization failed: {error}")

        st.markdown('</div>', unsafe_allow_html=True)



# =====================================================
# SCHEDULE
# =====================================================

elif page == "Schedule":

        page_heading(
        "SCHEDULE",
        "Tournament Schedule",
        "View and export the generated tournament fixtures."
    )

        optimization_results = st.session_state.get(
            "optimization_results"
        )

        if not optimization_results:
            st.info(
                "No schedule available yet. "
                "Go to Configuration and run the optimization first."
            )

        else:
            # Select algorithm
            algorithm_names = list(optimization_results.keys())

            selected_algorithm = st.selectbox(
                "Select Algorithm",
                algorithm_names
            )

            selected_result = optimization_results[selected_algorithm]

            schedule = selected_result.get("schedule", [])

            if not schedule:
                st.warning("No matches were scheduled by this algorithm.")

            else:
                # Convert schedule to DataFrame
                schedule_df = pd.DataFrame(schedule)

                # Keep the expected columns and their order
                columns = [
                    "date",
                    "time",
                    "team1",
                    "team2",
                    "venue"
                ]

                schedule_df = schedule_df.reindex(columns=columns)

                # Sort schedule
                schedule_df = schedule_df.sort_values(
                    by=["date", "time", "venue"]
                ).reset_index(drop=True)

                # Rename columns for display
                display_df = schedule_df.rename(
                    columns={
                        "date": "Date",
                        "time": "Time",
                        "team1": "Home Team",
                        "team2": "Away Team",
                        "venue": "Venue"
                    }
                )

                # Summary metrics
                
                col1, col2, col3 = st.columns(3)

                with col1:
                    st.metric(
                        label="Scheduled Matches",
                        value=len(schedule_df),
                        delta=None
                    )

                with col2:
                    st.metric(
                        label="Unscheduled Matches",
                        value=selected_result.get("unscheduled_matches", 0),
                        delta=None
                    )

                with col3:
                    st.metric(
                        label="Fitness Score",
                        value=f'{selected_result.get("fitness", 0):.4f}',
                        delta=None
                    )


                st.markdown("---")

                panel_heading(
                    "Generated Fixtures",
                    f"Schedule produced by {selected_algorithm}"
                )

                st.dataframe(
                    display_df,
                    use_container_width=True,
                    hide_index=True
                )

                # Download schedule
                csv_data = display_df.to_csv(index=False).encode("utf-8-sig")

                st.download_button(
                    label="Download Schedule CSV",
                    data=csv_data,
                    file_name=f"{selected_algorithm.replace(' ', '_')}_schedule.csv",
                    mime="text/csv",
                    use_container_width=True
                )



# =====================================================
# ANALYTICS
# =====================================================
elif page == "Analytics":

    page_heading(
        "WORKSPACE / INSIGHTS",
        "Performance Analytics",
        "Understand algorithm behavior and compare scheduling quality."
    )

    optimization_results = st.session_state.get(
        "optimization_results", {}
    )

    # -------------------------------------------------
    # CHECK RESULTS
    # -------------------------------------------------

    if not optimization_results:

        st.info(
            "No optimization results available yet. "
            "Go to Configuration and run the optimization first."
        )

    else:

        # -------------------------------------------------
        # PREPARE REAL RESULTS
        # -------------------------------------------------

        algorithm_colors = {
            "Baseline": "#8496B3",
            "Genetic Algorithm": "#718BFF",
            "Memetic Algorithm": "#42D9AA"
        }

        analytics_rows = []

        for name, result in optimization_results.items():

            analytics_rows.append({
                "Algorithm": name,
                "Fitness": float(result.get("fitness", 0)),
                "Conflicts": int(result.get("conflicts", 0)),
                "Team Conflicts": int(
                    result.get("team_conflicts", 0)
                ),
                "Venue Conflicts": int(
                    result.get("venue_conflicts", 0)
                ),
                "Unscheduled Matches": int(
                    result.get("unscheduled_matches", 0)
                ),
                "Rest Violations": int(
                    result.get("rest_violations", 0)
                ),
                "Balance Violations": int(
                    result.get("balance_violations", 0)
                ),
                "Execution Time": float(
                    result.get("execution_time", 0)
                )
            })

        analytics_df = pd.DataFrame(analytics_rows)

        chart_colors = [
            algorithm_colors.get(name, "#718BFF")
            for name in analytics_df["Algorithm"]
        ]

        # -------------------------------------------------
        # FITNESS & CONFLICTS
        # -------------------------------------------------

        left, right = st.columns(2)

        with left:

            st.markdown(
                '<div class="panel">',
                unsafe_allow_html=True
            )

            panel_heading(
                "Fitness Comparison",
                "Higher is better"
            )

            fig = go.Figure()

            fig.add_trace(go.Bar(
                x=analytics_df["Algorithm"],
                y=analytics_df["Fitness"],
                marker_color=chart_colors,
                text=[
                    f"{value:.4f}"
                    for value in analytics_df["Fitness"]
                ],
                textposition="outside",
                hovertemplate=(
                    "%{x}<br>"
                    "Fitness: %{y:.4f}"
                    "<extra></extra>"
                )
            ))

            max_fitness = max(
                analytics_df["Fitness"].max(),
                0.1
            )

            fig.update_yaxes(
                range=[0, max_fitness * 1.25]
            )

            fig = style_chart(fig, 340)

            st.plotly_chart(
                fig,
                use_container_width=True
            )

            st.markdown('</div>', unsafe_allow_html=True)

        with right:

            st.markdown(
                '<div class="panel">',
                unsafe_allow_html=True
            )

            panel_heading(
                "Conflict Comparison",
                "Lower is better"
            )

            fig2 = go.Figure()

            fig2.add_trace(go.Bar(
                x=analytics_df["Algorithm"],
                y=analytics_df["Conflicts"],
                marker_color=chart_colors,
                text=analytics_df["Conflicts"],
                textposition="outside",
                hovertemplate=(
                    "%{x}<br>"
                    "Conflicts: %{y}"
                    "<extra></extra>"
                )
            ))

            fig2 = style_chart(fig2, 340)

            st.plotly_chart(
                fig2,
                use_container_width=True
            )

            st.markdown('</div>', unsafe_allow_html=True)

        # -------------------------------------------------
        # ALGORITHM BENCHMARK
        # -------------------------------------------------

        st.markdown(
            '<div class="panel">',
            unsafe_allow_html=True
        )

        panel_heading(
            "Algorithm Benchmark",
            "Side-by-side performance comparison"
        )

        benchmark_df = analytics_df[
            [
                "Algorithm",
                "Fitness",
                "Conflicts",
                "Unscheduled Matches",
                "Execution Time"
            ]
        ].copy()

        benchmark_df["Fitness"] = benchmark_df["Fitness"].map(
            lambda x: f"{x:.4f}"
        )

        benchmark_df["Execution Time"] = (
            benchmark_df["Execution Time"].map(
                lambda x: f"{x:.4f} s"
            )
        )

        st.dataframe(
            benchmark_df,
            use_container_width=True,
            hide_index=True
        )

        st.markdown('</div>', unsafe_allow_html=True)

        # -------------------------------------------------
        # FITNESS DISTRIBUTION
        # -------------------------------------------------

        st.markdown(
            '<div class="panel">',
            unsafe_allow_html=True
        )

        panel_heading(
            "Fitness Distribution",
            "Fitness score across the available algorithms"
        )

        fig3 = go.Figure()

        fig3.add_trace(go.Scatter(
            x=analytics_df["Algorithm"],
            y=analytics_df["Fitness"],
            mode="lines+markers+text",
            line=dict(
                color="#718BFF",
                width=3
            ),
            marker=dict(
                size=12,
                color="#42D9AA",
                line=dict(
                    width=2,
                    color="#EAF0FF"
                )
            ),
            text=[
                f"{value:.4f}"
                for value in analytics_df["Fitness"]
            ],
            textposition="top center",
            fill="tozeroy",
            fillcolor="rgba(113,139,255,.10)",
            hovertemplate=(
                "%{x}<br>"
                "Fitness: %{y:.4f}"
                "<extra></extra>"
            )
        ))

        max_fitness = max(
            analytics_df["Fitness"].max(),
            0.1
        )

        fig3.update_yaxes(
            range=[0, max_fitness * 1.25]
        )

        fig3 = style_chart(fig3, 300)

        st.plotly_chart(
            fig3,
            use_container_width=True
        )

        st.markdown('</div>', unsafe_allow_html=True)

        # -------------------------------------------------
        # DETAILED CONSTRAINT METRICS
        # -------------------------------------------------

        st.markdown(
            '<div class="panel">',
            unsafe_allow_html=True
        )

        panel_heading(
            "Constraint Analysis",
            "Detailed scheduling violations"
        )

        # Show which scheduling rules were active for this run

        applied_constraints = st.session_state.get(
            "constraints_applied"
        )

        if applied_constraints:

            applied_labels = [
                f"Minimum rest period ({st.session_state.get('min_rest_hours', 48)}h)"
                if key == "rest"
                else "Avoid venue conflicts"
                if key == "venue"
                else "Avoid team conflicts"
                if key == "team"
                else "Balance number of games"
                for key, enabled in applied_constraints.items()
                if enabled
            ]

            if applied_labels:
                st.caption(
                    "Active rules: " + " | ".join(applied_labels)
                )
            else:
                st.caption(
                    "All scheduling rules were disabled for this run."
                )

        constraint_df = analytics_df[
            [
                "Algorithm",
                "Team Conflicts",
                "Venue Conflicts",
                "Rest Violations",
                "Balance Violations"
            ]
        ]

        st.dataframe(
            constraint_df,
            use_container_width=True,
            hide_index=True
        )

        # Violation details per algorithm (rest period and balance)

        for name, result in optimization_results.items():

            rest_details = result.get("rest_details", [])
            balance_details = result.get("balance_details", [])

            if not rest_details and not balance_details:
                continue

            with st.expander(
                f"Violation details · {name}",
                expanded=False
            ):

                for detail in rest_details:
                    st.markdown(
                        f"<div style='font-size:12px;color:#F0A9A9;'>"
                        f"Rest period: {detail}</div>",
                        unsafe_allow_html=True
                    )

                for detail in balance_details:
                    st.markdown(
                        f"<div style='font-size:12px;color:#F0D9A0;'>"
                        f"Balance: {detail}</div>",
                        unsafe_allow_html=True
                    )

        st.markdown('</div>', unsafe_allow_html=True)


# =====================================================
# FOOTER
# =====================================================
st.markdown("""
<div style="text-align:center;padding:30px 0 5px;color:#647590;
            font-size:10px;letter-spacing:1.5px;">
    SPORTS TOURNAMENT SCHEDULER · SMART TOURNAMENT SCHEDULING
</div>
""", unsafe_allow_html=True)
