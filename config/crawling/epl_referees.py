from fake_useragent import UserAgent
from urllib.request import Request, urlopen
import csv, datetime, argparse
from bs4 import BeautifulSoup

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
        
    

def main(matchWeek):
        matchWeekReq = Request(f'https://www.premierleague.com/matchweek/{matchWeek}/blog?match=true')
        matchWeekReq.add_header('User-Agent', ua.random)
        matchWeekDoc = urlopen(matchWeekReq).read().decode('utf8')
        soup = BeautifulSoup(matchWeekDoc, 'html.parser')
        matchIdList= list(m.attrs['data-id'] for m in soup.select("a.matchAbridged"))
        print(matchIdList)
        
        for i in matchIdList:
                match_req = Request(f'https://www.premierleague.com/match/{i}')
                match_req.add_header('User-Agent', ua.random)
                match_doc = urlopen(match_req).read().decode('utf8')
                
                soup = BeautifulSoup(match_doc, 'html.parser')
                
                teamName = list(t.text for t in soup.select("div.team span.long"))
                ref = soup.find(class_="referee")
                if ref is not None:
                        ref = ref.text.strip()
                date = datetime.datetime.fromtimestamp(int(soup.find(class_="matchDate")['data-kickoff'][:-3])).strftime('%d/%m/%Y')
                season = season_from_date(date)
                fulltime = soup.find(class_="score fullTime").text.split('-')
                halftime = soup.select("div.halfTime")[0].contents[2].strip().split('-')
                # res = soup.select("tbody.matchCentreStatsContainer")

                print(teamName + [ref, date, season] +  fulltime +  halftime)
                # print(res)        

if __name__ == '__main__':
        matchWeek = int(args.MatchWeek)
        main(matchWeek + 7830)                
        print('Finish!')



    
