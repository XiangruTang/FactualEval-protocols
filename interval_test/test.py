import json

with open('bws_output.json') as f:
  bws_output = json.load(f)

with open('bws_output_redo.json') as f:
  bws_output_redo = json.load(f)

with open('likert_output.json') as f:
  likert_output = json.load(f)

with open('likert_output_redo.json') as f:
  likert_output_redo = json.load(f)

# *************************************************************************************
# likert_user_score:
# This dictionary maps each turker to an array of (orig score, new score)
# *************************************************************************************

likert_user_score = {}

for task in likert_output_redo:
    for model in likert_output_redo[task]:
        for turker_score_pair_redo in likert_output_redo[task][model]:
            turker = turker_score_pair_redo[0]
            if turker not in likert_user_score:
                likert_user_score[turker] = []
            redo_score = turker_score_pair_redo[1]
            
            # Find that turker in the original
            # "Task 9" is blank
            if model not in likert_output[task]:
                continue

            for turker_score_pair in likert_output[task][model]:
                if turker_score_pair[0] == turker:
                    orig_score = turker_score_pair[1]
                    break

            likert_user_score[turker].append((orig_score, redo_score))

# *************************************************************************************
# bws_user_rank:
# This dictionary maps each turker to an array of (orig best/worst summary, new best_worst_summary)
# *************************************************************************************

bws_user_rank = {}

for task in bws_output_redo:
    for category in bws_output_redo[task]:
        for turker_rank_pair_redo in bws_output_redo[task][category]:
            turker = turker_rank_pair_redo[0]
            if turker not in bws_user_rank:
                bws_user_rank[turker] = []
            redo_rank = turker_rank_pair_redo[1]
            
            if category not in bws_output[task]:
                continue

            for turker_rank_pair in bws_output[task][category]:
                if turker_rank_pair[0] == turker:
                    orig_rank = turker_rank_pair[1]
                    break

            bws_user_rank[turker].append((orig_rank, redo_rank))

# *************************************************************************************
# Likert average difference:
# For each turker, measure the average absolute deviation of the scores
# *************************************************************************************

likert_average_diff = {}
for user in likert_user_score:
    tmp_diff_sum = 0
    for score_pair in likert_user_score[user]:
        tmp_diff_sum += abs(int(score_pair[0]) - int(score_pair[1]))
    likert_average_diff[user] = tmp_diff_sum/len(likert_user_score[user])

print(likert_average_diff)

# *************************************************************************************
# BWS average difference:
# For each turker, measure the average number of differences of all best-worst rankings
# *************************************************************************************

bws_average_diff = {}
for user in bws_user_rank:
    tmp_diff_sum = 0
    for score_pair in bws_user_rank[user]:
        if score_pair[0] != score_pair[1]:
            tmp_diff_sum += 1

    bws_average_diff[user] = tmp_diff_sum/len(bws_user_rank[user])

print(bws_average_diff)


with open('likert_average_diff.json', 'w', encoding='utf-8') as f:
    json.dump(likert_average_diff, f, ensure_ascii=False, indent=4)

with open('bws_average_diff.json', 'w', encoding='utf-8') as f:
    json.dump(bws_average_diff, f, ensure_ascii=False, indent=4)


print("likert: ", sum(likert_average_diff.values())/len(likert_average_diff.values()))
print("bws: ", sum(bws_average_diff.values())/len(bws_average_diff.values()))

