import pdfkit
import json
import base64

header = """
    <html>
      <style>
        .external {
          display: table;
          height: 100%;
          width: 100%;
        }
        .response {
          margin-left: auto;
          margin-right: auto;
          border: 1px solid black;
          width: 400px;
          height: 400px;
          font-size: 2em;
        }
        .q-img {
          max-width: 100%;
          margin-top: 40px;
        }
      </style>
"""

footer = """
    </html>
"""

template = """
    <div class="external">
      <h3>{title}</h3>
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


def html_from_submission(submission, qdata):
    res = [header]
    res.append(
        template.format(title="Student ID",
                        imgb64="",
                        q_resp=submission["sid"])
    )

    #Order correctly
    for qid in sorted(submission["qs"].keys()):
        q = submission["qs"][qid]
        qinfo = qdata[qid]
        res.append(
            template.format(title=qinfo["name"],
                            imgb64=qinfo["imgb64"],
                            q_resp=q["q_resp"])
        )

    res.append(footer)

    return ''.join(res)

def pdf_from_html(sid, html):
    opts = {
        'page-size': 'Letter',
        'margin-top': '0.75in',
        'margin-right': '0.75in',
        'margin-bottom': '0.75in',
        'margin-left': '0.75in',
        'encoding': "UTF-8"
    }
    pdfkit.from_string(html, "output/" + str(sid) + ".pdf")




outline = get_outline()
question_data = get_question_data(outline)

student_submission = {
        "sid": 0,
        "qs": {"Q2.1": {"q_resp": "False"}}
}


sub_html = html_from_submission(student_submission, question_data)
pdf_from_html(student_submission["sid"], sub_html)




