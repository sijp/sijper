'''
main config file
globals should be declared here
'''
import usersaction
import postsaction

username="sijper"
password="walla!walla"

actionmodules={ "createuser" : usersaction.CreateUser ,
		"getuser" : usersaction.GetUser,
		"follow" : useraction.Follow,
		"unfollow" : useraction.Unfollow,
		"postmessage" : postsaction.PostMessage,
		"getfeed" : postaction.GetFeed,
		"getglobalfeed" : postaction.GetFeed }
