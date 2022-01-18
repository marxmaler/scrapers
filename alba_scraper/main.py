from functions import extract_brand_url, extract_page_data, save_as_csv

urls, companies = extract_brand_url()
print(companies)
# jobs_list = extract_page_data(urls)
# for i in range(len(jobs_list)):
#     save_as_csv(jobs_list[i], companies[i])
