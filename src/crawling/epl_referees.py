import json
from fake_useragent import UserAgent
from urllib.request import Request, urlopen
import csv, datetime, argparse
from bs4 import BeautifulSoup
from statistic_model import MatchStatistic

# Initialize User Agent
ua = UserAgent()

# Initialize parser
parser = argparse.ArgumentParser()
 
# Adding optional argument
parser.add_argument("-mw", "--MatchWeek", help = "MatchWeek")

# Read arguments from command line
args = parser.parse_args()

def write_file(data, file_output_path, is_append = False):
        print('Writing to file...')
        if len(data) <= 0:
                return
        mode = 'a' if is_append else 'w'
        with open(file_output_path, mode) as f:
                writer = csv.writer(f, delimiter=',', quoting=csv.QUOTE_ALL)
                writer.writerow(data)
                
def season_from_date(date):
    _, month, year = date.split('/')
    return f'{year}-{int(year)-1999}' if int(month) > 7 else f'{int(year)-1}-{int(year)-2000}'

def manipulateJsonStats(data):
        match_stats = MatchStatistic(data)
        match_stats.get_stats(data)
        
        print(vars(match_stats))
        
        
        
    

def main(matchWeek):
        matchWeekReq = Request(f'https://www.premierleague.com/matchweek/{matchWeek}/blog?match=true')
        matchWeekReq.add_header('User-Agent', ua.random)
        matchWeekDoc = urlopen(matchWeekReq).read().decode('utf8')
        soup = BeautifulSoup(matchWeekDoc, 'html.parser')
        matchIdList= list(m.attrs['href'] for m in soup.select("a.match-fixture--abridged"))
        print(matchIdList)
        
        for i in matchIdList[0:1]:
                # match_req = Request(f'https://www.premierleague.com{i}')
                # match_req.add_header('User-Agent', ua.random)
                # match_doc = urlopen(match_req).read().decode('utf8')
                
                # soup = BeautifulSoup(match_doc, 'html.parser')
                
                # teamName = list(t.text for t in soup.findAll(class_="mc-summary__team-name u-hide-phablet"))
                # day, *left, ref = list(t.text.strip() for t in soup.findAll(class_="mc-summary__info"))
                # # if ref is not None:
                # #         ref = ref.text.strip()
                
                # fulltime = soup.find(class_="mc-summary__score js-mc-score").text.split('-')
                # halftime = soup.select("span.js-mc-half-time-score")[0].text.split('-')
                # date = datetime.datetime.strptime(day, '%a %d %b %Y').strftime('%d/%m/%Y')
                # season = season_from_date(date)

                # print(teamName + [date, ref.split(': ')[-1], season] +  fulltime +  halftime)
                
                match_req = Request(f'https://footballapi.pulselive.com/football/stats{i}')
                match_req.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.75 Safari/537.36')
                match_req.add_header('Origin', 'https://www.premierleague.com')
                match_req.add_header('Content-Type', 'application/x-www-form-urlencoded; charset=UTF-8'),
                match_req.add_header('Referer', 'https://www.premierleague.com//clubs/1/Arsenal/squad?se=79')
                match_stats = json.loads(urlopen(match_req).read().decode('utf8'))
                manipulateJsonStats(match_stats)
        

if __name__ == '__main__':
        matchWeek = int(args.MatchWeek)
        main(matchWeek + 12268)                
        print('Finish!')



    
