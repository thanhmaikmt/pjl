Protocol


Client sends >
Server sends < 

First message must be your name
>NAME


>L
< +NAME1
< +NAME2
< + ...
< $

>[G|g]   opo_name                  # G I move first
<[!|?]   message


>m column
<m column                          # -1 means opo has left game

>[l|w|d]                           # loss win draw at end of the game   

>Q                                 # quit                                

