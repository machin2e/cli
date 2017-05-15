from setuptools import setup, find_packages
setup(
	name="builder",
	description="Builder",
	version="0.0.1",
	url="https://github.com/mokogobo/builder",
	author="Builder Network",
	zip_safe=False,
	packages=find_packages(),
	install_requires = [
		'petname',
		'pexpect',
		'psutil',
		'netifaces',
		'portalocker'
	],
	entry_points = {
		'console_scripts': ['builder=builder.command_line:main'],
	},
)
