This is a complete Information Retrieval (IR) system implementation for the given assignment.

## PART 1: INSTALLING EVERYTHING YOU NEED

1. Install Python (if not already installed)
**Download Python:**
**Verify Python is installed:**
Open Command Prompt and type:
    python --version
You should see something like Python 3.13.0

2. Install Elasticsearch (the search database)
Download Elasticsearch:

Go to https://www.elastic.co/downloads/elasticsearch

Download version 7.17.15(Download the Zip file) (not the latest 8.x - stick with 7.x); I don't know why the latest isn't working for the dataset given.

Extract the ZIP file to C:\Users\YourName\Desktop\elasticsearch-7.17.15
Run these commands:

    cd C:\Users\YourName\Desktop\elasticsearch-7.17.15\bin
    elasticsearch

Keep this window open. Elasticsearch is now running.

Verify Elasticsearch is working:
Open your web browser and go to: http://localhost:9200
You should see a JSON response with cluster information.

3. Install Visual Studio C++ Compiler
Why do you need this? trec_eval (evaluation tool) needs to be compiled from C code.
Download Visual Studio Build Tools:
Go to https://visualstudio.microsoft.com/downloads/#build-tools-for-visual-studio-2022

Scroll down to "Build Tools for Visual Studio 2022",Run the installer,Select "Desktop development with C++",Click "Install",After restart, verify compiler works:
Open "Developer Command Prompt for VS 2022" (search in Start Menu)
Type:

    cl

You should see compiler information.

4. Install trec_eval (evaluation tool)
Download source code:

Go to https://github.com/usnistgov/trec_eval
Click "Download ZIP"

Extract to C:\Users\YourName\Desktop\trec_eval-9.0.8
Compile trec_eval:
Open "Developer Command Prompt for VS 2022"
Navigate to the source folder:

    cd C:\Users\YourName\Desktop\trec_eval-9.0.8\trec_eval-9.0.8

Run the build command:

    build.bat
Wait for compilation to finish (you will see many warnings - ignore them)
You should now have trec_eval.exe in the folder
Copy trec_eval to your project folder:

    copy trec_eval.exe C:\Users\YourName\Desktop\cranfield\

5. Install Python package (elasticsearch)
Open Command Prompt and run:

    pip install elasticsearch
    
## PART 2: DOWNLOAD THE DATA FILES
The Cranfield dataset contains 1,400 documents, 225 queries, and relevance judgments.

Download from IS telegram-ISR section or : https://github.com/oussbenk/cranfield-trec-xml
You need these 3 files:
cran.all.1400.xml (documents),cran.qry.xml (queries),cranqrel.trec.txt (relevance judgments - answer key)
Place them in your project folder: C:\Users\YourName\Desktop\cranfield

## PART 3: CREATE YOUR PROJECT FOLDER
Create a folder on your desktop
Your folder should now contain:
Data files (from download):cran.all.1400.xml,cran.qry.xml,cranqrel.trec.txt,Python scripts-index.py,helpers.py,ranking.py,queries.py,run_fast.py,es_builtin.py,

Result files (generated after running):results_OkapiTF.txt,results_TFIDF.txt,results_BM25.txt,results_Laplace.txt,results_JelinekMercer.txt,results_ES_Builtin.txt,

## PART 4: THE PYTHON SCRIPTS 
Script 1: index.py

What it does: Reads the XML documents and sends them to Elasticsearch.
What happens when you run it:
Opens cran.all.1400.xml
Extracts docno, title, text from each document
Combines title + text, converts to lowercase
Removes extra spaces
Counts words per document
Sends all 1,400 documents to Elasticsearch

How to run:

    python index.py

Script 2: helpers.py

What it does: Provides functions that all ranking models need.
Functions provided:
get_tf(term, doc_id) - How many times does this word appear in this document?
get_df(term) - In how many documents does this word appear?
get_doc_length(doc_id) - How many total words in this document?
get_all_doc_ids() - List of all document IDs
Also computes global stats:

N = total documents (1,400)

avgdl = average document length (176.73 words)

V = vocabulary size (~247,426 unique words)

Script 3: queries.py

What it does: Reads the 225 queries from XML file.
What happens when you run it:
Opens cran.qry.xml
Extracts num (query ID) and title (query text)
Cleans text (lowercase, removes punctuation)
Splits into individual words (terms)

Script 4: ranking.py

What it does: Implements all 5 ranking formulas using helpers.py.
Formula 1: Okapi TF

score = sum( tf / (tf + 0.5 + 1.5 × (doc_len / avg_len)) )
Formula 2: TF-IDF

score = sum( okapi_tf × log((N - df + 0.5) / (df + 0.5) + 1) )
Formula 3: BM25

Parameters: k1 = 1.2, b = 0.75
score = sum( log((N - df + 0.5)/(df + 0.5) + 1) × (tf × (k1 + 1)) / (tf + k1 × (1 - b + b × (len / avg_len))) )
Formula 4: Laplace Language Model

score = sum( log((tf + 1) / (doc_len + V)) )
Formula 5: Jelinek-Mercer Language Model

Parameters: λ = 0.7
score = sum( log( λ × (tf / doc_len) + (1 - λ) × (1 / V) ) )

Script 5: run_fast.py

What it does: Runs BM25, Laplace, and Jelinek-Mercer models efficiently.
It loads all data once instead of calling Elasticsearch 1.5 million times-the previous used python file was named run_model.py and it was slow since it was calling Elasticsearch 1.5 million times.

How to run:

    python run_fast.py

What happens:
Loads all 1,400 documents from Elasticsearch (1 call)
Loads term vectors for all documents (1,400 calls)
Pre-computes term frequencies and document frequencies
Runs BM25, Laplace, Jelinek-Mercer from cache (0 calls to ES)
Creates 3 result files

Script 6: es_builtin.py

What it does: Uses Elasticsearch's built-in search
How to run:
    python es_builtin.py

What happens:

For each of 225 queries, sends a match query to Elasticsearch
Elasticsearch returns top 100 documents using its internal BM25
Saves results to results_ES_Builtin.txt

                    HOW TO RUN EVERYTHING
Step 1: Start Elasticsearch
Open Command Prompt #1:

    cd C:\Users\YourName\Desktop\elasticsearch-7.17.15\bin
    elasticsearch
Keep this window open.

Step 2: Index the documents
Open Command Prompt #2:

    cd C:\Users\YourName\Desktop\cranfield
    python index.py
Step 3: Run the models

    python run_fast.py
    python es_builtin.py
Step 4: Evaluate results with trec_eval

    trec_eval cranqrel.trec.txt results_BM25.txt
    trec_eval cranqrel.trec.txt results_TFIDF.txt
    trec_eval cranqrel.trec.txt results_OkapiTF.txt
    trec_eval cranqrel.trec.txt results_Laplace.txt
    trec_eval cranqrel.trec.txt results_JelinekMercer.txt
    trec_eval cranqrel.trec.txt results_ES_Builtin.txt
For each, look for the line that starts with map. This is the MAP score.

## PART 5: FILE FORMAT EXPLANATION
Each line:

1 Q0 184 1 24.28 BM25
Column	Meaning	Example
1	Query ID	1
2	Literal "Q0" (required by TREC)	Q0
3	Document ID	184
4	Rank (position in results)	1
5	Score from the model	24.28
6	Model name	BM25
Qrels file format (cranqrel.trec.txt)
Each line:

text
1 0 184 1
Column	Meaning	Example
1	Query ID	1
2	Iteration (always 0)	0
3	Document ID	184
4	Relevance (1=relevant, 0=not relevant)	1
