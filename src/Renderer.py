MAIN_FILENAME = "README.md"
TEMPLATE_LOCATION = "templates/"
RENDERED_LOCATION = "rendered/"
MAIN_LOCATION = ""

class Renderer:
	def __init__(self):
		self.filename = None 
		self.content = None
		self.templateIsMain = False 
		self.symbolMap = {}

	def loadTemplate(self, filepath):
		with open(filepath, "r") as templateFile:
			self.content = templateFile.readlines()
		self.filename = filepath.split("/")[-1]
		self.templateIsMain = self.filename == MAIN_FILENAME

	def addSymbol(self, name, value):
		self.symbolMap[name] = value
	def render(self):
		renderedContent = ""
		for line in self.content:
			listSymbols = []
			for symbol, value in self.symbolMap.items():
				if symbol in line and isinstance(value, list):
					listSymbols.append(symbol)
				else:
					line = line.replace("{{"+symbol+"}}", str(self.symbolMap[symbol]))
			
			if len(listSymbols) > 0:
				contentRow = line
				line = ""
				for i in range(len(self.symbolMap[listSymbols[0]])):
					renderedRow = contentRow
					for symbol in listSymbols:
						renderedRow = renderedRow.replace("{{"+symbol+"}}", str(self.symbolMap[symbol][i]))
					line += renderedRow + "\n"
			
			if not line.endswith("\n"):
				line += "\n"
			renderedContent += line

		self.saveRendering(renderedContent)

	def saveRendering(self, rendering):
		if self.templateIsMain:
			outputFilepath = MAIN_LOCATION + self.filename
		else:
			outputFilepath = RENDERED_LOCATION + self.filename
		with open(outputFilepath, "w") as renderedFile:
			renderedFile.write(rendering)

	def renderFile(self, filepath):
		self.loadTemplate(filepath)
		self.render()