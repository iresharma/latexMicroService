from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
from os import environ, remove, walk
import imgkit
from PIL import Image
import random
import string

TOKEN = '13711ba50ac880e44c115afed90d5267d9e0e695716cd8ceaab0469f4d31cad4'

baseStart = '''
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <title>Maths Equations</title>
  <script src='https://cdn.mathjax.org/mathjax/latest/MathJax.js?config=TeX-AMS-MML_HTMLorMML'></script>
  <script>
  MathJax.Hub.Config({
  tex2jax: {inlineMath: [['$','$'], ['\\(','\\)']]}
});
  </script>
</head>
<body>
  <h2>$$'''

baseEnd = '''
$$</h2>
</body>
</html>
'''

options = {
    'format': 'png',
    'encoding': "UTF-8",
    'custom-header': [
        ('Accept-Encoding', 'gzip')
    ],
}

app = Flask(__name__)

CORS(app)

def cropper(name: str):
  image = Image.open(name)
  box = (image.size[0]/2 - image.size[0]/8, 0, image.size[0]/2 + image.size[0]/8, image.size[1])
  cropped_image = image.crop(box)
  cropped_image.save('cropped_image' + '_' + name +'.png')
  remove(name)
  return 'cropped_image' + '_' + name +'.png'


@app.route('/wake')
def wake():
    if request.headers['auth'] == TOKEN:
        return 'Hey, I\'m the server and I\'m up', 200
    else:
        return 'ERRRRRRRRrrrrrr', 403


@app.route('/png', methods=['POST'])
def png():
    args = request.get_json()
    print(args['latex'])
    res = ''.join(random.choices(string.ascii_uppercase +
                             string.digits, k = 5))
    imgkit.from_string(
        baseStart + args['latex'] + baseEnd, res + '.png', options=options)
    name = cropper(res + '.png')
    return send_file(name, mimetype='image/png')

@app.route('/matrix', methods=['POST'])
def matrix():
  args = request.get_json()
  mat = args['matrix']
  start = r'\begin{bmatrix}'
  end = r'\end{bmatrix}'
  s = ''
  for i in mat:
    for j in i:
      s = s + str(j) + '&'
    s = s[0:len(s) - 1] + '\\\\'
  res = ''.join(random.choices(string.ascii_uppercase +
                             string.digits, k = 5))
  imgkit.from_string(baseStart + start + s + end + baseEnd, res + '.png', options=options)
  name = cropper(res + '.png')
  return send_file(name, mimetype='image/png')

@app.after_request
def delete(response):
  path = walk('.')
  for root, direc, files in path:
    for i in files:
      if 'cropped_image' in i:
        remove(i)
  return response

if __name__ == "__main__":
    app.run(debug=True)
