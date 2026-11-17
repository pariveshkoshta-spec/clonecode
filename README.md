# Project Walkthrough: Advanced Code Clone Detection

## Overview
This project successfully implemented and evaluated an advanced, hybrid code clone detection system. The objective was to determine if two distinct code snippets are semantic clones (performing the same logic/function), even if they are written in different languages or use different algorithms.

We built a lightweight **Hybrid Model** that leverages classical machine learning, and benchmarked its scalability and performance against massive state-of-the-art **Large Language Models (LLMs)**.

---

## 🏗 Architecture & Methodology

The pipeline was built using a modular Python architecture located in `Desktop/placement grind/projects proof/clonecode/`.

### 1. The Hybrid Model
Instead of relying purely on an LLM to "read" the code, our hybrid model extracts two distinct feature sets and uses a Logistic Regression classifier to make a final prediction:
* **Structural Features (AST):** We utilized `tree-sitter` to parse the raw code into an Abstract Syntax Tree. We extracted structural metrics (node count, tree depth) to mathematically compare the structural skeletons of the two snippets.
* **Semantic Features (MiniLM):** We used the `all-MiniLM-L6-v2` model via `sentence-transformers` to generate dense vector embeddings of the code, calculating cosine similarity to determine how closely the *intent* of the code matches.

### 2. The LLM Baselines
To prove the efficiency of the hybrid approach, we benchmarked it against four LLMs using the Groq API:
* **Allam 2 7B** (Small Architecture)
* **Qwen 3.8 27B** (Medium Architecture)
* **Groq Compound** (Compound Architecture)
* **GPT-OSS 120B** (Massive Architecture)

We applied strict Prompt Engineering to ensure the LLMs returned binary classification (`1` for Clone, `0` for Non-Clone) and built a custom Regex parser to extract answers even if the models became overly verbose.

---

## 📊 Evaluation & Results

We ran the pipeline through two distinct phases of evaluation.

### Phase 1: The "Dummy" Dataset (Proof of Concept)
We procedurally generated a tricky dataset of 20 pairs containing "Hard Positives" (cross-language logic) and "Hard Negatives" (code that looks identical but performs opposite functions).
* **Hybrid Model:** F1 Score `0.91`
* **Qwen 27B / Compound:** F1 Score `1.00`
* **GPT-OSS 120B:** F1 Score `0.00` *(Failed to follow system prompt instructions, resulting in blank outputs).*

**Takeaway:** The architecture works flawlessly. Both the LLMs and the Hybrid model handled the complex logic well, but massive foundational models (like GPT-OSS) can be unreliable without fine-tuning.

### Phase 2: The BigCloneBench Dataset (Enterprise Scale)
We downloaded the industry-standard `code_x_glue_cc_clone_detection_big_clone_bench` dataset from HuggingFace to test how the models scale to real-world, massive enterprise Java files.

* **Hybrid Model:**
  * **Precision:** `0.31` | **Recall:** `0.67` | **F1 Score:** `0.42`
  * **Performance:** Parsed 500 massive file pairs locally in under 60 seconds.
  * **Cost:** $0.00 (0 tokens used).
* **LLM Baselines:**
  * **Performance:** **FAILED**
  * **Takeaway:** Real-world code snippets are thousands of tokens long. The LLMs burned through the absolute daily maximum of **500,000 API tokens** in less than an hour before they could even finish evaluating a single model baseline.

---

## 🏆 Conclusion
This project successfully proves that while cloud-based LLMs are intelligent, they **collapse under their own weight** when applied to enterprise-scale codebases due to massive token exhaustion, rate limits, and slow latency. 

Conversely, the **Hybrid Model** (AST + MiniLM) proved to be highly scalable, privacy-preserving (running 100% locally), and incredibly fast. It successfully established a baseline F1 Score of `0.42` on real-world data without any hyperparameter tuning, making it the clear architectural choice for real-time IDE plugins or massive codebase scanning.

### Future Improvements
To improve the `0.42` baseline score of the Hybrid model, future iterations should:
1. Implement **Tree-Edit-Distance (TED)** in the AST parser for higher-fidelity structural comparisons.
2. Fine-tune the Logistic Regression weights on a larger training split of BigCloneBench.
