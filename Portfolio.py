import os
import requests

from Entry import Entry

ENV_SECRET_GITHUB = "SECRET_GITHUB"
SECRET_GITHUB = os.environ.get(ENV_SECRET_GITHUB)

GITHUB_ENDPOINT = "https://api.github.com"
API_VERSION = "application/vnd.github.v3+json"

HEADER_OAUTH = "OAUTH-TOKEN"
HEADER_ACCEPT = "Accept"

HEADERS = {HEADER_OAUTH: SECRET_GITHUB, HEADER_ACCEPT: API_VERSION}

class Portfolio:

	def __new__(cls, username):
		if SECRET_GITHUB == None:
			raise NameError(f"No OAuth token env variable found, please set ${ENV_SECRET_GITHUB} (editable inside Portfolio.py) to your OAuth token.")
		return super(Portfolio, cls).__new__(cls)

	def __init__(self, username):
		self.username = username
		self.repos = None
		self.entries = []
		self.fetchRepos()
		self.generateEntries()
		self.render()

	def render(self):
		for entry in self.entries:
			print(entry)

	def generateEntries(self):
		for repo in self.repos:
			if not repo["private"]:
				entry = self.generateEntry(repo)
				if entry != None:
					self.entries.append(self.generateEntry(repo))

	def fetchRepos(self):
		self.repos = get("/user/repos")

	def generateEntry(self, repo):
		owner = repo["owner"]["login"]
		name = repo["name"]
		contributors = get(f"/repos/{owner}/{name}/stats/contributors")
		userContributor = None
		userAdditions = 0
		userDeletions = 0
		totalAdditions = 0
		totalDeletions = 0
		totalCommits = 0
		for contributor in contributors:
			print(contributor["author"]["login"])
			additions = sum([week["a"] for week in contributor["weeks"]])
			deletions = sum([week["d"] for week in contributor["weeks"]])
			totalAdditions += additions
			totalDeletions += deletions
			totalCommits += contributor["total"]
			if contributor["author"]["login"] == self.username:
				print(":)")
				userContributor = contributor
				userAdditions = additions
				userDeletions = deletions

		entry = Entry(self.username, owner, name)
		if(userContributor != None):
			entry.setCommits(userContributor["total"])
			entry.setTotalCommits(totalCommits)
			entry.setAdditions(userAdditions)
			entry.setDeletions(userDeletions)
			entry.setTotalAdditions(totalAdditions)
			entry.setTotalDeletions(totalDeletions)
			return entry
		return None

def getFull(fullPath):
	if SECRET_GITHUB == None:
		raise NameError(f"No OAuth token env variable found, please set ${ENV_SECRET_GITHUB} (editable inside Portfolio.py) to your OAuth token.")
	return requests.get(fullPath, auth=(SECRET_GITHUB, "")).json()

def get(path):
	return getFull(f"{GITHUB_ENDPOINT}{path}")