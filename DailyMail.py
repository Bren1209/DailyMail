from bs4 import BeautifulSoup
import requests
import csv
import random
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import os

# Daily Rise issue nr. -- Stopped working after issue #10, reverted back to #2, now fixed.

issue_message = ''

if os.path.isfile('issue_nr.csv'):

    with open('issue_nr.csv', 'r') as f1:
        opened_file = f1.readlines()
        last_issue = opened_file[-1]

    next_issue = int(last_issue) + 1

    with open ('issue_nr.csv', 'w') as f2:
        f2.write(str(next_issue))

else:

    with open('issue_nr.csv', 'w', newline='') as csvfile:
        data = csv.writer(csvfile)
        data.writerow([0])

    with open('issue_nr.csv', 'r') as f1:
        opened_file = f1.readlines()
        last_issue = opened_file[-1]

    next_issue = int(last_issue) + 1

    with open('issue_nr.csv', 'w') as f2:
        f2.write(str(next_issue))


issue_message = f'\n------ ISSUE NR. {next_issue} ------'

####################################

# Get the latest article

r_article = requests.get('https://www.infoworld.com/category/python/').content

article_soup = BeautifulSoup(r_article, 'html.parser')

articles = article_soup.find_all('div', {'class': 'river-well article'})
article_titles = []
link_list = []

for article in articles:
    article_titles.append(article.h3.text.replace('\n', ''))
    link_list.append(article.h3.a['href'])

csv_title_list = []

if os.path.isfile('last_article.csv'):

    with open('last_article.csv', 'a+', newline='') as f:
        writer = csv.writer(f)
        writer.writerow([article_titles[0]])

    with open('last_article.csv', 'r') as f:
        data = csv.reader(f)
        for row in data:
            csv_title_list.append(row)

else:

    with open('last_article.csv', 'w', newline='') as csvfile:
        data = csv.writer(csvfile)
        data.writerow(["PyTorch 1.5 adds C++ power, distributed training"])
        data.writerow(["PyTorch 1.5 adds C++ power, distributed training"])

    with open('last_article.csv', 'a+', newline='') as f:
        writer = csv.writer(f)
        writer.writerow([article_titles[0]])

    with open('last_article.csv', 'r') as f:
        data = csv.reader(f)
        for row in data:
            csv_title_list.append(row)

article_message = ''

if csv_title_list[-1] == csv_title_list[-2]:
    article_message = '\nNo new article from InfoWorld today.'
else:
    full_link = 'https://www.infoworld.com/' + link_list[0]
    article_message = f'\n\nLATEST PYTHON ARTICLE: \n\n{article_titles[0]}\n{full_link}'


###########################################

# Get weather (double check date) - Got a better website, added more weather details

r = requests.get('https://www.yr.no/place/South_Africa/Western_Cape/Cape_Town/').content

soup = BeautifulSoup(r, 'html.parser')

forecast = soup.find_all('tr')
weather = []
for item in forecast:
    if '12:00' in item.text:
        weather.append(item.td.text.replace(' ', ''))
        weather.append(item.find('figure').text.replace('\n', ''))
        weather.append(item.find('td', {'class': 'temperature plus'}).text)

weather_message = f'\n\nToday\'s weather:\n\n{weather[0]}: {weather[2]} - {weather[1]}\n{weather[3]}: {weather[5]} - {weather[4]}'

############################################

# Get inspirational quotes

r_quote = requests.get('https://parade.com/936820/parade/good-morning-quotes/').content
r_quote2 = requests.get('https://parade.com/973277/jessicasager/inspirational-quotes/').content

quote_soup = BeautifulSoup(r_quote, 'html.parser')
quote2_soup = BeautifulSoup(r_quote2, 'html.parser')

morning_quotes = quote_soup.find_all('p')
inspir_quotes = quote2_soup.find_all('p')
quotes_results1 = []
quotes_results2 = []

for quote in morning_quotes:
    quotes_results1.append(quote.text)

for quote in inspir_quotes:
    quotes_results2.append(quote.text)

morning_quotes_cleaned = quotes_results1[7:-7]
morning_picked_quote = random.choice(morning_quotes_cleaned)
morning_message = ''

inspir_quotes_cleaned = quotes_results2[7:-6]
inspir_picked_quote = random.choice(inspir_quotes_cleaned)
inspirational_message = ''

if len(morning_picked_quote) > 20:
    morning_message = f'\nMorning Quote nr. {morning_picked_quote}'
else:
    morning_message = f'Yo sup. Quote length is less than 20 characters, so probably an author separated' \
                      f'from their quote by a <p>. Have a dope day!'

if len(inspir_picked_quote) > 20:
    inspirational_message = f'\nInspirational Quote nr. {inspir_picked_quote}'
else:
    inspirational_message = f'Yo sup. Quote length is less than 20 characters, so probably an author separated ' \
                      f'from their quote by a <p>. Have a dope day though!'

##############################################3

# Check Python Internship Job Status:

r_internship = requests.get('https://www.adzuna.co.za/search?q=python%20developer&w=Cape%20Town%20Region%2C%20Western%20Cape').content

internship_soup = BeautifulSoup(r_internship, 'html.parser')

check_results = internship_soup.find_all('div', {'class': 'a'})

job_count_stats = internship_soup.find('div', {'class': 'st_p_top'})
job_count = job_count_stats.strong.text
job_salary_stats = internship_soup.find('div', {'class': 'st_p_bottom_salary'})
job_salary = job_salary_stats.strong.text


internship_message = ''
# internship_results = []
internship_flag = False

for result in check_results:
    if 'internship' in result.text.lower():
        internship_flag = True
    else:
        pass

if internship_flag:
    internship_message = f'\nInternship(s) found, check: https://www.adzuna.co.za/search?q=python%20developer&w=Cape%20Town%20Region%2C%20Western%20Cape\n' \
                         f'Current available Python-related jobs in CT: {job_count}\n' \
                         f'Average salary for a Python Developer in CT per year: {job_salary}'
else:
    internship_message = f'\nNo internship results found on Adzuna today.\n\n' \
                         f'Current available Python-related jobs in CT: {job_count}\n' \
                         f'Average salary for a Python Developer in CT per year: {job_salary}'
#
##############################################################

# Short joke

r_joke = requests.get('https://bestlifeonline.com/funny-short-jokes/').content

joke_soup = BeautifulSoup(r_joke, 'html.parser')

jokes = joke_soup.find_all('ol', {'class': 'ol1'})
joke_list = [joke.text.split('\n') for joke in jokes]
joke_message = random.choice(joke_list[0][1:-1])


###############################################################

# Relevant jobs - Removed Pnet website due to structure change, unable to scrape with BS.

indeed = 'https://www.indeed.co.za/jobs?q=python+developer&l=Cape+Town%2C+Western+Cape'
careers24 = 'https://www.careers24.com/jobs/kw-python-developer/m-true/'

r_indeed = requests.get(indeed).content
r_careers24 = requests.get(careers24).content

soup_indeed = BeautifulSoup(r_indeed, 'html.parser')
soup_careers24 = BeautifulSoup(r_careers24, 'html.parser')

indeed_desc = []
indeed_links = []

careers24_desc = []
careers24_links = []


for job in soup_indeed.find_all('a', {'target': '_blank'}):
    indeed_desc.append(job.text.replace('\n', ''))
    indeed_links.append('www.indeed.co.za' + (job['href']))

for job in soup_careers24.find_all('div', {'class': 'span6 job_search_content'}):
    careers24_desc.append(job.span.text)
    careers24_links.append('www.careers24.com' + (job.find('a')['href']))

top_selection = '\n\nMost relevant jobs from Indeed & Careers24:\n\n'

for i in range(len(indeed_desc)):

    if 'python' in indeed_desc[i].lower():
        top_selection += f'{indeed_desc[i]}\n{indeed_links[i]}\n\n\n'
    elif 'internship' in indeed_desc[i].lower():
        top_selection += f'{indeed_desc[i]}\n{indeed_links[i]}\n\n\n'

for i in range(len(careers24_desc)):

    if 'python' in careers24_desc[i].lower():
        top_selection += f'{careers24_desc[i]}\n{careers24_links[i]}\n\n\n'
    elif 'internship' in careers24_desc[i].lower():
        top_selection += f'{careers24_desc[i]}\n{careers24_links[i]}\n\n\n'


########################################################

# Local Covid statistics

r_covid = requests.get('https://www.worldometers.info/coronavirus/country/south-africa/').content

covid_soup = BeautifulSoup(r_covid, 'html.parser')

covid_stats = covid_soup.find_all('div', {'class': 'maincounter-number'})

covid_diff = covid_soup.find('div', {'class': 'news_body'})
covid_diff_msg = covid_diff.text.replace('\n', '').replace(' [source]', '.')

covid_list = [i.text.replace('\n', '').replace(' ', '') for i in covid_stats]

covid_message = f'\nSA Covid Stats:\n' \
                f'\nTotal Cases: {covid_list[0]}\n' \
                f'Total Deaths: {covid_list[1]}\n' \
                f'Total Recoveries: {covid_list[2]}\n' \
                f'{covid_diff_msg}'


###########################################################

# Build message and send mail

content = f'{issue_message}' \
          f'\n{morning_message}' \
          f'\n\nToday\'s joke:' \
          f'\n{joke_message}' \
          f'\n____' \
          f'{weather_message}' \
          f'\n\n###################' \
          f'{article_message}' \
          f'\n\n###################' \
          f'{covid_message}' \
          f'\n\n###################' \
          f'{internship_message}' \
          f'{top_selection}' \
          f'###################' \
          f'{inspirational_message}'

print(content)

s = smtplib.SMTP(host='smtp.gmail.com', port=587)

s.ehlo()
s.starttls()
s.login('your@email.here', 'password')

msg = MIMEMultipart()

msg['From'] = 'your@email.here'
msg['To'] = 'to@email.here'
msg['Subject'] = 'The Daily Rise'

msg.attach(MIMEText(content, 'plain'))
s.send_message(msg)
s.close()
