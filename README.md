Pollstagram
===========

An awesome project.

## Issues ##

Some security flaws I've inadvertently created:

*	Secret keys in `.ebextensions/pollstagram.config` on GitHub
	*	Need to untrack this file and remove history from GitHub
*	Created rule for DB instance `rds-awseb-e-fyxfkvfm4e-stack-awsebrdsdbsecuritygroup-1iwzee8613wfp-ztz9` which allows connection from any IP address
	*	Need to use SSL authentication instead
	
TODO:

*	Need git branch/workflow to hold files like `local_settings.py` so this can be shared across team without being deployed to Amazon Beanstalk.
*	Organize setting files in a more logical/coherent manner
