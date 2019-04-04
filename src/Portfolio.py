import os
import requests

from Renderer import Renderer, TEMPLATE_LOCATION


ENV_SECRET_GITHUB = "SECRET_GITHUB"
SECRET_GITHUB = os.environ.get(ENV_SECRET_GITHUB)

GITHUB_ENDPOINT = "https://api.github.com"
API_VERSION = "application/vnd.github.v3+json"

HEADER_OAUTH = "OAUTH-TOKEN"
HEADER_ACCEPT = "Accept"

SYMBOL_USERNAME = "username"
SYMBOL_REPO_OWNER = "repoOwner"
SYMBOL_REPO_NAME = "repoName"
SYMBOL_REPO_URL = "repoUrl"
SYMBOL_COMMITS = "commits"
SYMBOL_ADDITIONS = "additions"
SYMBOL_DELETIONS = "deletions"
SYMBOL_TOTAL_COMMITS = "totalCommits"
SYMBOL_TOTAL_ADDITIONS = "totalAdditions"
SYMBOL_TOTAL_DELETIONS = "totalDeletions"


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
		self.sortEntries(SYMBOL_ADDITIONS, reverse = True)
		self.render()

	def render(self):
		renderer = Renderer()
		self.setupRenderer(renderer)
		for filename in os.listdir(TEMPLATE_LOCATION):
			print(f"Rendering {filename}...")
			renderer.renderFile(TEMPLATE_LOCATION + filename)

	def generateEntries(self):
		for repo in self.repos:
			if not repo["private"]:
				entry = self.generateEntry(repo)
				if entry != None:
					self.entries.append(entry)

	def sortEntries(self, symbol, reverse = False):
		self.entries.sort(key = lambda entry : entry.get(symbol))
		if reverse:
			self.entries = self.entries[::-1]

	def fetchRepos(self):
		print("Fetching repository data...")
		self.repos = get("/user/repos")

	def generateEntry(self, repo):
		entry = {}
		entry[SYMBOL_REPO_OWNER] = repo["owner"]["login"]
		entry[SYMBOL_REPO_NAME] = repo["name"]
		entry[SYMBOL_REPO_URL] = f"https://github.com/{entry[SYMBOL_REPO_OWNER]}/{entry[SYMBOL_REPO_NAME]}"

		print(f"Fetching contributor data for {entry[SYMBOL_REPO_NAME]}")

		contributors = get(f"/repos/{entry[SYMBOL_REPO_OWNER]}/{entry[SYMBOL_REPO_NAME]}/stats/contributors")
		totalAdditions = 0
		totalDeletions = 0
		totalCommits = 0
		for contributor in contributors:
			additions = sum([week["a"] for week in contributor["weeks"]])
			deletions = sum([week["d"] for week in contributor["weeks"]])
			totalAdditions += additions
			totalDeletions += deletions
			totalCommits += contributor["total"]
			if contributor["author"]["login"] == self.username:
				entry[SYMBOL_COMMITS] = contributor["total"]
				entry[SYMBOL_ADDITIONS] = additions
				entry[SYMBOL_DELETIONS] = deletions

		entry[SYMBOL_TOTAL_COMMITS] = totalCommits
		entry[SYMBOL_TOTAL_ADDITIONS] = totalAdditions
		entry[SYMBOL_TOTAL_DELETIONS] = totalDeletions
		
		if(entry.get(SYMBOL_COMMITS) != None):
			return entry
		return None

	def setupRenderer(self, renderer):
		renderer.addSymbol(SYMBOL_USERNAME, self.username)
		renderer.addSymbol(SYMBOL_REPO_OWNER, [entry.get(SYMBOL_REPO_OWNER) for entry in self.entries])
		renderer.addSymbol(SYMBOL_REPO_NAME, [entry.get(SYMBOL_REPO_NAME) for entry in self.entries])
		renderer.addSymbol(SYMBOL_COMMITS, [entry.get(SYMBOL_COMMITS) for entry in self.entries])
		renderer.addSymbol(SYMBOL_ADDITIONS, [entry.get(SYMBOL_ADDITIONS) for entry in self.entries])
		renderer.addSymbol(SYMBOL_DELETIONS, [entry.get(SYMBOL_DELETIONS) for entry in self.entries])
		renderer.addSymbol(SYMBOL_TOTAL_COMMITS, [entry.get(SYMBOL_TOTAL_COMMITS) for entry in self.entries])
		renderer.addSymbol(SYMBOL_TOTAL_ADDITIONS, [entry.get(SYMBOL_TOTAL_ADDITIONS) for entry in self.entries])
		renderer.addSymbol(SYMBOL_TOTAL_DELETIONS, [entry.get(SYMBOL_TOTAL_DELETIONS) for entry in self.entries])
		renderer.addSymbol(SYMBOL_REPO_URL, [entry.get(SYMBOL_REPO_URL) for entry in self.entries])

def getFull(fullPath):
	if SECRET_GITHUB == None:
		raise NameError(f"No OAuth token env variable found, please set ${ENV_SECRET_GITHUB} (editable inside Portfolio.py) to your OAuth token.")
	return requests.get(fullPath, auth=(SECRET_GITHUB, "")).json()

def get(path):
	return getFull(f"{GITHUB_ENDPOINT}{path}")