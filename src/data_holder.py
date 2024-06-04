from settings import T
global misinformation_count, upvoted_misinformation_count, messages_exchanged_steps, votes_exchanged_steps, message_propagation_times_80_percentile, message_propagation_times_90_percentile, message_propagation_times_full, total_owt_created, total_owts_responded_to, adversary_count, message_seen_counter
misinformation_count = [0] * T
upvoted_misinformation_count = [0] * T
downvoted_misinformation_count = [0] * T

messages_exchanged_steps = [0] * T
votes_exchanged_steps = [0] * T 

message_propagation_times_80_percentile = []
message_propagation_times_90_percentile = []
message_propagation_times_full = []

# total messages sent out
total_owt_created = 0
total_owts_responded_to = 0

adversary_count = 0

highest_percentile_reached_for_message = 0

message_seen_counter = {}