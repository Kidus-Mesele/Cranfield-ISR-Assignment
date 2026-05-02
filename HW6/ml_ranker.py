import numpy as np
from sklearn import linear_model
from sklearn.model_selection import KFold
from collections import defaultdict
import csv

def load_feature_matrix(csv_file):
    rows = []
    with open(csv_file, 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            rows.append(row)
    return rows

def train_and_rank(rows, feature_names, n_splits=5):
    X = []
    y = []
    qid_list = []
    docno_list = []
    
    for row in rows:
        X.append([float(row[name]) for name in feature_names])
        y.append(int(row['label']))
        qid_list.append(row['qid'])
        docno_list.append(row['docno'])
    
    X = np.array(X)
    y = np.array(y)
    
    kf = KFold(n_splits=n_splits, shuffle=True, random_state=42)
    
    all_predictions = []
    all_coefficients = []
    
    print(f"\n{'='*50}")
    print(f"Training with {n_splits}-fold cross validation")
    print(f"{'='*50}")
    
    fold_num = 1
    for train_idx, test_idx in kf.split(X):
        X_train, X_test = X[train_idx], X[test_idx]
        y_train, y_test = y[train_idx], y[test_idx]
        
        regr = linear_model.LinearRegression()
        regr.fit(X_train, y_train)
        
        print(f"\nFold {fold_num}:")
        for name, coef in zip(feature_names, regr.coef_):
            print(f"  {name}: {coef:.6f}")
        
        all_coefficients.append(regr.coef_)
        
        predictions = regr.predict(X_test)
        
        for i in range(len(predictions)):
            all_predictions.append({
                'qid': qid_list[test_idx[i]],
                'docno': docno_list[test_idx[i]],
                'score': predictions[i],
                'fold': fold_num
            })
        
        fold_num += 1
    
    avg_coef = np.mean(all_coefficients, axis=0)
    print(f"\n{'='*50}")
    print("Average Coefficients:")
    for name, coef in zip(feature_names, avg_coef):
        print(f"  {name}: {coef:.6f}")
    
    return all_predictions, avg_coef

def generate_rankings(predictions, output_file):
    query_results = defaultdict(list)
    for pred in predictions:
        query_results[pred['qid']].append((pred['docno'], pred['score']))
    
    with open(output_file, 'w') as f:
        for qid in sorted(query_results.keys(), key=lambda x: int(x)):
            docs = sorted(query_results[qid], key=lambda x: x[1], reverse=True)
            for rank, (docno, score) in enumerate(docs[:100], 1):
                f.write(f"{qid} Q0 {docno} {rank} {score:.6f} ML_Linear\n")
    
    print(f"\nRankings saved to {output_file}")
    print(f"  Queries: {len(query_results)}")

def save_coefficients(rows, feature_names, output_file):
    X = []
    y = []
    for row in rows:
        X.append([float(row[name]) for name in feature_names])
        y.append(int(row['label']))
    
    X = np.array(X)
    y = np.array(y)
    
    regr = linear_model.LinearRegression()
    regr.fit(X, y)
    
    with open(output_file, 'w') as f:
        f.write("Feature Coefficients\n")
        f.write("=" * 40 + "\n")
        for name, coef in zip(feature_names, regr.coef_):
            f.write(f"{name}: {coef:.6f}\n")
        f.write(f"\nIntercept: {regr.intercept_:.6f}\n")
    
    print(f"Coefficients saved to {output_file}")
    return regr.coef_

def main():
    print("Loading feature matrix...")
    rows = load_feature_matrix("feature_matrix.csv")
    print(f"Loaded {len(rows)} rows")
    
    feature_names = ['OkapiTF', 'TFIDF', 'BM25', 'Laplace', 'JelinekMercer', 'ES_Builtin']
    
    predictions, avg_coef = train_and_rank(rows, feature_names, n_splits=5)
    
    generate_rankings(predictions, "results_ML_Linear.txt")
    
    save_coefficients(rows, feature_names, "ml_coefficients.txt")

if __name__ == "__main__":
    main()