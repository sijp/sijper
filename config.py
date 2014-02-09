####################
# main config file #
####################

#########################
# module import section #
#########################
import usersaction
import postsaction


###########
# globals #
###########

#databse username
username="sijper"

#database password
password="walla!walla"

#dictionary mapping strings command (recieved by http clients) to abstractaction.AbstractAction 
#derived classes that can handle the other params and the appropriate actions
actionmodules={ "createuser" : usersaction.CreateUser ,
        "getuser" : usersaction.GetUser,
        "follow" : usersaction.Follow,
        "unfollow" : usersaction.Unfollow,
        "getfollowing" : usersaction.GetFollowing,
        "postmessage" : postsaction.PostMessage,
        "getfeed" : postsaction.GetFeed,
        "getglobalfeed" : postsaction.GetFeed }
