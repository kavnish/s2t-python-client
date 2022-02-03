from grpc_utils import getStub
from onlineSession import onlineSession
from Listener import  Listener
from tests import testPunctuation, testOffline, testAudioIterator, testOnline


#*-*-*       Examples        *-*-*#

# testPunctuation(stub, text)
# testOffline(stub, file_path)
# testAudioIterator()
# testOnline(stub)

#*-*-*         main         *-*-*#

stub = getStub()
testOnline(stub)

#*-*-*       Sample Text        *-*-*#

'''Training speaker-discriminative and robust speaker verification systems without speaker labels is still challenging and worthwhile to explore. In this study,
 we propose an effective self-supervised learning framework and a novel regularization strategy to facilitate self-supervised speaker representation learning.
  Different from contrastive learning-based'''



