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
		"follow" : usersaction.Follow,
		"unfollow" : usersaction.Unfollow,
		"getfollowing" : usersaction.GetFollowing,
		"postmessage" : postsaction.PostMessage,
		"getfeed" : postsaction.GetFeed,
		"getglobalfeed" : postsaction.GetFeed }
