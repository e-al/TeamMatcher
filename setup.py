try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

config = {
    'description': 'TeamMatcher is a project to help students find the teams/projects to work together',
    'author': 'Team20',
    'url': 'https://github.com/e-al/TeamMatcher',
    'download_url': 'https://github.com/e-al/TeamMatcher',
    'author_email': 'evchenk2@illinois.edu',
    'version': '0.1',
    'install_requires': ['nose', 'flask', 'flask-mysql','numpy','pandas','nltk','sklearn','scipy'],
    'packages': ['TeamMatcher'],
    'include_package_data': True,
    'scripts': [],
    'name': 'TeamMatcher'
}

setup(**config)
