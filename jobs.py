from bs4 import BeautifulSoup
import requests
import time

print("What job are you looking for?")
role = input(">")

html_text = requests.get(f'https://www.jobstreet.com.sg/en/job-search/{role}-jobs/').text
soup = BeautifulSoup(html_text, 'lxml')
jobs = soup.find('div', class_='FYwKg')
prefer_loc = input("Your preferred location (type nil if no preference): ")
print(f"Filtering for {prefer_loc}...")

def find_jobs():
    companies = jobs.find_all('div', class_ = 'FYwKg _17IyL_0 _2-ij9_0 _3Vcu7_0 MtsXR_0')
    for index, company in enumerate(companies):
        try:
            company_name = company.find('span', class_= 'FYwKg _2Bz3E C6ZIU_0 _6ufcS_0 _2DNlq_0 _29m7__0').text
        except Exception:
            company_name = "Unknown or Confidential"
        company_location = company.find('span', class_='FYwKg _3MPd_ _2Bz3E And8z').text
        posted = company.find('span', class_="FYwKg _2Bz3E C6ZIU_0 _1_nER_0 _3KSG8_0 _29m7__0").text
        job_name = company.find('div', class_="FYwKg _2j8fZ_0 sIMFL_0 _1JtWu_0").text
        job_pay = company.find_all('span', class_='FYwKg _2Bz3E C6ZIU_0 _1_nER_0 _2DNlq_0 sQuda_0')
        link = company.find('h1', class_='FYwKg _2Bz3E C6ZIU_0 _6ufcS_0 _2DNlq_0 sQuda_0').a['href']
        if len(job_pay) == 2:
            job_pay_included = job_pay[1].text

        if prefer_loc.upper() != company_location.upper() and prefer_loc != 'nil':
            continue

        with open(f"Available Jobs/job{index}.txt", "w", encoding="utf-8") as f:
            f.write(f"Role: {job_name}\n")
            f.write(f"Company: {company_name}\n")
            if len(job_pay) == 2:
                f.write(f"Pay: {job_pay_included}\n")
            f.write(f"Location: {company_location}\n")
            f.write(f"{posted}\n")
            f.write(f"More info: https://www.jobstreet.com.sg{link}\n")

if __name__ == '__main__':
    while True:
        find_jobs()
        waiting_time = 10
        print(f"Refreshing after {waiting_time} min...")
        time.sleep(waiting_time * 60)
