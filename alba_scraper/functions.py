import requests
from bs4 import BeautifulSoup
from tqdm import tqdm
import csv

# brand별 모집 공고 페이지 url 추출
def extract_brand_url():
    res = requests.get("http://www.alba.co.kr/")
    soup = BeautifulSoup(res.text, "html.parser")
    lis = soup.find_all(class_="impact")
    urls = []
    companies = []
    for li in lis:
        a = li.find("a")
        span = li.find("span", class_="company")
        urls.append(a["href"])
        companies.append(span.text)

    return urls, companies

# 페이지 데이터 추출
def extract_page_data(urls):
    jobs_list = []

    for url in tqdm(urls):
        page = 1
        jobs = []
        while True:
            paged_url = f"{url}job/brand/?page={page}&pagesize = 50"
            page +=1
            res = requests.get(paged_url)
            soup = BeautifulSoup(res.text, "html.parser")
            tbody = soup.find("tbody")
            try:
              trs = tbody.find_all("tr")
            except:
              break
            if len(trs)<2:
                break
            for tr in trs:
                tds = tr.find_all("td")
                if len(tds)<2: #공고 요약 보기 들어있는 tr 거르기
                    continue
                try:
                    place = tds[0].text
                    title = tds[1].find("span").text
                    time = tds[2].text
                    pay = tds[3].text
                    date = tds[4].text
                    job = {
                        "place": place,
                        "title": title,
                        "time": time,
                        "pay": pay,
                        "date":date,
                    }
                    jobs.append(job)
                except:
                    continue
        jobs_list.append(jobs)

    return jobs_list

# csv로 저장
def save_as_csv(jobs, company_name):
    file = open(f"{company_name}.csv", mode="w", encoding="utf-8")
    writer = csv.writer(file)
    for job in tqdm(jobs):
        writer.writerow(list(job.values()))