import streamlit as st
from orchestrator import run_pipeline
from llm_engine import generate_summary
from report.pdf_report_generator import generate_pdf_report
from report.visual_charts import plot_blood_parameters

# ---------- PAGE CONFIG ----------
st.set_page_config(
    page_title="AI Health Diagnostics",
    page_icon="🧬",
    layout="wide"
)

# ---------- HEADER ----------
st.image("assets/banner.png", use_container_width=True)

st.markdown(
    """
    <h1 style="text-align:center; color:#1F618D;">
        🧬 AI-Based Automated Health Diagnostic System
    </h1>
    <p style="text-align:center; font-size:18px; color:#566573;">
        Multi-Model AI • Pattern Recognition • Risk Assessment • Smart Recommendations
    </p>
    <hr>
    """,
    unsafe_allow_html=True
)

# ---------- SIDEBAR ----------
st.sidebar.image("assets/doctor.png", width=150)
st.sidebar.header("👤 Patient Information")

age = st.sidebar.number_input("Age", min_value=1, max_value=100)
gender = st.sidebar.selectbox("Gender", ["Male", "Female"])

st.sidebar.image("assets/heart.png", width=120)
st.sidebar.info("AI-assisted health insights (educational use only).")

# ---------- MAIN BODY ----------
st.subheader("📄 Blood Report Analysis")
st.image("assets/blood.png", width=120)

uploaded = st.file_uploader(
    "Upload Blood Report (PDF / CSV / JSON)",
    type=["pdf", "csv", "json"]
)

st.markdown("### 🔍 Click below to analyze sample report")

# ---------- ANALYSIS ----------
if st.button("🧠 Analyze Health Report"):
    # SAMPLE DATA (can later be replaced with parser output)
    data = {
        "Hemoglobin": 10.5,
        "RBC": 4.0,
        "WBC": 12000,
        "Glucose": 140,
        "LDL": 160,
        "HDL": 35
    }

    interpretations, patterns, risk, recommendations = run_pipeline(
        data, age, gender
    )

    summary = generate_summary(
        interpretations, patterns, risk, recommendations
    )

    st.markdown("---")

    # ---------- SUMMARY ----------
    st.subheader("🧠 AI Diagnostic Summary")
    st.text_area("Generated Medical Summary", summary, height=300)

    # ---------- RISK ----------
    st.subheader("⚠️ Overall Health Risk")
    if risk == "High Risk":
        st.error(risk)
    elif risk == "Moderate Risk":
        st.warning(risk)
    else:
        st.success(risk)

    # ---------- PATTERNS ----------
    st.subheader("🧩 Detected Health Patterns")
    for p in patterns:
        st.write("✔", p)

    # ---------- RECOMMENDATIONS ----------
    st.subheader("💡 Personalized Recommendations")
    for r in recommendations:
        st.write("👉", r)

    # ---------- GRAPH ----------
    st.markdown("---")
    st.subheader("📊 Blood Parameter Visualization")
    fig = plot_blood_parameters(data)
    st.pyplot(fig)

    # ---------- PDF ----------
    st.markdown("---")
    st.subheader("📥 Download Medical Report")
    pdf_file = generate_pdf_report(summary)

    with open(pdf_file, "rb") as f:
        st.download_button(
            label="📄 Download PDF Medical Report",
            data=f,
            file_name="AI_Medical_Report.pdf",
            mime="application/pdf"
        )

# ---------- FOOTER ----------
st.markdown(
    """
    <hr>
    <p style="text-align:center; color:gray;">
        ⚠ Disclaimer: This AI-generated report is for educational purposes only.<br>
        Always consult a certified medical professional.
    </p>
    """,
    unsafe_allow_html=True
)