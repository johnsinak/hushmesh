T = 120 # Steps Internet blackout = 5days 5 * 24 / 120 = 1 hours
N = 600 # users
A = 25 # X
B = 25 # Y
WORLD_DIMENSION = (A, B)
r = 2
MOVE_RANGE = ((-r, r), (-r, r))
d = 1
MESSAGE_EXCHANGE_RANGE = ((-d, d), (-d, d))
ADVERSARY_RATIO = 0.015
# TODO: removeeeeeeeeeeee
JAMMING_ATTACK = True

# Watts-Strogatz model parameters
WS_DELTA = 15
# WS_DELTA = N // 10
WS_BETA = 0.5

# User settings
MESSAGE_STORAGE_SIZE = 1500 
MAX_VOTES_ALLOWED_ON_MESSAGE = 10000 # 1.5 GB

# (10000 + 10000)
# 1000 rest 
# 19000 junk | 
# Write about this, and discuss how this affects us add to 5.2 all params

MIN_TTL = 15
USER_MESSAGE_CREATION_RATE = 0.05 # Fixed
USER_ACT_PROBABILITY = 0.15 # Fixed Write all the reasoning

OWT_MIN_TRUST_VALUE = 4 # [[[[[[[Code]]]]]]] Fixed Change to ratio, for the scale: i.e 1000UP 995 D should not be trusted
OWT_MIN_UP_RATIO = 0.6 #60 percent upvotes
# 10 UP - 6 D
UPVOTE_MIN_TRUST_VALUE = 2 # Fixed
UPVOTE_MIN_UP_RATIO = 0.6 # FIXED

ADVERSARY_FRIEND_REDUCTION = 0.4 # Tweakable
USER_VOTING_ON_UNKNOWN_MESSAGES_RATE = 0.02 # Tweakable Important param
USER_UPVOTING_ON_MISINFORMATION_RATE = 0.3 # Tweakable Important param
USER_UPVOTING_ON_NORMAL_RATE = 0.6 # Tweakable Important param

# Go for 3 examples and try to describe those

# Talk about adversary trying to tweak the trust scores |

# leave red message to mention trust does not get calcualted if we don't don't know the  don't know the voters
# don't know the author
# don't know the voters

OLD_MESSAGE_CUTOFF = 24
# mention in both design 4.5 (how the message storage works) and  implementation 5.2
#Add information about the owt handling (out going and incoming) and how we treat the older ones (do we use the same cutoff or not)

# [[[PROGRAMMING]]] Fix: the created_at thing with a received at for the class and that's what the old message cutoff should be calculated on
# TODO: [[[PROGRAMMING]]] Fix the how many adversary messages were trusted field
# Program related
UPVOTE = True
DOWNVOTE = False

# TODO: Write the evaluation section
# TODO: finish 4.6

# DIOGO: full draft of the paper except the intro by tomorrow night