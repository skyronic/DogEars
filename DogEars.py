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
		self.view.add_regions('dogears_' + key, [s for s in self.view.sel()], "", "bookmark")

		print("Saving bookmark {0} at key {1}".format(bookmarkName, key))


class BrowseBookmarksCommand(sublime_plugin.TextCommand):
	def run(self, edit):
		bookmarkOpts = []
		self.panelKeys = []

		baseName = os.path.basename(self.view.file_name())

		for key, val in BOOKMARKS.iteritems():
			if baseName == val['baseName']:
				bookmarkOpts.append(val['name'])
				self.panelKeys.append(key)

		window = self.view.window()

		window.show_quick_panel(bookmarkOpts, self.on_bookmark_selected)

	def on_bookmark_selected(self, idx):

		if(idx == -1):
			print("No bookmark selected. Returning ")
			return

		# Get the key for the bookmark
		key = self.panelKeys[idx]

		# Retrieve the region for the bookmark
		bmRegion = self.view.get_regions("dogears_" + key)

		if len(bmRegion) == 0:
			return

		self.view.run_command("select_all_bookmarks", {'name':"dogears_" + key})



