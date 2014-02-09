sijper
======

basic microblogging project - a fully ReSTful web server, that supports basic microblogging actions.

System Structure:
-----------------
The system relies on the existence of Python 2.7.4 and a MySQL Server. For a nice drawing please
see the structure.svg or structure.pdf files.

##dbhandler.py
This module supplies basic functions to work with the MySQL Server.
It is responsible to create,close or execute SQL Queries via MySQLdb (Python Driver)
It also supplies the cleanDB and setupDB functions, to reset the Database.

##abstractaction.AbstractAction
This is a class which, every other action (createuser,follow...) must subclass
in order to bring the system the proper functionality in order to process the action.
A basic action should implement the execute and getDict method.
The constructor signature must match exactly the signature that is required by the http post request (same parameters names).

###execute:
executes an SQL Query that represents the action. Usually one should implement it
to return the SQL String and decorate the function with SqlExecutor which is also
supplied by this module.

###getDict:
Should call execute and transform its result to a python structure (lists and tuples)
that could be later be transformed to JSON via the json module.
Usually, as SqlExecutor returns a list of tuples (each represents a single record),
it should be processed into a Post or a User object (or a list of these).

##postsaction.py and usersaction.py
In these modules, all needed subclasses of abstractaction.AbstractAction are made,
each represents a proper action.

##sijperserver.SijperServer
This class is a subclass of threading.Thread. It runs in its own thread
and accepts tcp connections.
Once a connection is made a clientthread.ClientThread is created to handle the Client.

##clientthread.ClientThread
Gets a socket, and reads the HTTP POST request.
once read and processed, an appropriate Action object is created (subclass of AbstractAction)
and executed via its getJSON method.
Once done, the json result is sent back to the client via HTTP POST response.

HTTP API:
---------

All parameters are sent via HTTP Post. The "action" parameter defines the needed action to be made on the server. The rest of the parameters should match the class derived from AbstractAction.

* action=createuser: creates a new user in the system
	+ uname=[New User Name]
* action=follow: make user with id `follower` follow user with id `followee`
	+ follower=[User ID]
	+ followee=[Targeted User ID]
* action=unfollow: make user with id `follower` unfollow user with id `followee`
	+ follower=[User ID]
	+ followee=[Targeted User ID]
* action=postmessage: post a message with `msgtext` on behalf of `userid`
	+ userid=[User ID]
	+ msgtext=[Post Text]
* action=getfeed: returns the feed the user with ID `userid` is following. If fromid is supplied, it will return only messages with PostID>`fromid`
	+ userid=[User ID]
	+ fromid=[begining from id]
* action=getglobalfeed: returns all messages. If fromid is supplied, it will return only messages with PostID>`fromid`
	+ fromid=[begining from id]

