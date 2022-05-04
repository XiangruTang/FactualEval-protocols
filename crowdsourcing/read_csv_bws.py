import os
import csv

path = "./question_mapping_bws.csv"
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
                article_to_answer_order[index + 1][row_number] = int(value)

        row_number += 1
    # print(article_to_answer_order)


directory = "./bws_csv/"
summary_number_to_name = {1:"pegasus", 2:"prophetnet", 3:"bart", 4:"bertextabs"}

for root,dirs,files in os.walk(directory):
    for file in files:
        if file.endswith(".csv"):
            start_number = int(file.split("Likert ")[1].split("-")[0])
            # print(start_number)
            with open(directory + file, newline='') as csvfile:
                csvreader = csv.reader(csvfile, delimiter=',', quotechar='"')
                row_number = 0
                for row in csvreader:
                    if row_number == 0:
                        pass
                    else:
                        for index, value in enumerate(row[2:]):
                            
                            if not value:
                                continue

                            # 1-indexed
                            article_number = start_number + index // 4 
                            summary_number = article_to_answer_order[article_number][index % 4 + 1]
                            summery_name = summary_number_to_name[summary_number]

                            if summery_name not in article_to_summary_scores[article_number]:
                                article_to_summary_scores[article_number][summery_name] = []

                            article_to_summary_scores[article_number][summery_name].append(int(value))

                    row_number += 1


print(article_to_summary_scores)

