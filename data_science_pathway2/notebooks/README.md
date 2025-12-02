# Data Science Pathway 2 – Notebooks

This folder contains the recommended Jupyter notebooks for **Data Science Pathway 2 (Intermediate ML)**. They mirror the structure of Pathway 1 and align with the Streamlit content in `data_science_pathway2_module.py`.

## Notebook list

- `U1_feature_pipelines.ipynb`
- `U2_regression_models.ipynb`
- `U3_classification_metrics.ipynb`
- `U4_model_validation.ipynb`
- `U5_clustering_segmentation.ipynb`
- `U6_deployment_basics.ipynb`
- `U7_capstone_template.ipynb`

## Unit 1 – Feature Engineering & Data Pipelines

**File:** `U1_feature_pipelines.ipynb`

Focus:
- Turn messy tables into clean, reusable feature pipelines.
- Demonstrate data leakage and how to avoid it.

Suggested sections:
- Setup and imports; load `../data/unit1_events.csv`.
- Data understanding (head/info, missingness, column types).
- Baseline "manual" cleaning and simple model.
- Proper `ColumnTransformer` + `Pipeline` for preprocessing.
- Leakage example (fitting transforms on full data before split).
- Save fitted pipeline with `joblib` to `../artifacts/u1_feature_pipeline.joblib`.

## Unit 2 – Supervised Learning: Regression

**File:** `U2_regression_models.ipynb`

Focus:
- Linear regression, Ridge, Lasso.
- Regression metrics and interpretation.

Suggested sections:
- Setup; load `../data/unit2_regression_features.csv` (or reuse Unit 1 features).
- Baseline `LinearRegression` with RMSE/MAE/R².
- Ridge and Lasso across several `alpha` values.
- Compare metrics and inspect coefficients.

## Unit 3 – Supervised Learning: Classification

**File:** `U3_classification_metrics.ipynb`

Focus:
- Binary classification.
- Accuracy vs precision/recall/F1, ROC-AUC, PR-AUC.

Suggested sections:
- Setup; load `../data/unit3_classification_features.csv`.
- Baseline logistic regression classifier; confusion matrix.
- Imbalance demonstration (majority-class accuracy vs recall).
- Threshold tuning using predicted probabilities.
- ROC and precision–recall curves.

## Unit 4 – Model Evaluation & Validation

**File:** `U4_model_validation.ipynb`

Focus:
- Generalisation.
- Cross-validation and time-aware validation.

Suggested sections:
- Setup; reuse regression or classification dataset.
- Train/validation/test split; train vs validation vs test metrics.
- k-fold cross-validation with `cross_val_score`.
- Time-series style split (if dates available); show why random shuffling is wrong.
- Example of overfitting by reusing the test set for tuning (what *not* to do).

## Unit 5 – Unsupervised Learning & Segmentation

**File:** `U5_clustering_segmentation.ipynb`

Focus:
- Clustering, scaling and segment interpretation.

Suggested sections:
- Setup; load `../data/unit5_segmentation_features.csv`.
- Scale features and explore distributions.
- k-means for several values of k; inertia and silhouette scores.
- Add cluster labels back to the data and profile segments.
- Brief business narrative describing how segments would be used.

## Unit 6 – Deploying & Operationalising Models

**File:** `U6_deployment_basics.ipynb`

Focus:
- Saving/loading pipelines.
- Batch scoring and simple app patterns.

Suggested sections:
- Load a trained pipeline from earlier units with `joblib.load`.
- Implement a `score_file(input_path, output_path)` helper.
- Example of a CLI call (`python score.py --in data.csv --out preds.csv`).
- Simple Streamlit/CLI-style interface stub for predictions.
- Sketch basic monitoring checks (data drift, metric tracking).

## Unit 7 – Capstone Project Template

**File:** `U7_capstone_template.ipynb`

Focus:
- Provide a structured template that matches the Unit 7 capstone brief.

Suggested sections (mostly markdown with TODO cells):
- Title & Problem statement.
- Context & stakeholders.
- Data understanding & EDA.
- Feature engineering & pipelines.
- Modelling (baseline + improved).
- Evaluation & validation.
- (Optional) Segmentation / unsupervised analysis.
- Deployment & monitoring plan.
- Conclusions, limitations, next steps.

## Datasets (suggested locations)

Create small, realistic CSVs under:

- `data_science_pathway2/data/unit1_events.csv`
- `data_science_pathway2/data/unit2_regression_features.csv`
- `data_science_pathway2/data/unit3_classification_features.csv`
- `data_science_pathway2/data/unit5_segmentation_features.csv`

You can reuse the same base dataset for several units (e.g. customer/patient events) with different targets or feature subsets.
