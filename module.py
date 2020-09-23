import bpcs

alpha = 0.45
vslfile = 'C:/Users/areev/OneDrive/Documents/GitHub/bpcs/examples/vessel.png'
msgfile = 'C:/Users/areev/OneDrive/Documents/GitHub/bpcs/examples/message.txt' # can be any type of file
encfile = 'C:/Users/areev/OneDrive/Documents/GitHub/bpcs/examples/encoded.png'
msgfile_decoded = 'C:/Users/areev/OneDrive/Documents/GitHub/bpcs/examples/tmp.txt'

#bpcs.capacity(vslfile, alpha) # check max size of message you can embed in vslfile
bpcs.encode(vslfile, msgfile, encfile, alpha) # embed msgfile in vslfile, write to encfile
bpcs.decode(encfile, msgfile_decoded, alpha) # recover message from encfile