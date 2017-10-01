from setuptools import setup, find_packages
setup(
	name="Gesso",
	description="Interactive CLI to bootstrap and automate creation of interactive systems.",
	version="0.1.0",
	url="https://github.com/machineeeee/gesso-python",
	author="Machineee",
	zip_safe=False,
	packages=find_packages(),
	package_data = { 'gesso': [ 'data/*' ] },
	install_requires = [
		'petname',
		'pexpect',
		'psutil',
		'netifaces',
		'portalocker',
                'watchdog',
                'tinydb',
                'tabulate'
	],
	entry_points = {
		'console_scripts': ['gesso=gesso.command_line:main'],
	},
)
