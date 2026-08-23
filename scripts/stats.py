import os
import requests

GITHUB_TOKEN = os.environ.get("GITHUB_TOKEN")

QUERY = """
{
  viewer {
    contributionsCollection {
      contributionCalendar {
        totalContributions
      }
    }
  }
}
"""


def fetch_stats():
    headers = {"Authorization": f"Bearer {GITHUB_TOKEN}"}

    response = requests.post(
        "https://api.github.com/graphql", json={"query": QUERY}, headers=headers
    )

    return response.json()


def generate_svg(data):
    total = data["data"]["viewer"]["contributionsCollection"]["contributionCalendar"][
        "totalContributions"
    ]

    svg = f"""
    <svg xmlns="http://www.w3.org/2000/svg" width="400" height="120">
        <rect width="100%" height="100%" fill="black"/>
        <text x="20" y="60" fill="#00ff88"
              font-size="24"
              font-family="monospace">
            Total Contributions: {total}
        </text>
    </svg>
    """

    with open("assets/stats.svg", "w") as f:
        f.write(svg)


if __name__ == "__main__":
    data = fetch_stats()
    generate_svg(data)
