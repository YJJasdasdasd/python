from extractors.indeed import extract_indeed_jobs
from extractors.wwr import extract_wwr_jobs

keyword = input("무엇을 검색할래?")

indeed = extract_indeed_jobs(keyword)
wwr = extract_wwr_jobs(keyword)

jobs = indeed + wwr

for job in jobs:
    print(job)
    print("/////\n//////")
