#encoding=utf-8
import os
import csv

path = "./question_mapping_bws_xsum.csv"
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

directory = "./bws/"
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
                        turker_id = row[1].strip()
                        for index, value in enumerate(row[3:-1]):
                            assert value is not None

                            # 1-indexed
                            article_number = start_number + index // 2
                            summary_number =  article_to_answer_order[article_number][int(value[-1])]
                            summary_name = summary_number_to_name[summary_number]
                            if index % 2 == 0:
                                article_to_best_worst[article_number]["best"].append((turker_id, summary_name))
                            else:
                                article_to_best_worst[article_number]["worst"].append((turker_id, summary_name))
                    row_number += 1


print(article_to_best_worst)

import json
with open('bws_output_redo.json', 'w') as f:
    json.dump(article_to_best_worst, f)

