import os
import sys
import pygit2
import util

def clone_github_repository(username, repository, clone_dir_path=None):

	if clone_dir_path == None:
		clone_dir_path = '%s/%s' % (util.get_gesso_dir(), 'devices')
	
	remote_repository_uri = 'https://github.com/%s/%s' % (username, repository)
	local_repository_clone_path = '%s/%s/%s' % (clone_dir_path, username, repository)
	
	"""
	user_path = '%s/%s' % (clone_dir_path, username)
	if not os.path.exists(user_path):
	    os.makedirs(user_path)
	"""
	create_user_directory(username)
	
	#pygit2.clone_repository(remote_repository_uri, local_repository_clone_path, bare=False)
	pygit2.clone_repository(remote_repository_uri, local_repository_clone_path, bare=False)

def create_user_directory(username, root_path=util.get_gesso_dir()):
	if not os.path.exists(root_path):
	    os.makedirs('%s/.devices/%s' % (root_path, username))

if __name__ == "__main__":
	username = sys.argv[1].split('/')[0] # 'machineeeee'
	repository = sys.argv[1].split('/')[1] # 'raspberry-pi-3'

	print('Cloning %s/%s to %s/%s/%s' % (username, repository, '.packages', username, repository))
	create_packages_directory()
	clone_github_repository(username, repository, '%s/%s' % (os.getcwdu(), '.packages'))

	# TODO: Index downloaded packages (or infer from git repositories)
	# TODO: Index packages that are actually used, and only store those in the project's YAML config
