import os
import base64

from typing import List

from utils import dateutils
from utils.logger import info
from service.leetcode import LeetCodeService
from service.github import GitHubService


GITHUB_API_TOKEN = os.environ["MY_GITHUB_TOKEN"]
GITHUB_API_RAW_BASE_URL = "https://raw.githubusercontent.com"
LEETCODE_RANKING_CSV_PATH = "outputs/leetcode_ranking.csv"


class Ranking:
    def __init__(self, epoch_ms: int, ranking: int) -> None:
        self.epoch_ms = epoch_ms
        self.ranking = ranking

    def __str__(self) -> str:
        return f"Ranking({dateutils.epoch_ms_to_date_str(self.epoch_ms)},{self.ranking})"


class LeetCodeRankingUpload:
    def __init__(self) -> None:
        self.github_service = GitHubService(GITHUB_API_TOKEN)
        self.leetcode_service = LeetCodeService()
        self.LEETCODE_RANKING_CSV_PATH = "analysis/output/leetcode_rankings.csv"

    def run(self) -> None:
        rankings_from_github: List[Ranking] = self.get_rankings_from_github()
        ranking_from_leetcode: Ranking = Ranking(dateutils.get_epoch_ms(), self.leetcode_service.get_ranking("eunsour"))
        latest_rankings: List[Ranking] = rankings_from_github + [ranking_from_leetcode]

        issue_title = f"LeetCode Ranking - {dateutils.get_kst_today()}"
        upload_contents = f"LeetCode Ranking : {format(ranking_from_leetcode.ranking, ',')}등"

        repo = self.github_service.get_github_repo("leetcode")
        self.upload_rankings_csv(latest_rankings)
        self.github_service.upload_github_issue(repo, issue_title, upload_contents)

    def get_rankings_from_github(self) -> List[Ranking]:
        content: bytes = self.github_service.get_raw_content(
            owner="eunsour",
            repo="leetcode",
            file_path=LEETCODE_RANKING_CSV_PATH,
            branch="master",
        )
        return [
            Ranking(*map(int, line.split(",")))
            for line in filter(lambda x: len(x) > 0, content.decode(encoding="ascii").split("\n"))
        ]

    def upload_rankings_csv(self, sorted_rankings: List[Ranking]) -> str:
        return self.github_service.upload_file(
            owner="eunsour",
            repo="leetcode",
            file_path=LEETCODE_RANKING_CSV_PATH,
            base64content=base64.b64encode(
                "\n".join(map(lambda x: f"{x.epoch_ms},{x.ranking}", sorted_rankings)).encode(encoding="ascii")
            ).decode("ascii"),
        )


if __name__ == "__main__":
    LeetCodeRankingUpload().run()
    info("Upload Github Issue Success!")
