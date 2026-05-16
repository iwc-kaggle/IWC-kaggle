# 📚 UniLibrary Match: Intelligent Book Recommender System

### 👥 Team Profile
* **Team Name:** IWC
* **Team Components:** Riccardo Cerimele & Janina Spielkamp
* **Project Video Presentation:** [Insert Link to Your Movie Trailer Video Here]

---

## 📁 Repository Contents

This repository contains all the essential files needed to run, evaluate, and interact with our university library recommendation engine:

* **`IWC_1689_CrossVal.ipynb`**: The master Colab Notebook containing the 5-fold cross-validation engine and the production code used to generate our top submission.
* **`app.py`**: The clean, web-based user interface built with Streamlit.
* **`recommendations.csv`** *(generated as `submission_adaptive_hybrid.csv`)*: Our highest-scoring output file containing the top-10 tailored book recommendations for every user. This strategy achieved a benchmark score of **0.1689** on the Kaggle competition leaderboard.
* **`items.csv` & `interactions_train.csv`**: The foundational university datasets containing book metadata (titles, authors, subjects) and student borrowing histories.

---

## 🛠️ Instructions to Open the User Interface (UI)

Since GitHub Codespaces pre-installs the necessary core libraries, you can launch the application directly using the following steps:

1. **Open the Project:** Access the repository inside your GitHub Codespace environment.
2. **Open the Terminal:** Locate the terminal panel at the bottom of the workspace screen.
3. **Run the Interface:** Type the following command into the terminal and press **Enter**:
   ```bash
   python3 -m streamlit run app.py
   ```
4. **View in Browser:**
   * A pop-up notification will appear in the bottom-right corner stating *"Your application is running on port 8501."* Click the **"Open in Browser"** button.
   * Alternatively, navigate to the **Ports** tab next to the terminal panel, hover over port `8501`, and click the **Globe Icon** (Open in Browser).

---

## 📈 Exploratory Data Analysis (EDA) & Conclusions

Our final submission strategy was built entirely on two crucial insights discovered during our exploratory data analysis:

* **The Re-Read Phenomenon (54% Threshold):** We discovered that **54% of all interactions in the training data represent repeat checkouts**—meaning students frequently borrow books they have already read in the past. In an academic environment, students continuously return to the same core reference materials, textbooks, and program guides.
* **The Sparsity Bottleneck:** The dataset reflects a sharp long-tail distribution where a vast majority of new or casual library users have 5 or fewer total book rentals. Pure collaborative filtering techniques fail on these users because there isn't enough overlapping history to find a match.

---

## 🧠 Algorithmic Logic: Our Winning Strategy

To clear the baseline target of 0.1452 and secure our peak leaderboard score of **0.1689**, we developed an **Adaptive Segmented Hybrid** architecture. The entire data processing workflow executes down the following pipeline:

```text
                  [ Raw Interaction Data ]
                             │
                  ┌──────────┼──────────┐
                  ▼          ▼          ▼
             [User-User] [Item-Item] [TF-IDF Content]
                  │          │          │
                  └──────────┼──────────┘
                             ▼
               [User Profile Segmentation]
               ├── New Users (≤5): Focus on Content/Item Space
               └── Power Users (>5): Focus on Collaborative Space
                             ▼
                [Last-Book Contextual Nudge]
                             ▼
            [Historical Re-Read Multiplier (2.0x)]
                             ▼
                [Log-Scale Popularity Boost]
                             ▼
                   [Final Top-10 Rankings]
```

1. **Temporal Decay Weighting:** Recent checkouts are scaled higher than older interactions using a linear time formula, ensuring the system prioritizes a student's current semester needs without losing their long-term interests.
2. **Profile Segmentation (New vs. Power Users):**
   * **New Users (<= 5 books read):** The system relies heavily on Content-Based TF-IDF matching (50%) built from author and subject metadata alongside Item-Item patterns (30%) to overcome the cold-start problem.
   * **Power Users (> 5 books read):** The system shifts priorities toward User-User (45%) and Item-Item (40%) collaborative pipelines to uncover deeper behavioral relationships.
3. **The "Last-Book" Series Nudge:** The algorithm isolates the absolute last book a student checked out and applies an immediate boost to items sharing a high item-item similarity score. This successfully captures next-in-series sequences or direct research continuations.
4. **Historical Multiplier (The Re-Read Booster):** To exploit our 54% re-read EDA finding, any book already sitting in a user's historical interaction vector receives a massive **2.0x weight multiplier**, guaranteeing that essential recurring study materials remain easily retrievable.
5. **Log-Scale Popularity Scaling:** A global, log-scaled popularity boost is applied at the end to gently favor generally popular books across the entire university network, filling in any gaps for low-activity accounts.

---
## 📊 Cross-Validation Performance Metrics

The table below presents the performance metrics evaluated using an explicit 5-Fold Cross-Validation split on our training data, directly validating our hybrid approach against standalone baselines:

| Metric | user-user CF | item-item CF | Any other technique (Our Adaptive Hybrid) |
| :--- | :---: | :---: | :---: |
| **Precision@10** | 0.0664 | 0.0638 | **0.0708** |
| **Recall@10** | 0.3079 | 0.2778 | **0.3137** |

*Note on Validation Evaluation:* While local cross-validation intentionally isolates random subsets of data to test retrieval metrics under strict constraints, our unified pipeline scales optimally on unobserved data, achieving our top performance score of **0.1689** on the live Kaggle leaderboard.

---
## 💻 User Interface Functionalities

The **UniLibrary Match** front-end application translates our data engineering models into a premium, comprehensive ecosystem designed for modern scholars. The interactive dashboard includes the following active chapters:

* **Personalized Recommendations:** Displays the core top-10 hybrid recommendations engine shelf dynamically adapted to the student's profile segment.
* **Favorite Authors & Subjects:** An intuitive profile tracking utility that shows your primary academic domain focuses, favorite writers, and recurring study subjects.
* **Most Popular Shelf:** Aggregates network-wide metadata to showcase what books are currently trending across the campus library community.
* **Search Catalog:** An active search field allowing readers to instantly filter, query, and lookup titles inside the global item dataset.
* **The Academic Book Club:** Connects students sharing a similar "reading DNA." This feature visualizes the exact reading paths and checkout histories of peers with overlapping research needs to provide community validation.
* **Challenge of the Month & Reading Tracker:** A productivity module designed to keep students engaged (e.g., a monthly milestone target of 180 total reading minutes). It includes a functional logging tool where users can save explicit telemetry data (e.g., *"Logged 30 minutes of reading Book X on Day Y"*).
* **Scholar Leaderboard:** A monthly scoreboard highlighting the top-performing readers and most active students inside the university database.
* **Detailed Book Insights & Similar Titles:** Clicking any title unfolds comprehensive textbook descriptions, categorical metadata fields, and an automated list of contextually related lookalikes.

---



## 🎯 Conclusion

By shifting our paradigm away from a single model and embracing an **Adaptive Segmented Hybrid** architecture, our engine successfully mitigates data sparsity for new scholars while unlocking personalized predictive pathways for power users. Backed by temporal weighting, explicit re-read boosting, and next-in-series logic, **UniLibrary Match** transforms a massive catalog of obscure titles into an active, highly organized academic ecosystem that saves time, builds confidence, and connects readers with shared academic needs.
