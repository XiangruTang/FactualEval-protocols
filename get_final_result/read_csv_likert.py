import os
import csv

#original data
directory = "./annotation/likert_10_csv_cnn/"
#shuffle order
path = "./shuffle_order/question_mapping_cnn.csv"
#final result
final_file = './final_result/cnndm.likert_10.csv'

#corpus
corpus_name = 'cnndm'

article_to_answer_order = {}
article_to_summary_scores = {}

with open(path, newline='') as csvfile:
    csvreader = csv.reader(csvfile, delimiter=',', quotechar='|')
    row_number = 0
    for row in csvreader:
        if row_number == 0:
            for index, value in enumerate(row[1:]):
                article_to_answer_order[int(value)] = {}
                article_to_summary_scores[int(value)] = {}
        else:
            for index, value in enumerate(row[1:]):
                if not value:
                    continue
                article_to_answer_order[index + 1][row_number] = int(value)
        row_number += 1
    # print(article_to_answer_order)

for key, val in article_to_answer_order.items():
    for row_num in range(1, 5):
        test = article_to_answer_order[key][row_num]

summary_number_to_name = {1:"pegasus", 2:"prophetnet", 3:"bart", 4:"bertextabs"}

missing_annotations = set()
for _, _, files in os.walk(directory):
    for file in files:
        if file.endswith(".csv"):
            start_number = int(file.split("Likert ")[1].split("-")[0])
            with open(directory + file, newline='') as csvfile:
                csvreader = csv.reader(csvfile, delimiter=',', quotechar='"')
                row_number = 0
                for row in csvreader:
                    if row_number == 0:
                        pass
                    else:
                        # remove "any comments" & "understand the instructions"
                        tmp_row = row[3:-1]
                        if len(tmp_row) == 18:
                            tmp_row = row[2:]
                        for index, value in enumerate(tmp_row):
                            if not value:
                                missing_annotations.add(file)
                                continue

                            # 1-indexed
                            article_number = start_number + index // 4 
                            summary_number = article_to_answer_order[article_number][index % 4 + 1]
                            summary_name = summary_number_to_name[summary_number]
                            #if article_number == 5:
                            #    print(f"start number: {start_number}", f"index: {index}", f"index % 4 + 1: {index % 4 + 1}", f"summary number: {summary_number}", f"summary name: {summary_name}", article_to_answer_order[article_number])
                            #    import pdb;pdb.set_trace()

                            if summary_name not in article_to_summary_scores[article_number]:
                                article_to_summary_scores[article_number][summary_name] = []

                            article_to_summary_scores[article_number][summary_name].append(int(value))

                    row_number += 1

bad = 0
# deleting the article number with missing annotations
#del article_to_summary_scores[9]
for key, val in article_to_summary_scores.items():
    try:
        assert len(val) == 4
        for k1, v1 in val.items():
            assert len(v1) == 3
    except:
        print(key)
        bad += 1
#print(article_to_summary_scores)
#print(f"This many articles: {len(article_to_summary_scores)}")
#print(f"This many examples have an incorrect number of model annotations or number of annotators from the above number: {bad}")
#print(f"These files are missing complete example annotations: {missing_annotations}")
#




def divide_chunks(l, n):
    for i in range(0, len(l), n): 
        yield l[i:i + n]
  
examples = list(range(1, 101))
chunks = list(divide_chunks(examples, 5))

ids = ['pegasus', 'prophetnet', 'bart', 'bertextabs']

fieldnames = ["annotator", "document", "system", "corpus", "score"]
with open(final_file, "w") as outputf:
    writer = csv.DictWriter(outputf, fieldnames=fieldnames)
    for chunk_count, chunk in enumerate(chunks):
        for annotator in range(3):
            for document in chunk:
            #    if document == 9:
            #        continue
                for system in ids:
                    annotator_final = chunk_count * 3 + annotator + 1
                    score = article_to_summary_scores[document][system][annotator]
                    cur_dict = {"annotator": annotator_final, "document": document, "system": system, "corpus": corpus_name, "score": score}
                    writer.writerow(cur_dict)

#for key, val in article_to_summary_scores.items():
#    import pdb;pdb.set_trace()
#    try:
#        assert len(val) == 4
#        for k1, v1 in val.items():
#            assert len(v1) == 3
#    except:
#        print(key)
#        bad += 1
