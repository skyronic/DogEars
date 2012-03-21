import sublime, sublime_plugin
import os

BOOKMARKS = []

class NewBookmarkCommand(sublime_plugin.TextCommand):
	def run(self, edit):
		sel = self.view.sel()

		if not len(sel) == 1:
			# Work only on single selections
			return

		if not sel[0].begin() == sel[0].end():
			# Only on single caret selections
			return

		point = sel[0].begin()

		self.fileName = self.view.file_name()
		self.row, self.col = self.view.rowcol(point)

		window = self.view.window()

		defaultString = os.path.basename(self.fileName) + " - "

		window.show_input_panel("Enter Bookmark Name: ", defaultString, self.on_bookmark_name_entered, None, None)

	def on_bookmark_name_entered(self, bookmarkName):
		print("Saving bookmark {0} as {1}-{2}:{3}".format(bookmarkName, self.fileName, self.row, self.col))

		bookmark = {}
		bookmark['fileName'] = self.fileName
		bookmark['row'] = self.row
		bookmark['col'] = self.col
		bookmark['name'] = bookmarkName
		BOOKMARKS.append(bookmark)

