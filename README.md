# CS70 PDF Generator
-------------
This code is for generating pdfs given short answer submissions on gradescope

`gradescope_csv_to_submissions.py` requires
1. An `answers.csv`, the answers received by gradescope
2. A `roster.csv`, the roster containing a list of students, student emails, and sids
it will then
1. Generate an outline in the stdout that should be copied to `outline.json` with question names modified
2. Create a `student_submissions.csv` file which will be used to generate pdfs

`student_submissions.py` requires
1. The `outline.json` that has all of the questions
2. The `student_submissions.csv` file generated by the above script
3. The relevant `output_xx` images in `./question_imgs/`
This will generate one PDF per SID in the `output/` folder when run. By default it uses all available cores.