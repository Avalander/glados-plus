import glados


class Movie(glados.Module):
	def get_help_list(self):
		return [

		]

	@glados.Module.commands('release')
	def release(self, message, content):
		pass
