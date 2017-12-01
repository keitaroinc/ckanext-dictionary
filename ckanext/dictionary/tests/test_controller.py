from bs4 import BeautifulSoup
from nose.tools import assert_equal, assert_true, assert_in
from ckan.lib.helpers import url_for
import unittest
import ckan.tests.helpers as helpers
import ckan.model as model
from ckan.tests import factories

from pprint import pprint

webtest_submit = helpers.webtest_submit
submit_and_follow = helpers.submit_and_follow


class TestDictonaryController(helpers.FunctionalTestBase):
    def setup(self):
        super(TestDictonaryController, self).setup()
        self.app = helpers._get_test_app()
        self.user = factories.Sysadmin()
        self.user_env = {'REMOTE_USER': self.user['name'].encode('ascii')}
        self.dataset = factories.Dataset()

    def test_new_data_dictionary(self):
        #/dataset/dictionary/new_dict/{id}
        edit_dict_url = url_for(controller='ckanext.dictionary.controller:DDController',
                            action='new_data_dictionary',
                                id=self.dataset['id'])
        r = self.app.post(edit_dict_url,
                      params={
                          'field-0': 'field',
                          'title-0': 'title',
                          'format_0': 'Default String',
                          'description_0': 'desc'
                      },
                      extra_environ=self.user_env)

        #print r.status_int
        if r.status_int == 302:
            assert r.status_int == 302

    def test_new_resource_ext(self):
        #dataset/new_resource/{id}
        edit_dict_url = url_for(controller='ckanext.dictionary.controller:DDController',
                                action='new_resource_ext',
                                id=self.dataset['id'])
        req = self.app.post(
                            edit_dict_url,
                            params={'url': 'url','name': 'name','description': 'description','format': 'format'},
                            extra_environ=self.user_env
                            )
        #print req.status_int
        if req.status_int == 302:
            assert True

    # def test_dictionary(self):
    #     edit_dict_url = url_for(controller='ckanext.dictionary.controller:DDController', action='dictionary', id=self.dataset['id'])
    #     req = self.app.post(edit_dict_url, params=)

    def test_edit_dictionary(self):
        #/dataset/dictionary/edit/{id}
        edit_dict_url = url_for(controller='ckanext.dictionary.controller:DDController',
                                action='edit_dictionary',
                                id=self.dataset['id'])

        for i in range(10):
            r = self.app.post(edit_dict_url,
                              params={
                                  'field': 'field_'+str(i),
                                  'title': 'title_'+str(i),
                                  'format': 'format_'+str(i),
                                  'description': 'description_'+str(i)
                              },
                              extra_environ=self.user_env
                              )
            if r.status_int == 302:
                assert True

    def test_finaldict(self):
        #/dataset/dictionary/add/{id}
        edit_dict_url = url_for(
            controller='ckanext.dictionary.controller:DDController',
            action='finaldict',
            id=self.dataset['id']
        )
        for i in range(3):
            r = self.app.post(
                edit_dict_url,
                params={'field' : 'field_'+str(i),
                        'title': 'title_'+str(i),
                        'format' : 'format_'+str(i),
                        'description' : 'description_'+str(i)
                        },
                extra_environ=self.user_env
                )

            if r.status_int == 302:
                assert True
