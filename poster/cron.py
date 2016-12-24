from poster.models import PostableItem
import poster.actions as actions
import time
import os

def auto_post(*args):
    os.chdir(args[0])
    item = PostableItem.objects.get(pk=2)
    currTime = int(time.time())
    if (currTime % item.repostWaitInterval) < 30:
        actions.delete(item)
        actions.post(item)
        print("Reposted item {} at {}".format(item.title, currTime))


