import streamlit as st
import requests
import pandas as pd

# -----------------------------
# CONFIG
# -----------------------------
st.set_page_config(
    page_title="Rural Connect: An Intelligent Telemedicine Access System",
    page_icon="🩺",
    layout="wide"
)

BACKEND_URL = "http://127.0.0.1:8000"

# -----------------------------
# STYLING
# -----------------------------
st.markdown("""
<style>
.main {
    background-color: #FFFAF0;
}
.big-title {
    font-size: 2.2rem;
    font-weight: 700;
    color: 	#FFFAF0;
}
.sub-text {
    color: #475569;
    font-size: 1rem;
}
.card {
    background: white;
    padding: 18px;
    border-radius: 16px;
    border: 1px solid #e2e8f0;
    box-shadow: 0 2px 8px rgba(0,0,0,0.04);
    margin-bottom: 16px;
}
.card-title {
    font-size: 1.25rem;
    font-weight: 700;
    color: #0f172a;
}
.tag {
    display: inline-block;
    padding: 4px 10px;
    border-radius: 999px;
    background: #e0f2fe;
    color: #0369a1;
    font-size: 0.8rem;
    margin-right: 6px;
    margin-top: 6px;
}
.emergency {
    display: inline-block;
    padding: 4px 10px;
    border-radius: 999px;
    background: #fee2e2;
    color: #b91c1c;
    font-size: 0.8rem;
    font-weight: 600;
}
.normal {
    display: inline-block;
    padding: 4px 10px;
    border-radius: 999px;
    background: #dcfce7;
    color: #166534;
    font-size: 0.8rem;
    font-weight: 600;
}
.footer-note {
    color: #64748b;
    font-size: 0.9rem;
    margin-top: 24px;
}
</style>
""", unsafe_allow_html=True)

# -----------------------------
# HEADER
# -----------------------------
st.markdown('<div class="big-title">🩺 Rural Connect -An Intelligent Telemedicine Access System</div>', unsafe_allow_html=True)
st.markdown(
    '<div class="sub-text">Find specialized doctors based on disease, location, and language for faster emergency access in rural and urban areas.</div>',
    unsafe_allow_html=True
)

st.divider()

# -----------------------------
# SIDEBAR
# -----------------------------
st.sidebar.header("⚙️ Search Filters")

problem = st.sidebar.text_input("Enter disease / condition", placeholder="e.g. cardiac arrest, fever, fracture")
location = st.sidebar.text_input("Enter city / region", placeholder="e.g. Chennai, Thoothukudi")
language = st.sidebar.selectbox("Preferred doctor language", ["", "Tamil", "English", "Hindi", "Telugu", "Malayalam"])
top_k = st.sidebar.slider("Number of recommendations", min_value=1, max_value=20, value=5)

search_btn = st.sidebar.button("🔍 Find Doctors", use_container_width=True)

# -----------------------------
# HEALTH CHECK
# -----------------------------
def check_backend():
    try:
        response = requests.get(f"{BACKEND_URL}/", timeout=5)
        return response.status_code == 200
    except:
        return False

backend_ok = check_backend()

if backend_ok:
    st.success("✅ Backend connected successfully")
else:
    st.error("❌ Backend not reachable. Make sure FastAPI is running at http://127.0.0.1:8000")
    st.stop()

# -----------------------------
# API CALL
# -----------------------------
def search_doctors(problem, location, language, top_k):
    payload = {
        "symptoms": problem,
        "city": location,
        "language": language,
        "top_k": top_k
    }

    try:
        response = requests.post(f"{BACKEND_URL}/recommend", json=payload, timeout=15)

        if response.status_code == 200:
            return response.json()
        else:
            st.error(f"Backend Error: {response.status_code}")
            st.code(response.text)
            return None

    except requests.exceptions.ConnectionError:
        st.error("❌ Could not connect to backend.")
        return None
    except requests.exceptions.Timeout:
        st.error("⏳ Backend request timed out.")
        return None
    except Exception as e:
        st.error(f"Request failed: {e}")
        return None

# -----------------------------
# INTRO
# -----------------------------
if not search_btn:
    col1, col2 = st.columns([2, 1])

    with col1:
        st.info("""
### How this system helps
- Finds the right specialist for a disease or emergency
- Filters doctors by city and language
- Supports rural and urban telemedicine access
- Gives phone number, booking link, and video consultation link
- Useful in urgent care situations
        """)

        st.markdown("### Example Searches")
        st.markdown("""
- `cardiac arrest` in `Chennai` with `Tamil`
- `stroke` in `Thoothukudi` with `English`
- `diabetes symptoms` in `Chennai` with `Tamil`
        """)

    with col2:
        st.metric("Use Case", "Rural + Urban")
        st.metric("Language Support", "Multi-language")
        st.metric("Mode", "Emergency Ready")

# -----------------------------
# SEARCH
# -----------------------------
if search_btn:
    if not problem.strip():
        st.warning("Please enter a disease / condition.")
    elif not location.strip():
        st.warning("Please enter a city / region.")
    else:
        with st.spinner("Finding the best doctors..."):
            result = search_doctors(problem, location, language, top_k)

        if result is None:
            st.stop()

        # Handle flexible backend response
        if isinstance(result, dict):
            doctors = result.get("recommendations", result.get("results", result.get("doctors", [])))
        elif isinstance(result, list):
            doctors = result
        else:
            doctors = []

        st.subheader(f"Search Results ({len(doctors)} doctor(s) found)")

        if len(doctors) == 0:
            st.warning("No matching doctors found. Try another city or broader search.")
        else:
            st.markdown(f"""
### Search Summary
- Condition: `{problem}`
- City: `{location}`
- Language: `{language if language else 'Any'}`
- Requested Results: `{top_k}`
            """)

            st.divider()

            for idx, doctor in enumerate(doctors, start=1):
                doctor_name = doctor.get("doctor_name", "N/A")
                specialty = doctor.get("specialty", doctor.get("mapped_specialist", "N/A"))
                subspecialty = doctor.get("subspecialty", "N/A")
                hospital = doctor.get("hospital_name", "N/A")
                city = doctor.get("city", "N/A")
                area = doctor.get("area", "N/A")
                languages = doctor.get("languages_spoken", "N/A")
                phone = doctor.get("phone_number", "N/A")
                consultation_mode = doctor.get("consultation_mode", "N/A")
                booking_link = doctor.get("booking_link", "")
                video_link = doctor.get("video_consult_link", "")
                emergency = str(doctor.get("emergency_supported", "No")).strip().lower() == "yes"
                rating = doctor.get("rating", "N/A")
                score = doctor.get("score", None)

                emergency_badge = (
                    '<span class="emergency">Emergency Supported</span>'
                    if emergency
                    else '<span class="normal">Standard Consultation</span>'
                )

                score_html = f'<span class="tag">Match Score: {round(score, 3)}</span>' if score is not None else ''

                st.markdown(f"""
<div class="card">
    <div class="card-title">{idx}. {doctor_name}</div>
    <div style="margin-top:8px;">{emergency_badge}</div>
    <div style="margin-top:12px;">
        <span class="tag">{specialty}</span>
        <span class="tag">{subspecialty}</span>
        <span class="tag">{hospital}</span>
        <span class="tag">{city} - {area}</span>
        <span class="tag">{languages}</span>
        <span class="tag">Mode: {consultation_mode}</span>
        <span class="tag">Rating: {rating}</span>
        {score_html}
    </div>
</div>
                """, unsafe_allow_html=True)

                c1, c2, c3 = st.columns([1.2, 1.2, 2])

                with c1:
                    st.write(f"Phone: {phone}")

                with c2:
                    if phone and phone != "N/A":
                        st.markdown(f"[Call Doctor](tel:{phone})")

                with c3:
                    if video_link and str(video_link).strip():
                        st.markdown(f"[Start Video Consultation]({video_link})")
                    elif booking_link and str(booking_link).strip():
                        st.markdown(f"[Book Appointment]({booking_link})")
                    else:
                        st.write("No booking/video link available")

                st.divider()

            with st.expander("View results in table format"):
                df = pd.DataFrame(doctors)
                st.dataframe(df, use_container_width=True)

# -----------------------------
# FOOTER
# -----------------------------
st.markdown(
    '<div class="footer-note">Built for accessible specialist discovery in emergencies and rural telemedicine scenarios.</div>',
    unsafe_allow_html=True
)