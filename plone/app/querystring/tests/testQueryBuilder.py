from zope.component import getMultiAdapter
from plone.app.testing import TEST_USER_NAME, TEST_USER_ID
from plone.app.testing import login, setRoles

from .base import unittest
from .base import PLONE_APP_QUERYSTRING_FUNCTIONAL_TESTING


class TestQuerybuilderView(unittest.TestCase):
    layer = PLONE_APP_QUERYSTRING_FUNCTIONAL_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        self.request = self.layer['request']

        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        login(self.portal, TEST_USER_NAME)

        self.portal.invokeFactory("Folder", 'folder', title='Folder')
        self.portal.invokeFactory("Document",
                                  "collectionstestpage",
                                  title="Collectionstestpage")
        testpage = self.portal['collectionstestpage']
        self.portal.portal_workflow.doActionFor(testpage, 'publish')
        self.query = [{
            'i': 'Title',
            'o': 'plone.app.querystring.operation.string.is',
            'v': 'Collectionstestpage',
        }]

    @property
    def querybuilder(self):
        return getMultiAdapter((self.portal, self.request),
                               name='querybuilderresults')

    def testQueryBuilderQuery(self):
        results = self.querybuilder(query=self.query)
        self.assertEqual(results[0].Title(), "Collectionstestpage")

    def testQueryBuilderHTML(self):
        results = self.querybuilder.html_results(self.query)
        self.assertTrue('Collectionstestpage' in results)

    def testGettingConfiguration(self):
        res = self.portal.folder.restrictedTraverse('@@querybuildernumberofresults')
        res(self.query)

    def testQueryBuilderNumberOfResults(self):
        results = self.querybuilder.number_of_results(self.query)
        numeric = int(results.split(' ')[0])
        self.assertEqual(numeric, 1)

    def testQueryBuilderNumberOfResultsView(self):
        res = self.portal.folder.restrictedTraverse('@@querybuildernumberofresults')
        length_of_results = res.browserDefault(None)[0](self.query)
        # apparently brower travelsal is different from the traversal we get
        # from restrictedTraverse. This did hurt a bit.
        numeric = int(length_of_results.split(' ')[0])
        self.assertEqual(numeric, 1)


class TestConfigurationFetcher(unittest.TestCase):
    layer = PLONE_APP_QUERYSTRING_FUNCTIONAL_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        login(self.portal, TEST_USER_NAME)
        self.portal.invokeFactory("Folder", 'folder', title='Folder')

    def testGettingJSONConfiguration(self):
        self.portal.folder.restrictedTraverse('@@querybuilderjsonconfig')()
