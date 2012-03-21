import sublime, sublime_plugin
import os
import string, random

def id_generator(size=5, chars=string.ascii_uppercase + string.digits):
	return ''.join(random.choice(chars) for x in range(size))


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
		self.point = point

		self.fileName = self.view.file_name()

		window = self.view.window()

		defaultString = os.path.basename(self.fileName) + " - "

		window.show_input_panel("Enter Bookmark Name: ", defaultString, self.on_bookmark_name_entered, None, None)

	def on_bookmark_name_entered(self, bookmarkName):
		print("Saving bookmark {0} as {1}-{2}:{3}".format(bookmarkName, self.fileName, self.row, self.col))

		# Create a unique ID for the bookmark
		key = id_generator()

		bookmark = {}
		bookmark['fileName'] = self.fileName
		bookmark['name'] = bookmarkName
		bookmark['key'] = key

		BOOKMARKS.append(bookmark)

		# Create a region to behave like a bookmark
		self.view.add_region('bookmark_' + key, sublime.Region(self.point, self.point), "", "bookmark", sublime.HIDDEN)

