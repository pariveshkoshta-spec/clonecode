# Code Clone Detection: Performance Metrics

This document outlines the raw evaluation metrics for the Hybrid Model (AST + MiniLM) compared to the LLM baselines.

---

## 1. Initial Prototype Evaluation (20 Procedurally Generated Pairs)
*This dataset included edge cases like cross-language clones and deceptive non-clones.*

| Model Architecture | Model Name | Precision | Recall | F1-Score | Status |
| :--- | :--- | :---: | :---: | :---: | :--- |
| **Hybrid (AST + MiniLM)** | `Custom Logistic Regression` | 0.83 | 1.00 | **0.91** | ✅ Success |
| **Medium LLM** | `Qwen 3.8 27B` | 1.00 | 1.00 | **1.00** | ✅ Success |
| **Compound LLM** | `Groq Compound` | 1.00 | 1.00 | **1.00** | ✅ Success |
| **Small LLM** | `Allam 2 7B` | 0.71 | 1.00 | **0.83** | ✅ Success |
| **Massive LLM** | `GPT-OSS 120B` | 0.00 | 0.00 | **0.00** | ❌ Failed (Zero-shot Output Format) |

---

## 2. Enterprise Scale Evaluation (500 BigCloneBench Pairs)
*This dataset was sourced directly from HuggingFace to test scalability against massive, real-world enterprise Java files.*

| Model Architecture | Model Name | Precision | Recall | F1-Score | Status |
| :--- | :--- | :---: | :---: | :---: | :--- |
| **Hybrid (AST + MiniLM)** | `Custom Logistic Regression` | 0.31 | 0.67 | **0.42** | ✅ Success (< 60s runtime) |
| **Small LLM** | `Allam 2 7B` | N/A | N/A | **N/A** | ❌ Failed (Token Exhaustion) |
| **Medium LLM** | `Qwen 3.8 27B` | N/A | N/A | **N/A** | ❌ Failed (Token Exhaustion) |
| **Compound LLM** | `Groq Compound` | N/A | N/A | **N/A** | ❌ Failed (Token Exhaustion) |

---

## Metric Definitions
* **Precision:** Out of all the pairs the model *claimed* were clones, what percentage were *actually* clones? (High precision means very few false alarms).
* **Recall:** Out of all the *actual* clones that existed in the dataset, what percentage did the model successfully find? (High recall means it rarely misses a clone).
* **F1-Score:** The harmonic mean of Precision and Recall. This is the ultimate "overall performance" grade for the model.
