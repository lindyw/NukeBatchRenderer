# NOTES
'''
1. Check if the node is disabled or enabled
   - node['disable'].value()
2. os path:
     Last - os.path.basename
     Second Last - str.split("/")[-2]
'''
import nuke
import sys
import os
# Start Rendering each Nuke Project (.nk)
proj = str(sys.argv[1])
try:
    nuke.scriptOpen(proj)
except RuntimeError:
    pass

writenodes = []
startFrame = 0
endFrame = 0


# Recursive function to get the read node from the above
def getUpNode(n):
    if n.input(0).input(0) is None and n.input(0).Class() == "Read":
        return n.input(0)['file'].getValue()
    else:
        n = n.input(0)
        print n.name()
        return getUpNode(n)


for i in nuke.allNodes():
    if i.Class() == "//ZSERVER01/FreeDUI/FreeDUI/NukeTools/gizmos/jtool/seqWrite.gizmo":
        # write node and its read file
        str_name = getUpNode(i)
        print str_name
        writenodes.append(str(i.name()) + ": " + str(str_name.split("/")[-2]))
    elif i.Class() == "Write":
        str_name = i['file'].getValue()
        writenodes.append(str(i.name()) + ": " + str(str_name.split("/")[-2]))
# Write all nodes to txt file
if len(writenodes) > 0:
    # frame range
    startFrame = nuke.root()['first_frame'].getValue()
    endFrame = nuke.root()['last_frame'].getValue()
    if not os.path.exists('D:/Temp/nukeBatch/'):
        os.mkdir('D:/Temp/nukeBatch')
        print "NUKEBATCH"
    file = open(str("D:/Temp/nukeBatch/" + os.path.basename(proj) + ".txt"), 'w')
    for node in writenodes:
        file.write(node + "\n")
    file.write('FrameRange:\n')
    file.write(str(int(startFrame)) + "\n")
    file.write(str(int(endFrame)) + "\n")
    file.close()
# if i.Class() == "//ZSERVER01/FreeDUI/FreeDUI/NukeTools/gizmos/jtool/seqWrite.gizmo":
#     if i['name'].getValue() == "seqWrite1" or i['name'].getValue() == "seqWrite2":
#         first_frame = i.knob('IN').value()
#         last_frame = i.knob('OUT').value()
#         nuke.execute(i.node('Write1'), int(first_frame), int(last_frame))
# if i.Class() == "Write":
#     if i.knob('use_limit').getValue() == 1.0:
#         first_frame = i.knob('first').value()
#         last_frame = i.knob('last').value()
#         nuke.execute(i, int(first_frame), int(last_frame))
#     else:
#         print str(i) + " : No Frame Range specified"
nuke.scriptClose()
