# NOTES
'''
1. Check if the node is disabled or enabled
   - node['disable'].value()

'''

import nuke
import sys
import os
# Start Rendering each Nuke Project (.nk)
proj = str(sys.argv[2])
nodes = []
nodes = sys.argv[3]
start = str(sys.argv[4])
end = str(sys.argv[5])

# try:
#     nuke.scriptOpen(proj)
# except RuntimeError:
#     pass

for n in nodes:
    print ("NAME:" + str(nuke.toNode(str(n))))
    # nuke.execute(n, int(start), int(end))
# for i in nuke.allNodes():
#     if i.Class() == "Write" or i.Class() == "//ZSERVER01/FreeDUI/FreeDUI/NukeTools/gizmos/jtool/seqWrite.gizmo":
#         writenodes.append(i)
# return writenodes
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
