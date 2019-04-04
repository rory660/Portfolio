class Entry:
	def __init__(self, username, owner, repository):
		self.username = username
		self.owner = owner
		self.repository = repository
		self.commits = None
		self.additions = None
		self.deletions = None
		self.totalAdditions = None
		self.totalDeletions = None
		self.totalCommits = None

	def __str__(self):
		return f"<Entry username = {self.username}, owner = {self.owner}, repository = {self.repository}, commits = {self.commits}/{self.totalCommits}, additions = {self.additions}/{self.totalAdditions}, deletions = {self.deletions}/{self.totalDeletions}>"

	def setCommits(self, commits):
		self.commits = commits

	def setAdditions(self, additions):
		self.additions = additions

	def setDeletions(self, deletions):
		self.deletions = deletions

	def setTotalCommits(self, totalCommits):
		self.totalCommits = totalCommits

	def setTotalAdditions(self, totalAdditions):
		self.totalAdditions = totalAdditions

	def setTotalDeletions(self, totalDeletions):
		self.totalDeletions = totalDeletions

	def getOwner(self):
		return self.owner

	def getRepository(self):
		return self.repository

	def getCommits(self):
		return self.commits

	def getAdditions(self):
		return self.additions

	def getDeletions(self):
		return self.deletions

	def getTotalCommits(self):
		return self.totalCommits

	def getTotalAdditions(self):
		return self.totalAdditions

	def getTotalDeletions(self):
		return self.totalDeletions

