import os
import csv

path = "./question_mapping_likert_xsum.csv"
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

for key, val in article_to_answer_order.items():
    for row_num in range(1, 5):
        test = article_to_answer_order[key][row_num]

directory = "./likert/"
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
                        turker_id = row[1].strip()
                        # remove "any comments" & "understand the instructions"
                        tmp_row = row[3:-1]
                        if len(tmp_row) == 18:
                            tmp_row = row[2:]
                        for index, value in enumerate(tmp_row):
                            if not value:
                                missing_annotations.add(file)
                                continue

                            article_number = start_number + index // 4 
                            summary_number = article_to_answer_order[article_number][index % 4 + 1]
                            summary_name = summary_number_to_name[summary_number]

                            if summary_name not in article_to_summary_scores[article_number]:
                                article_to_summary_scores[article_number][summary_name] = []

                            article_to_summary_scores[article_number][summary_name].append((turker_id, int(value)))

                    row_number += 1

print(article_to_summary_scores)

import json
with open('likert_output_redo.json', 'w') as f:
    json.dump(article_to_summary_scores, f)
