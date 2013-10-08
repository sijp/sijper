sijper
======

basic microblogging project

As part of a job interview


HTTP API:
-----------

All parameters are sent via HTTP Post. The "action" parameter defines the needed action to be made on the server. The rest of the parameters should match the class derived from AbstractAction.

* action=createuser: creates a new user in the system
	+ uname=<New User Name>
* action=follow: make user with id `follower` follow user with id `followee`
	+ follower=<User ID>
	+ followee=<Targeted User ID>
