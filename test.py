import numpy as np

def loadMatrix(f):
    m = np.genfromtxt(f, delimiter=',')
    m = np.nan_to_num(m)
    m = np.matrix(m)
    return m

A = loadMatrix("purchase.csv")
V = loadMatrix("view.csv")

AtA = np.transpose(A) * A

hp3 = np.array([1,0,0,0,1,0,0])
hp3 * AtA  # user-centric recommendations based on history of user purchases

hv3 = np.array([0,1,0,1,0,1,0])

AtV = np.transpose(A) * V

right = np.vstack((hp3.reshape(-1,1), hv3.reshape(-1,1)))
left = np.hstack((AtA, AtV))

r3 = left * right


# Correlation or not correlation

# P = purchase.  User: u1, u2, u3; Products: A, B, C
P = np.matrix([[1, 1, 0],
               [0, 0, 0],
               [0, 0, 1]])

# G = gender.  M or F
G = np.matrix([[1, 0],
               [0, 1],
               [1, 0]])

PtG = np.transpose(P) * G
# Note that since u2 (female) hasn't bought anything, the female column are all zeros.

r2 = PtG * G[1,:].reshape(-1,1) # So the recommendation for user2, based on gender, are still all zeros
r1 = PtG * G[0,:].reshape(-1,1) # But r1 will get recommendation for all 3 items because u3 is also a male.
r3 = PtG * G[2,:].reshape(-1,1) # And r3 will also get recommendation for all 3 items because u1 is also a male.


G[2] = [0,1] # Let's say u3 becomes a female.
PtG = np.transpose(P) * G
r1 = PtG * G[0,:].reshape(-1,1) # Now r1 will not get recommendation for the 3rd item.


###################################
###################################

A = np.matrix([[1,0,1,0,0,0], [1,0,1,0,1,0], [0,1,1,1,0,0], [0,1,0,1,0,1], [0,0,0,0,0,0]]) # History of purchase

# In the following examples, each value in the vector represents the total # of items the user has purchased
# from the specified product mix.
print "Item 3:", (A * np.matrix([0,0,1,0,0,0]).transpose()).tolist() # Call .tolist() just for ease of viewing
print "Item 4:", (A * np.matrix([0,0,0,1,0,0]).transpose()).tolist()
print "Item 3 and 4:", (A * np.matrix([0,0,1,1,0,0]).transpose()).tolist()
print "Item 1 and 3:", (A * np.matrix([1,0,1,0,0,0]).transpose()).tolist()
