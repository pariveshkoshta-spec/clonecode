from data_pipeline.loader import load_dummy_dataset
from data_pipeline.ast_parser import get_ast_similarity
from models.embeddings import get_semantic_similarity
from models.llm_client import query_llm
from models.hybrid_classifier import HybridClassifier
from prompts.templates import CLONE_DETECTION_PROMPT
from evaluation.evaluator import evaluate_model
import time

def main():
    print("Loading dataset...")
    df = load_dummy_dataset()
    
    y_true = df['is_clone'].tolist()
    
    # 1. Feature Extraction for Hybrid Model
    print("Extracting AST and Semantic features...")
    X_features = []
    for _, row in df.iterrows():
        ast_sim = get_ast_similarity(row['code1'], row['code2'])
        sem_sim = get_semantic_similarity(row['code1'], row['code2'])
        X_features.append([ast_sim, sem_sim])
        
    # 2. Train/Test Hybrid Model
    print("Evaluating Hybrid Model...")
    classifier = HybridClassifier()
    classifier.train(X_features, y_true) 
    y_pred_hybrid = [classifier.predict(f) for f in X_features]
    evaluate_model(y_true, y_pred_hybrid, "Hybrid Model (AST + MiniLM)")
    
    # 3. Evaluate Small Model (Allam 7B) via Groq
    print("\nEvaluating allam-2-7b (via Groq)...")
    y_pred_llama = []
    for _, row in df.iterrows():
        prompt = CLONE_DETECTION_PROMPT.format(code1=row['code1'], code2=row['code2'])
        pred = query_llm(prompt, "allam-2-7b")
        y_pred_llama.append(pred)
        time.sleep(2.5) # Simple rate limiting
    evaluate_model(y_true, y_pred_llama, "Allam 2 7B Baseline")

    # 4. Evaluate Medium Model (Qwen 3.8 27B) via Groq
    print("\nEvaluating qwen/qwen3.8-27b (via Groq)...")
    y_pred_gemma = []
    for _, row in df.iterrows():
        prompt = CLONE_DETECTION_PROMPT.format(code1=row['code1'], code2=row['code2'])
        pred = query_llm(prompt, "qwen/qwen3.8-27b")
        y_pred_gemma.append(pred)
        time.sleep(2.5) # Simple rate limiting
    evaluate_model(y_true, y_pred_gemma, "Qwen 3.8 27B Baseline")

    # 5. Evaluate Groq Compound Model via Groq
    print("\nEvaluating groq/compound (via Groq)...")
    y_pred_mixtral = []
    for _, row in df.iterrows():
        prompt = CLONE_DETECTION_PROMPT.format(code1=row['code1'], code2=row['code2'])
        pred = query_llm(prompt, "groq/compound")
        y_pred_mixtral.append(pred)
        time.sleep(2.5)
    evaluate_model(y_true, y_pred_mixtral, "Groq Compound Baseline")

if __name__ == "__main__":
    main()
