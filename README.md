# 📚 IWC Recommender System: Final Project Report

## 👥 Team Information
* **Team Members:** Riccardo Cerimele & Janina Spielkamp
* **Kaggle Competition:** IWC Recommender System
* **Final Public Score:** **0.1649** (Author-Heavy Hybrid)

---

## 1. Executive Summary
This project involved the development of a high-performance recommendation engine for a library dataset. Our final model uses a **Weighted Triple Hybrid** architecture that integrates collaborative filtering and content-based analysis. By refining our feature engineering to prioritize author-based loyalty, we achieved a peak precision@10 of 0.1649.

---

## 2. Model Architecture
Our "Triple Hybrid" system combines three distinct recommendation "brains," each assigned a specific voting weight based on validation performance:

### 🧠 Brain A: User-User Collaborative Filtering (45% Weight)
* **Methodology:** Cosine Similarity on the user-item interaction matrix.
* **Function:** Identifies users with overlapping reading histories. It excels at surfacing community-wide trends (e.g., "Readers who liked Italian Classics also liked...").

### 🧠 Brain B: Item-Item Collaborative Filtering (35% Weight)
* **Methodology:** Item-to-Item similarity mapping.
* **Function:** Focuses on the books themselves. This provides a "consistency" signal, recommending books that are statistically linked to the user's specific history, regardless of current trends.

### 🧠 Brain C: Author-Heavy Content Filtering (20% Weight)
* **Methodology:** TF-IDF Vectorization of Metadata.
* **Optimization:** We discovered that Authors are more predictive of future reads than Subjects. To implement this, we **doubled the frequency of the Author field** in the metadata string to ensure the algorithm prioritized the writer's style over the book's general category.

---

## 3. Methodology & Experimentation
We treated this project as a series of controlled experiments, using a local validation set to justify every change.

### Validation Strategy
We implemented a **Temporal Split** to simulate real-world conditions. We used the first 80% of interactions (sorted by time) for training and the remaining 20% for testing. This prevented "data leakage" and ensured the model could predict future behavior.

### Feature Importance Analysis
Before building the hybrid, we tested individual features to see which carried the strongest "signal":
* **Author-only Precision:** 0.0303
* **Subject-only Precision:** 0.0225
* **Insight:** Users follow authors more strictly than they follow subjects. This led to our "Author-Heavy" refinement.

### Experiment Log (Precision@10 Results)
| Model / Experiment | Precision@10 | Description |
| :--- | :--- | :--- |
| **Baseline (TF-IDF - Authors + Subjects)** | 0.0224 | Initial content-based attempt. |
| **Authors weighted 2x** | **0.0303** | **Key Insight:** Authors are the strongest metadata signal. |
| **Subjects weighted 2x** | 0.0225 | Marginal improvement over baseline. |
| **User-User Only** | 0.1630 | Strongest single-model collaborative signal. |
| **Item-Item Only** | 0.1587 | Reliable but less precise than user-based. |
| **Hybrid (User-User + Item-Item)** | 0.1642 | First significant breakthrough. |
| **Triple Hybrid (U-U + I-I + Content)** | 0.1648 | Adding metadata refined the top-tier rankings. |
| **Author-Heavy Hybrid (+10% Pop)** | **0.1649** | **Final Winning Model.** |

---

## 4. Popularity Amplification
To reach our final score, we applied a **10% Global Popularity Boost**. Using a logarithmic scale (log1p), we nudged books that were trending library-wide. This served as an effective "tie-breaker" when our similarity models calculated multiple books as being equally relevant.

---

## 5. Conclusion
The 0.1649 plateau was broken by shifting our focus from broad "Subjects" to specific "Authors." While collaborative filtering provided the foundation (80% total weight), the content-based refinement was the crucial element that provided the final precision boost.

---

## 🛠️ How to Reproduce
1.  Open the repository notebook: `Final_IWC.ipynb`.
2.  Run all cells to execute the **Validation Phase** and **Production Phase**.
3.  The final submission file will be generated as **`final_project_submission.csv`**.
