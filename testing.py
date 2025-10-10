# import streamlit as st
# import torch
# import torch.nn as nn
# from sentence_transformers import SentenceTransformer

# # ---------------------
# # 1. Load base model + regressor
# # ---------------------
# base_model = SentenceTransformer("sentence-transformers/all-mpnet-base-v2")

# class ATSRegressor(nn.Module):
#     def __init__(self, embedding_dim, hidden_size=256):
#         super().__init__()
#         self.fc = nn.Sequential(
#             nn.Linear(embedding_dim*2, hidden_size),
#             nn.ReLU(),
#             nn.Linear(hidden_size, 1)  # stop here, no extra layer
#         )

#     def forward(self, x):
#         return self.fc(x)



# # Load trained weights
# embedding_dim = base_model.get_sentence_embedding_dimension()
# regressor = ATSRegressor(embedding_dim=embedding_dim)
# regressor.load_state_dict(torch.load("ats_regression_model.pt", map_location="cpu"))
# regressor.eval()


# # ---------------------
# # 2. Streamlit UI
# # ---------------------
# st.title("📄 Resume vs JD ATS Score Predictor")

# resume_text = st.text_area("Paste Resume Text:")
# jd_text = st.text_area("Paste Job Description Text:")

# if st.button("Predict ATS Score"):
#     if resume_text.strip() == "" or jd_text.strip() == "":
#         st.warning("Please enter both Resume and Job Description")
#     else:
#         # Encode texts using MPNet
#         with torch.no_grad():
#             emb1 = base_model.encode(resume_text, convert_to_tensor=True)
#             emb2 = base_model.encode(jd_text, convert_to_tensor=True)
#             x = torch.cat([emb1, emb2]).unsqueeze(0)  # add batch dim

#             score = regressor(x).item()
#             score = max(0, min(score, 100))  # clamp to 0–100


#         # Show score as text
#         st.success(f"Predicted ATS Score: **{score} / 100**")

#         # Show score visually as a progress bar
#         st.progress(int(score))

import torch
print(torch.cuda.is_available()) # This will check for ROCm/CUDA availability
print(torch.cuda.device_count())

