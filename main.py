from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup

options = Options()
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")

browser = webdriver.Chrome(options=options)


def get_page_count(keyword):
    base_url = "https://www.indeed.com/jobs?q="
    browser.get(f"{base_url}{keyword}")

    soup = BeautifulSoup(browser.page_source, "html.parser")
    pagination = soup.find("nav", attrs={"aria-label": "pagination"})
    pages = pagination.select("div a")
    count = len(pages)
    if count >= 5:
        return 5
    else:
        return count


def extract_indeed_jobs(keyword):
    pages = get_page_count(keyword)
    results = []
    for page in range(pages):
        base_url = "https://www.indeed.com/jobs"
        final_url = browser.get(f"{base_url}?q={keyword}&start={page*10}")
        response = browser.get(final_url)
        soup = BeautifulSoup(response.page_source, "html.parser")
        job_list = soup.find("ul", class_="jobsearch-ResultsList")
        jobs = job_list.find_all("li", recursive=False)
        for job in jobs:
            zone = job.find("div", class_="mosaic-zone")
            if zone == None:
                anchor = job.select_one("h2 a")
                title = anchor["aria-label"]
                link = anchor["href"]
                company = job.find("span", class_="companyName")
                location = job.find("div", class_="companyLocation")
            job_data = {
                'link': f"https://kr.indeed.com{link}",
                'company': company.string,
                'location': location.string,
                'position': title
            }
            results.append(job_data)
    return results


jobs = extract_indeed_jobs("python")

print(len(jobs))
