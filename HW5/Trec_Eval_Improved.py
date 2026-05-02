from collections import OrderedDict
import math

relevanceJudgements = {}

def retrieveQueryResults(rankList):
    queryResults = OrderedDict()
    with open(rankList, 'r') as f:
        for line in f:
            items = line.strip().split()
            if len(items) < 3:
                continue
            queryID = items[0]
            documentID = items[2]
            if queryID in queryResults:
                queryResults[queryID].append(documentID)
            else:
                queryResults[queryID] = [documentID]
    return queryResults

def getRelevanceJudgements(qrel):
    global relevanceJudgements
    relevanceJudgements = {}
    with open(qrel, 'r') as f:
        for line in f:
            cols = line.strip().split()
            if len(cols) < 4:
                continue
            queryID = cols[0]
            documentID = cols[2]
            relevance = cols[3]
            if relevance == '1':
                if queryID in relevanceJudgements:
                    relevanceJudgements[queryID].append(documentID)
                else:
                    relevanceJudgements[queryID] = [documentID]

def designateVals(lst, val, rank):
    if rank in lst:
        lst[rank].append(val)
    else:
        lst[rank] = [val]
    return lst

def printMeanVals(lst, desc, kVals=[], qid=''):
    if not kVals:
        if len(lst) == 0:
            print(desc + ': 0.0000')
        else:
            print(desc + ': ' + str("{:.4f}".format(math.fsum(lst) / len(lst))))
    else:
        for k in kVals:
            if k in lst and len(lst[k]) > 0:
                val = math.fsum(lst[k]) / len(lst[k])
            else:
                val = 0.0
            if qid != '':
                print(f"{desc}{k} for {qid}: {val:.4f}")
            else:
                print(f"{desc}{k}: {val:.4f}")

def calculateMetrics(queryResults, option):
    kVals = [5, 10, 20, 50, 100]
    AP, RP, NDCG = [], [], []
    P, R, F1 = {}, {}, {}
    f = open("details.txt", 'w')
    
    for queryID in queryResults:
        if queryID not in relevanceJudgements:
            continue
        
        relevantDocuments = relevanceJudgements[queryID]
        results = queryResults[queryID]
        relevantNumber = 0
        psum = 0
        rp = 0
        relevanceScore = []
        
        for rank, document in enumerate(results, start=1):
            isRelevant = 1 if document in relevantDocuments else 0
            if isRelevant:
                relevantNumber += 1
            if rank <= len(relevantDocuments):
                rp = relevantNumber
            precision = relevantNumber / rank
            recall = relevantNumber / len(relevantDocuments) if len(relevantDocuments) > 0 else 0
            if isRelevant:
                psum += precision
            if rank in kVals:
                P = designateVals(P, precision, rank)
                R = designateVals(R, recall, rank)
                f1 = (2 * precision * recall) / (precision + recall) if (precision + recall) > 0 else 0
                F1 = designateVals(F1, f1, rank)
            relevanceScore.append(isRelevant)
            f.write(f"{queryID} {document} {rank} {isRelevant} {precision:.4f} {recall:.4f}\n")
        
        # DCG
        dc_value = sum(score / math.log(j + 2) for j, score in enumerate(relevanceScore))
        ideal = sorted(relevanceScore, reverse=True)
        idc_value = sum(score / math.log(j + 2) for j, score in enumerate(ideal))
        ndcg = dc_value / idc_value if idc_value > 0 else 0
        NDCG.append(ndcg)
        
        rPrecision = rp / len(relevantDocuments) if len(relevantDocuments) > 0 else 0
        RP.append(rPrecision)
        
        avgPrecision = psum / len(relevantDocuments) if len(relevantDocuments) > 0 else 0
        AP.append(avgPrecision)
        
        if option == 1:
            print(f"\nQuery {queryID}")
            print(f"Average Precision: {avgPrecision:.4f}")
            print(f"R-Precision: {rPrecision:.4f}")
            print(f"nDCG: {ndcg:.4f}")
    
    print("\n=== FINAL RESULTS ===")
    printMeanVals(AP, 'MAP')
    printMeanVals(RP, 'R-precision')
    printMeanVals(NDCG, 'nDCG')
    print("\nPrecision@K")
    printMeanVals(P, 'P@', kVals)
    print("\nRecall@K")
    printMeanVals(R, 'R@', kVals)
    print("\nF1@K")
    printMeanVals(F1, 'F1@', kVals)
    f.close()

def main():
    print("\nHW5 - TREC Evaluation")
    print("="*40)
    
    qrel_file = "qrels.txt"
    rank_file = "rankList.txt"
    
    queryResults = retrieveQueryResults(rank_file)
    getRelevanceJudgements(qrel_file)
    calculateMetrics(queryResults, 1)

if __name__ == "__main__":
    main()