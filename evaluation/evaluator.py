from sklearn.metrics import precision_score, recall_score, f1_score

def evaluate_model(y_true, y_pred, model_name):
    precision = precision_score(y_true, y_pred, zero_division=0)
    recall = recall_score(y_true, y_pred, zero_division=0)
    f1 = f1_score(y_true, y_pred, zero_division=0)
    
    report = f"\n--- {model_name} Evaluation ---\nPrecision: {precision:.2f}\nRecall:    {recall:.2f}\nF1 Score:  {f1:.2f}\n"
    print(report)
    
    with open("evaluation_report.txt", "a") as f:
        f.write(report)
        
    return {"precision": precision, "recall": recall, "f1": f1}
