import re

# Your sentence
sentence = "The quick brown the fox jumps over the lazy dog."
word='the'
# Define a regular expression pattern
pattern = f'{word}[^{word}]'  # This pattern matches three-letter words.

# Use re.search() to find words matching the pattern
matches = re.findall(pattern, sentence)

# Print the matching words
print(matches)
# import re
# cause = 'Prod'
# effect = 'S'
# # Define the regular expression pattern
# OneEffectPattern = f'[^{cause}]*({cause}[^{effect}]*{effect}[^{effect}{cause}]*)+'
# OneCausePattern = f'[^{cause}]*({cause}[^{effect}{cause}]*{effect}[^{cause}]*)+'
# CauseFirstPattern = f'[^{cause}{effect}]*({cause}[^{effect}]*{effect}[^{cause}]*)+'
#
# # Test strings
# test_strings = [
#     "ProdS",       # Matches: One "P" followed by "S"
#     "ProdQS",      # Matches: "P" followed by "S"
#     "ProdProdProdProdSProdS",  # Matches: "P" followed by "S"
#     "ProdProdProdS",     # Matches: "P" followed by "S"
#     "ProdSProdSS",    # Does not match: Second "P" followed by more than one "S"
#     "ProdProdProdSProd",    # Does not match: Ends with "P" and no "S"
#     "ProdProdProdProdSSSSProdS",
#     "ProdProdProdSGYJHVProdSProdSJHHJProdNKS",
#     "hghjgProdS",
#     "ghvghjfProdfdgProdgS",
#     "ghvghjfProdfdgProdgSddd",
#     "SProdSS",
#     "SProdProdS"
# ]
#
# for string in test_strings:
#     match = re.fullmatch(OneCausePattern, string)
#     if match:
#         print(f'Matched: "{string}"')
#     else:
#         print(f'Not Matched: "{string}"')

#################################################################
#################################################################
#           Expected Output
#################################################################

# **************** One Effect ***********************************
#     "PS",       # Matches: One "P" followed by "S"
#     "PQS",      # Matches: "P" followed by "S"
#     "PPPPSPS",  # Matches: "P" followed by "S"
#     "PPPS",     # Matches: "P" followed by "S"
#     "PSPSS",    # Does not match: Second "P" followed by more than one "S"
#     "PPPSP",      # Does not match: Ends with "P" and no "S"
#     "PPPPSSSSPS", # Does not match: Mulitple occurance of S without P in between
#     "PPPSGYJHVPSPSJHHJPNKS", # Matches: PPPS GYJHV PS PS JHHJ P NK S
#     "hghjgPS",    # Matches: hghjgP S
#     "ghvghjfPfdgPgS", # Matches: ghvghjf P fdg P g S
#     "ghvghjfPfdgPgSddd", # Matches: ghvghjf P fdg P g S ddd
#     "SPSS",               # Does not match: Mulitple occurance of S without P in between
#     "SPPS"                # Matches: Mulitple occurance of P followed by one S



# **************** One Cause ***********************************
#     "PS",       # Matches: One "P" followed by "S"
#     "PQS",      # Matches: "P" followed by "S"
#     "PPPPSPS",  # Does not Match: multiple "P" followed by "S"
#     "PPPS",     # Does not Match: multiple "P" followed by "S"
#     "PSPSS",    # Matches: Second "P" followed by more than one "S"
#     "PPPSP",      # Does not match: Ends with "P" and no "S"
#     "PPPPSSSSPS", # Does not match: Mulitple occurance of P without S in between
#     "PPPSGYJHVPSPSJHHJPNKS", # Does not match: PPPS GYJHV PS PS JHHJ P NK S
#     "hghjgPS",    # Matches: hghjg PS
#     "ghvghjfPfdgPgS", # Does not match: ghvghjf P fdg P g S
#     "ghvghjfPfdgPgSddd", # Does not match: ghvghjf P fdg P g S ddd
#     "SPSS",               # Matches: Mulitple occurance of S followed one P
#     "SPPS"                # Does not match: Mulitple occurance of P followed by one S


# def is_satistifed_1effect(effect, cause, trace):
#     effect_index = -1
#     current_index = 0
#     satisfied = False
#     while current_index < len(trace):
#         satisfied = False
#         for event in range(current_index, len(trace)):
#             if event == effect:
#                 effect_index = trace.index(effect)
#                 current_index = effect_index
#                 break
#         for event in range(current_index, len(trace)):
#             if event == cause:
#                 current_index = trace.index(cause)
#                 if effect_index > -1 :
#                     satisfied = True
#                 break
#         found_another_effect = False
#         for event in range(current_index, len(trace)):
#             if event == effect:
#                 found_another_effect = True
#                 # current_index = trace.index(cause)
#             if event == cause and not found_another_effect:
#                 satisfied = False
#                 return satisfied
#     return satisfied
#     # sort effect_indexes
#     # sort cause_indexes
#     # take the largest effect index
#     # if there is only one cause_index larger than the effect_index
#         #then this is one effect pattren
