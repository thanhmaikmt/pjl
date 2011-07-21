import feedforwardbrain

sz=[1,3,1]

brain=feedforwardbrain.FeedForwardBrain(sz)

print brain.weight
print brain.layer_size

brain.resize_inputs(3)

print brain.weight
print brain.layer_size

brain.mutate(100)

print brain.weight
print brain.layer_size



                