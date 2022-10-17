# -*- coding: utf-8 -*-

from setuptools import setup


with open('README.md') as f:
    readme = f.read()

with open('LICENSE') as f:
    license_jat = f.read()

setup(
    name='JiraAutomatedTasks',
    version='0.1.0',
    description='Package to do perform some automated task in Liferay Jira',
    long_description=readme,
    author='David Gutierrez Mesa',
    author_email='david.gutierrez@liferay.com',
    url='https://github.com/david-gutierrez-mesa/JiraAutomatedTasks',
    license=license_jat,
    packages=['liferay']
)
