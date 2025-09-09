import streamlit as st

# Example job cards
jobs = [
    {"title": "Senior UI/UX Designer", "company": "Amazon", "salary": "$250/hr", "location": "San Francisco, CA"},
    {"title": "Junior UI/UX Designer", "company": "Google", "salary": "$150/hr", "location": "California, CA"},
]

st.title("Recommended Jobs")

cols = st.columns(2)
for i, job in enumerate(jobs):
    with cols[i % 2]:
        st.markdown(
            f"""
            <div style="
                background-color: #f9f9f9;
                border-radius: 15px;
                padding: 20px;
                margin-bottom: 20px;
                box-shadow: 0 4px 8px rgba(0,0,0,0.1);
            ">
                <h4>{job['title']}</h4>
                <p><b>{job['company']}</b></p>
                <p>{job['salary']} | {job['location']}</p>
                <button style="padding: 6px 12px; border:none; border-radius:8px; background:#4CAF50; color:white; cursor:pointer;">
                    Details
                </button>
            </div>
            """,
            unsafe_allow_html=True
        )
