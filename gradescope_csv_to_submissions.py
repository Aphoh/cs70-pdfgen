# Converts gradescope csvs into a useable student_submissions.csv, and generates an outline.json
# answers.csv: csv from gradesope
# roster.csv: csv of email,sid,role,etc
import pandas as pd
import json
import pprint

# Generate outline
df = pd.read_csv("answers.csv").fillna("empty")
outputs = sorted(df["question_content"].str[30:43].unique())
questions = {}
for o in outputs:
    qid = "Q" + o[7:9]
    questions[qid] = {"name": qid, "img": o}
outline = {"questions": questions}
print(json.dumps(outline, indent=4))


roster = pd.read_csv("roster.csv", index_col="Email")
dfsid = df.join(roster, on="email_address")
dfsid["qid"] = "Q" + dfsid["question_content"].str[37:39]

# convert weird json answers to simple string

ans_text = []
for ind, a in dfsid["answers"].iteritems():
    r = json.loads(a)
    if not r:
        ans_text.append("blank")
    elif "0" in r and "1" not in r:
        ans_text.append(r['0'])
    else:
        ans_str = ',\n'.join(["part {}: {}".format(int(k)+1, v) for k, v in r.items()])
        ans_text.append(ans_str)
dfsid["ans_text"] = ans_text

# drop extraneus columns and export
dfsid.drop(["user_id", "question_title", "question_content", "graded", "answers", "name", "Role"], axis=1).to_csv("student_submissions.csv", index=False)
