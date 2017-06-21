from setuptools import setup, find_packages
setup(
	name="builder",
	description="Builder",
	version="0.0.1",
	url="https://github.com/buildernetwork/builder-python",
	author="Builder Network",
	zip_safe=False,
	packages=find_packages(),
	package_data = { 'builder': [ 'data/*', 'data/models/devices/*.yaml' ] },
        #data_files = [('data/models/devices', [ '*.yaml' ])],
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
		'console_scripts': ['builder=builder.command_line:main'],
	},
)
