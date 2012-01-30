from five import grok
from zope import schema

from plone.app.registry.browser import controlpanel

from plone.directives import form, dexterity

class IAPILeipzigSettings(form.Schema):
	"""
	"""
	api_key = schema.TextLine(
		title = u"API Key",
		description = u"Gib hier deinen API Key ein.",
	) 


class APILeipzigEditForm(controlpanel.RegistryEditForm):
    schema = IAPILeipzigSettings
    label = u"API Leipzig"
    description = u""

    def updateFields(self):
        super(APILeipzigEditForm, self).updateFields()

    def updateWidgets(self):
        super(APILeipzigEditForm, self).updateWidgets()

class APILeipzigControlPanel(controlpanel.ControlPanelFormWrapper):
    form = APILeipzigEditForm 