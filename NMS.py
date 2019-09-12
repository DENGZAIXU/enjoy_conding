import numpy as np
 
 
def nms(dets, thresh):
  x1 = dets[:, 0]
  y1 = dets[:, 1]
  x2 = dets[:, 2]
  y2 = dets[:, 3]
  score = dets[:, 4]
  
  order = score.argsort()[::-1]
  area = (x2 - x1) * (y2 - y1)
  res = []
  while order.size >= 1:
    i = order[0]
    res.append([x1[i], y1[i], x2[i], y2[i], score[i]])
    
    #intersect area left top point(xx1, yy1): xx1 >= x1, yy1 >= y1
    #intersect area right down point(xx2, yy2): xx2 <= x2, yy2 <= y2
    
    xx1 = np.maximum(x1[i], x1[order[1:]])
    yy1 = np.maximum(y1[i], y1[order[1:]])
    xx2 = np.minimum(x2[i], x2[order[1:]])
    yy2 = np.minimum(y2[i], y2[order[1:]])
 
    w = np.maximum(0.0, (xx2 - xx1))
    h = np.maximum(0.0, (yy2 - yy1))
    intersect = w * h
    
    #iou = intersect area / union; union = box1 + box2 - intersect
    iou = intersect / (area[i] + area[order[1:]] - intersect)
    # print("iou",iou)
    
    #update order index;ind +1:because ind is obtain by index [1:]
    ## NMS
    ind = np.where(iou <= thresh)[0]
    

    ## soft NMS
    weight = np.exp(-(iou*iou) / sigma) ## sigma = 0.5

    score[order[1:] = weight*score[order[1:]]

    idx = np.where(order[1:,4] <= 0.0001)[0]

    #print("idx",ind)
    #print("test",ind+1)
    order = order[ind +1]
    #print("order",order)
    
  return res
      
 
 
 
 
if __name__ == "__main__":
  
  dets = np.array([
                  [204, 102, 358, 250, 0.5],
                  [257, 118, 380, 250, 0.7],
                  [280, 135, 400, 250, 0.6],
                  [255, 118, 360, 235, 0.7]
                  ])
 
 
  thresh = 0.7
  res = nms(dets, thresh)
  print(res)
