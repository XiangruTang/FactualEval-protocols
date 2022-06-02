#encoding=utf-8
import os
import csv

#original data
directory = "./annotation/bws_csv_xsum/"
#shuffle order
path = "./shuffle_order/question_mapping_bws_xsum.csv"
#final result
final_file = './final_result/xsum.bws.csv'

corpus_name = 'xsum'

article_to_answer_order = {}
article_to_best_worst = {}

with open(path, newline='') as csvfile:
    csvreader = csv.reader(csvfile, delimiter=',', quotechar='|')
    row_number = 0
    for row in csvreader:
        if row_number == 0:
            for index, value in enumerate(row[1:]):
                article_to_answer_order[int(value)] = {}
                article_to_best_worst[int(value)] = {"best": [], "worst": []}
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
for root,dirs,files in os.walk(directory):
    for file in files:
        if file.endswith(".csv"):
            start_number = int(file.split("BWS ")[1].split("-")[0])

            with open(directory + file, newline='') as csvfile:
                csvreader = csv.reader(csvfile, delimiter=',', quotechar='"')
                row_number = 0
                for row in csvreader:
                    if row_number == 0:
                        pass
                    else:
                        for index, value in enumerate(row[3:-1]):
                            assert value is not None

                            # 1-indexed
                            article_number = start_number + index // 2
                            summary_number =  article_to_answer_order[article_number][int(value[-1])]
                            summary_name = summary_number_to_name[summary_number]
                            if index % 2 == 0:
                                article_to_best_worst[article_number]["best"].append(summary_name)
                            else:
                                article_to_best_worst[article_number]["worst"].append(summary_name)
                    row_number += 1


#print(article_to_best_worst)
for key, val in article_to_best_worst.items():
    try:
        for k1, v1 in val.items():
            try:
                assert len(v1) == 3
            except:
                article_to_best_worst[key][k1] = v1[1:]
                assert len(article_to_best_worst[key][k1]) == 3
    except:
        import pdb;pdb.set_trace()
        print()

def divide_chunks(l, n):
    for i in range(0, len(l), n): 
        yield l[i:i + n]
  
examples = list(range(1, 101))
chunks = list(divide_chunks(examples, 5))

ids = ['pegasus', 'prophetnet', 'bart', 'bertextabs']

fieldnames = ["annotator", "document", "system", "corpus", "rank (max 4 and least 1, else 2)"]
with open(final_file, "w") as outputf:
    writer = csv.DictWriter(outputf, fieldnames=fieldnames)
    for chunk_count, chunk in enumerate(chunks):
        for annotator in range(3):
            for document in chunk:
                for system in ids:
                    annotator_final = chunk_count * 3 + annotator + 1
                    best = article_to_best_worst[document]['best'][annotator]
                    worst = article_to_best_worst[document]['worst'][annotator]
                    if system == best:
                        score = 4
                    elif system == worst:
                        score = 1
                    else:
                        score = 2
                    cur_dict = {"annotator": annotator_final, "document": document, "system": system, "corpus": corpus_name, "rank (max 4 and least 1, else 2)": score}
                    writer.writerow(cur_dict)

