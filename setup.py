# $Id: setup.py,v 1.2 2008/11/30 03:44:04 asc Exp $

# http://peak.telecommunity.com/DevCenter/setuptools
# http://ianbicking.org/docs/setuptools-presentation/

try:
    from setuptools import setup, find_packages
except:
    from ez_setup import use_setuptools
    use_setuptools()
    from setuptools import setup, find_packages

readme = file('README','rb').read()

local__name = 'pwmarker'
local__version = '1.0.1'
local__url = 'http://www.aaronland.info/python/%s' % local__name
local__download = '%s/%s-%s.tar.gz' % (local__url, local__name, local__version)

setup(
    name = local__name,
    version = local__version,

    packages=find_packages(exclude=["*.tests", "*.tests.*", "tests.*", "tests"]),
    exclude_package_data={'':["examples", "README", "ez_setup*"]},

    # TO DO: proper packages for ModestMaps...
    install_requires = ['pycairo', 'PIL'],
    dependency_links = ['http://www.pythonware.com/products/pil/', 'http://www.aaronland.info/python/packageindex/'],

    author = "Aaron Straup Cope",
    author_email = "aaron@aaronland.net",
    description = "packages to generate pinwin-style markers with perspective shadows.",
    long_description=readme,
    
    license = "BSD",
    keywords = "",
    url = local__url,
    download_url = local__download,
    
    # Uncomment when you need to sanity check the
    # stuff that actually gets installed...
    zip_safe=False    
    )
