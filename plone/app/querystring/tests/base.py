from zope.component import getGlobalSiteManager
from zope.configuration import xmlconfig
from plone.testing import Layer
from plone.app.testing import PLONE_FIXTURE
from plone.app.testing import PloneSandboxLayer
from plone.app.testing import IntegrationTesting, FunctionalTesting

from plone.registry.interfaces import IRegistry
from plone.registry.registry import Registry

# We are either using a version of Python that has the
# capabilities or the setup.py picked up unittest2.
try:
    import unittest2 as unittest
except ImportError:
    import unittest


class PloneAppQuerystring(PloneSandboxLayer):
    defaultBases = (PLONE_FIXTURE,)

    def setUpZope(self, app, configurationContext):
        import plone.app.querystring
        import plone.app.querystring.tests
        xmlconfig.file('configure.zcml',
                       plone.app.querystring,
                       context=configurationContext)

    def setUpPloneSite(self, portal):
        self.applyProfile(portal, 'Products.CMFPlone:testfixture')
        self.applyProfile(portal, 'plone.app.querystring:default')

PLONE_APP_QUERYSTRING_FIXTURE = PloneAppQuerystring()
PLONE_APP_QUERYSTRING_INTEGRATION_TESTING = IntegrationTesting(
    bases=(PLONE_APP_QUERYSTRING_FIXTURE,),
    name="PloneAppQuerystring:Integration")
PLONE_APP_QUERYSTRING_FUNCTIONAL_TESTING = FunctionalTesting(
    bases=(PLONE_APP_QUERYSTRING_FIXTURE,),
    name="PloneAppQuerystring:Functional")


class RegistryOnly(Layer):
    """A layer that contains only a plone.registry instance
    and nothing more."""

    def setUp(self):
        global_site_manager = getGlobalSiteManager()
        self.registry = Registry()
        global_site_manager.registerUtility(self.registry, IRegistry)

    def tearDown(self):
        global_site_manager = getGlobalSiteManager()
        global_site_manager.unregisterUtility(provided=IRegistry)

REGISTRY_ONLY_LAYER = RegistryOnly()
