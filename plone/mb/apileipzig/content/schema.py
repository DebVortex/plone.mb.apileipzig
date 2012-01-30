from five import grok
from zope import schema

from plone.directives import form, dexterity

class IMediaHandbook(form.Schema):
	"""
	"""
	title = schema.TextLine(
		title = u"Titel",
	) 

	description = schema.TextLine(
		title = u"Beschreibung",
	)

	cache_timeout = schema.Int(
        title = u"Cache Ablaufzeit",
        description = u"Definieren Sie hier die Zeit, wie lange die " +\
            "Unternehmen gespeichert werden sollen. Eine hohe Cachezeit " +\
            "verringert die Wartezeit, allerdings werden die Daten nicht " +\
            "aktualisiert, bis die Zeit abgelaufen ist.",
        default = 60,
	)