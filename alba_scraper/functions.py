import math

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
        links = li.findAll("a", class_="brandHover")
        if links != []:
            for link in links:
                urls.append(link["href"])
                span = link.find("span", class_="company")
                if "." in span.text:
                    company = span.text.split(".")[0]
                    company = company.rstrip(" >")
                    companies.append(company)
                elif "/" in span.text:
                    company = span.text.replace("/", "&")
                    company = company.rstrip(" >")
                    companies.append(company)
                else:
                    company = span.text.rstrip(" >")
                    companies.append(company)


    return urls, companies


# 페이지 데이터 추출
def extract_page_data(urls):
    jobs_list = []

    for url in tqdm(urls):
        jobs = []
        res = requests.get(url)
        soup = BeautifulSoup(res.text, "html.parser")
        jobCount = soup.find("p", class_="jobCount")
        if(jobCount == None):
            continue
        lastPage = math.ceil(int(jobCount.find("strong").text.replace(",", ""))/50)
        for i in range(1, lastPage+1):
            paged_url = f"{url}job/brand/?page={i}&pagesize = 50"
            res = requests.get(paged_url)
            soup = BeautifulSoup(res.text, "html.parser")
            tbody = soup.find("tbody")
            trs = tbody.find_all("tr")

            if len(trs) < 2:
                break
            for tr in trs:
                tds = tr.find_all("td")
                if len(tds) < 2:  # 공고 요약 보기 들어있는 tr 거르기
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
                        "date": date,
                    }
                    jobs.append(job)
                except:
                    continue
        jobs_list.append(jobs)

    return jobs_list


# csv로 저장
def save_as_csv(jobs_list, company_names):
    for i in range(len(jobs_list)):
        file = open(f"{company_names[i]}.csv", mode="w", encoding="utf-8")
        writer = csv.writer(file)
        for job in tqdm(jobs_list[i]):
            writer.writerow(list(job.values()))
