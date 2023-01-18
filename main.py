import os

from pytz import timezone
from datetime import datetime

from leetcode_ranking import LeetCodeService
from github_utils import get_github_repo, upload_github_issue


if __name__ == "__main__":
    access_token = os.environ["MY_GITHUB_TOKEN"]
    repository_name = "leetcode"

    seoul_timezone = timezone("Asia/Seoul")
    today = datetime.now(seoul_timezone)
    today_date = today.strftime("%Y년 %m월 %d일")

    ranking = LeetCodeService().get_ranking("eunsour")

    issue_title = f"LeetCode Ranking - {today_date}"
    upload_contents = f"LeetCode Ranking : {format(ranking, ',')}등"
    repo = get_github_repo(access_token, repository_name)
    upload_github_issue(repo, issue_title, upload_contents)
    print("Upload Github Issue Success!")
