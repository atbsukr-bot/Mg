# Procedural neon room (inspired by the owner's reference): deep blue/purple walls, hexagon light panels,
# glowing TV, couch silhouette, red LED strip. Rendered sharp, then depth-of-field blur.
import numpy as np, cv2
W,H=2200,1240  # oversize so camera moves never show an edge
y,x=np.mgrid[0:H,0:W].astype(np.float32)
img=np.zeros((H,W,3),np.float32)  # BGR 0..1
# wall: blue -> violet gradient, darker at floor and corners
base=np.array([0.55,0.10,0.05])*(1-x/W)[...,None]+np.array([0.50,0.06,0.20])*(x/W)[...,None]
vign=np.clip(1-(((x-W*0.5)/(W*0.65))**2+((y-H*0.42)/(H*0.75))**2),0.05,1)[...,None]
img+=base*vign*0.9
# wall corner / panel lines
cv2.line(img,(int(W*0.30),0),(int(W*0.30),int(H*0.62)),(0.30,0.05,0.04),6)
def glow(c, rad, col, k):
    m=np.zeros((H,W),np.float32); cv2.circle(m,c,rad,1,-1)
    for s,a in ((rad*0.6,0.9),(rad*2.5,0.45),(rad*6,0.25)):
        img[:]+= cv2.GaussianBlur(m,(0,0),s)[...,None]*np.array(col)*a*k
# hexagon light panels (cyan, magenta, violet), top centre-right like the reference
def hexagon(cx,cy,r,col):
    pts=np.array([[cx+r*np.cos(np.pi/3*i+np.pi/6),cy+r*np.sin(np.pi/3*i+np.pi/6)] for i in range(6)],np.int32)
    m=np.zeros((H,W),np.float32); cv2.fillPoly(m,[pts],1)
    for s,a in ((2,1.0),(25,0.6),(70,0.35)): img[:]+=cv2.GaussianBlur(m,(0,0),s)[...,None]*np.array(col)*a
r=58; dx=r*np.sqrt(3)
for (i,j,col) in [(0,0,(1.0,0.85,0.2)),(1,0,(0.95,0.35,0.95)),(0.5,1,(0.9,0.2,0.75)),(1.5,1,(1.0,0.9,0.3)),(2,0,(1.0,0.3,0.95)),(-0.5,1,(1.0,0.75,0.15))]:
    hexagon(int(W*0.53+i*dx), int(H*0.17+j*r*1.5), r-4, col)
# TV on the right: rounded frame + warm orange/pink image
tx0,ty0,tx1,ty1=int(W*0.70),int(H*0.30),int(W*0.92),int(H*0.52)
cv2.rectangle(img,(tx0-8,ty0-8),(tx1+8,ty1+8),(0.02,0.02,0.03),-1)
tv=np.zeros((ty1-ty0,tx1-tx0,3),np.float32); ty,tx=np.mgrid[0:ty1-ty0,0:tx1-tx0]
tv[:]=np.array([0.45,0.15,0.55])
blob=np.exp(-(((tx-tv.shape[1]*0.45)/(tv.shape[1]*0.22))**2+((ty-tv.shape[0]*0.55)/(tv.shape[0]*0.3))**2))
tv+=blob[...,None]*np.array([0.1,0.55,1.0])*0.9
img[ty0:ty1,tx0:tx1]=tv
m=np.zeros((H,W),np.float32); m[ty0:ty1,tx0:tx1]=1
img+=cv2.GaussianBlur(m,(0,0),90)[...,None]*np.array([0.6,0.25,0.7])*0.6
# small blue spots on the wall (left), like recessed lights
glow((int(W*0.36),int(H*0.06)),10,(1.0,0.55,0.3),0.8); glow((int(W*0.62),int(H*0.06)),8,(1.0,0.55,0.3),0.6)
# red LED strip bottom right + red glow
cv2.line(img,(int(W*0.66),int(H*0.66)),(W,int(H*0.66)),(0.15,0.1,1.0),5)
m=np.zeros((H,W),np.float32); cv2.line(m,(int(W*0.66),int(H*0.66)),(W,int(H*0.66)),1,8)
img+=cv2.GaussianBlur(m,(0,0),40)[...,None]*np.array([0.1,0.05,0.9])*1.4
# couch silhouette left + floor
cv2.rectangle(img,(0,int(H*0.62)),(int(W*0.34),H),(0.16,0.04,0.03),-1)
cv2.rectangle(img,(0,int(H*0.55)),(int(W*0.30),int(H*0.66)),(0.20,0.05,0.04),-1)
img[int(H*0.80):]*=0.45
img=np.clip(img,0,1.4)
# depth of field
img=cv2.GaussianBlur(img,(0,0),11)
# grain-free tone map
img=1-np.exp(-img*1.25)
cv2.imwrite('work/neon_bg.png',(img*255).astype(np.uint8))
