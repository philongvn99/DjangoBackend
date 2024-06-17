import argparse
import csv
import json
from urllib.request import Request, urlopen

from bs4 import BeautifulSoup
from fake_useragent import UserAgent
from statistic_model import MatchStatistic

# Initialize User Agent
ua = UserAgent()

# Initialize parser
parser = argparse.ArgumentParser()

# Adding optional argument
parser.add_argument("-mw", "--MatchWeek", help="MatchWeek")

# Read arguments from command line
args = parser.parse_args()


def write_file(data, file_output_path, is_append=False):
    print("Writing to file...")
    if len(data) <= 0:
        return
    mode = "a" if is_append else "w"
    with open(file_output_path, mode) as f:
        writer = csv.writer(f, delimiter=",", quoting=csv.QUOTE_ALL)
        writer.writerow(data)


def manipulateStats(data: MatchStatistic, ref: str):
    return [
        data.match.season,
        data.match.kickoff,
        data.team1.info.shortName,
        data.team2.info.shortName,
        data.team1.stats.ftg,
        data.team2.stats.ftg,
        data.team1.stats.htg,
        data.team2.stats.htg,
        ref,
        data.team1.stats.sh,
        data.team2.stats.sh,
        data.team1.stats.sot,
        data.team2.stats.sot,
        data.team1.stats.co,
        data.team2.stats.co,
        data.team1.stats.fo,
        data.team2.stats.fo,
        data.team1.stats.yc,
        data.team2.stats.yc,
        data.team1.stats.rc,
        data.team2.stats.rc,
    ]


def main(matchWeek):
    matchWeekReq = Request(
        f"https://www.premierleague.com/matchweek/{matchWeek}/blog?match=true"
    )
    matchWeekReq.add_header("User-Agent", ua.random)
    matchWeekDoc = urlopen(matchWeekReq).read().decode("utf8")
    soup = BeautifulSoup(matchWeekDoc, "html.parser")
    matchIdList = list(
        m.attrs["href"] for m in soup.select("a.match-fixture--abridged")
    )
    print(matchIdList)

    filename = "src/crawling/match_stats.csv"
    fields = [
        "Season",
        "Date",
        "HomeTeam",
        "AwayTeam",
        "FTHG",
        "FTAG",
        "HTHG",
        "HTAG",
        "Referee",
        "HS",
        "AS",
        "HST",
        "AST",
        "HC",
        "AC",
        "HF",
        "AF",
        "HY",
        "AY",
        "HR",
        "AR",
    ]
    # writing to csv file
    with open(filename, "w") as csvfile:
        # creating a csv dict writer object
        writer = csv.writer(csvfile, delimiter=",")
        writer.writerow(fields)

        # writing data rows

        for i in matchIdList:
            match_req = Request(f"https://www.premierleague.com{i}")
            match_req.add_header("User-Agent", ua.random)
            match_doc = urlopen(match_req).read().decode("utf8")

            soup = BeautifulSoup(match_doc, "html.parser")

            ref = list(t.text.strip() for t in soup.findAll(class_="mc-summary__info"))[
                -1
            ].split(": ")[-1]

            match_req = Request(f"https://footballapi.pulselive.com/football/stats{i}")
            match_req.add_header(
                "User-Agent",
                "Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.75 Safari/537.36",
            )
            match_req.add_header("Origin", "https://www.premierleague.com")
            match_req.add_header(
                "Content-Type", "application/x-www-form-urlencoded; charset=UTF-8"
            ),
            match_req.add_header(
                "Referer", "https://www.premierleague.com//clubs/1/Arsenal/squad?se=79"
            )
            match_info = json.loads(urlopen(match_req).read().decode("utf8"))

            match_stats = MatchStatistic(match_info)
            match_stats.get_stats(match_info)

            writer.writerow(manipulateStats(match_stats, ref))


if __name__ == "__main__":
    matchWeek = int(args.MatchWeek)
    main(matchWeek + 12268)
    print("Finish!")
