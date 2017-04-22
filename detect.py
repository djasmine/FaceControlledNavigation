import urllib2
import time
import cv2
import base64


def detect_face(img):
    http_url = 'https://api-us.faceplusplus.com/facepp/v3/detect'
    key = "cyPxYi2NRhtB8o08J09q-APaV7Xmj4dW"
    secret = "ado3lgbDDi_BOMbyzYs8uwvMxpiPQHxm"
    return_attributes = "headpose"
    boundary = '----------%s' % hex(int(time.time() * 1000))
    data = []
    data.append('--%s' % boundary)
    data.append('Content-Disposition: form-data; name="%s"\r\n' % 'api_key')
    data.append(key)
    data.append('--%s' % boundary)
    data.append('Content-Disposition: form-data; name="%s"\r\n' % 'api_secret')
    data.append(secret)
    data.append('--%s' % boundary)
    data.append('Content-Disposition: form-data; name="%s"\r\n' % 'return_attributes')
    data.append(return_attributes)
    data.append('--%s' % boundary)
    cnt = cv2.imencode('.png', img)[1]
    b64 = base64.encodestring(cnt)
    data.append('Content-Disposition: form-data; name="%s"' % 'image_base64')
    data.append('Content-Type: %s\r\n' % 'application/octet-stream')
    data.append(b64)
    data.append('--%s--\r\n' % boundary)

    http_body = '\r\n'.join(data)
    # build http request
    req = urllib2.Request(http_url)
    # header
    req.add_header('Content-Type', 'multipart/form-data; boundary=%s' % boundary)
    req.add_data(http_body)
    try:
        # post data to server
        resp = urllib2.urlopen(req, timeout=5)
        # get response
        qrcont = resp.read()
        #print qrcont
        return qrcont

    except urllib2.HTTPError as e:
        print e.read()

