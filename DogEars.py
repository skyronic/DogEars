import sublime, sublime_plugin
import os
import string, random

def id_generator(size=5, chars=string.ascii_uppercase + string.digits):
	return ''.join(random.choice(chars) for x in range(size))


BOOKMARKS = {}

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
		# Create a unique ID for the bookmark
		key = id_generator()

		bookmark = {}
		bookmark['fileName'] = self.fileName
		bookmark['baseName'] = os.path.basename(self.fileName)
		bookmark['name'] = bookmarkName

		BOOKMARKS[key] = bookmark

		# Create a region to behave like a bookmark
		self.view.add_region('dogears_' + key, sublime.Region(self.point, self.point), "", "bookmark", sublime.HIDDEN)

		print("Saving bookmark {0} at key {1}".format(bookmarkName, key))

class DogEarListener(sublime_plugin.EventListener):
	def on_close(view):
		# Get the filename, and the base path
		baseName = os.path.basename(view.file_name())

		viewKeys = []

		# Iterate through all the bookmarks and see if any bookmarks match the keys
		for key, value in BOOKMARKS:
			if value['baseName'] == baseName:
				viewKey.append(key)

		for key in viewKeys:
			region = view.get_regions("dogears_" + key)

			if len(region) === 0:
				# This means that the bookmark must've been deleted or something
				pass
