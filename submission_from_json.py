import pdfkit
import json
import base64
import pandas as pd
import multiprocessing as mp
import os

header = """
    <html>
      <style>
        .external {
          display: table;
          height: 1426px;
          width: 8.5in;
        }
        .response {
          margin-left: auto;
          margin-right: auto;
          margin-top: 5px;
          border: 1px solid rgba(255, 0, 0, .5);
          width: 400px;
          min-height: 400px;
          height: auto;
          font-size: 2.5em;
          overflow-wrap: break-word;
        }
        .q-name {
          margin-bottom: 40px;
        }
        .q-img {
          max-width: 100%;
        }
      </style>
"""

footer = """
    </html>
"""

noimg_template = """
    <div class="external">
      <h3 class="q-name">{title}</h3>
      <div class="response">
        {q_resp1}
      </div>
      <div class="response">
        {q_resp2}
      </div>
    </div>
"""

template = """
    <div class="external">
      <h3 class="q-name">{title}</h3>
      <div>
          <img class="q-img" src="data:image/jpg;base64,{imgb64}"/>
      </div>
      <div class="response">
        {q_resp}
      </div>
    </div>
"""

def get_outline():
    outline = None
    with open("outline.json", 'r') as fin:
        outline = json.load(fin)

    return outline


def get_question_data(outline):
    question_data = {}
    for qid, q in outline["questions"].items():
        question_data[qid] = {}
        question_data[qid]["name"] = q["name"]
        with open("question_imgs/" + q["img"], 'rb') as fin:
            question_data[qid]["imgb64"] = base64.b64encode(fin.read()).decode('ascii')

    return question_data


def html_for_sid(sid, responses, qdata):
    res = [header]
    res.append(
        noimg_template.format(title="Student ID/Name",
                        imgb64="",
                        q_resp1=sid,
                        q_resp2=responses["_name"])
    )

    #Order correctly
    for qid in sorted(qdata.keys()):
        qinfo = qdata[qid]
        # Make sure question included in response
        q_resp = responses[qid] if qid in responses else ""
        res.append(
            template.format(title=qinfo["name"],
                            imgb64=qinfo["imgb64"],
                            q_resp=q_resp)
        )

    res.append(footer)

    return ''.join(res)

def pdf_from_html(sid, html):
    opts = {
        'page-size': 'Letter',
        'margin-top': '0.0in',
        'margin-right': '0.0in',
        'margin-bottom': '0.0in',
        'margin-left': '0.0in',
        'encoding': "UTF-8"
    }
    pdfkit.from_string(html, "output/" + str(sid) + ".pdf")


def submissions_dict(submissions_df):
    submissions = {}
    for sid, responses in submissions_df.groupby("SID"):
        resp_dict = {}
        for _, row in responses.iterrows():
            qid = row["qid"]
            resp_dict[qid] = row["ans_text"]
        submissions[sid] = resp_dict

        submissions[sid]["_name"] = responses.iloc[0]["Name"]

    return submissions


submissions_df = pd.read_csv("student_submissions.csv", dtype=str)
subs_dict = submissions_dict(submissions_df)

if not os.path.exists("output/"):
    os.makedirs("output/")


outline = get_outline()
question_data = get_question_data(outline)

def pdf_from_sid(sid):
    sub_html = html_for_sid(sid, subs_dict[sid], question_data)
    pdf_from_html(sid, sub_html)

pool = mp.Pool(mp.cpu_count())
pool.map(pdf_from_sid, list(subs_dict.keys()))

pool.close()



