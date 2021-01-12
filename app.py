from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
from os import environ, remove
import imgkit
from PIL import Image

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
TOKEN = '13711ba50ac880e44c115afed90d5267d9e0e695716cd8ceaab0469f4d31cad4'
# TOKEN = environ['TOKEN']

# imgkit.from_file('x.html', 'out.jpg')

def cropper():
  image = Image.open('out.png')
  box = (image.size[0]/2 - image.size[0]/8, 0, image.size[0]/2 + image.size[0]/8, image.size[1])
  cropped_image = image.crop(box)
  cropped_image.save('cropped_image.png')
  remove('out.png')


@app.route('/wake')
def wake():
    if request.headers['auth'] == TOKEN:
        return 'Hey, I\'m the server and I\'m up', 200
    else:
        return 'ERRRRRRRRrrrrrr', 403


@app.route('/png', methods=['POST'])
def png():
    if request.headers['auth'] == TOKEN:
        args = request.get_json()
        print(args['latex'])
        imgkit.from_string(
            baseStart + args['latex'] + baseEnd, 'out.png', options=options)
        cropper()
        return send_file('cropped_image.png', mimetype='image/png')

@app.route('/matrix', methods=['POST'])
def matrix():
  if request.headers['auth'] == TOKEN:
    args = request.get_json()
    mat = args['matrix']
    start = r'\begin{bmatrix}'
    end = r'\end{bmatrix}'
    s = ''
    for i in mat:
      for j in i:
        s = s + str(j) + '&'
      s = s[0:len(s) - 1] + '\\\\'
    imgkit.from_string(baseStart + start + s + end + baseEnd, 'out.png', options=options)
    cropper()
    return send_file('cropped_image.png', mimetype='image/png')

@app.after_request
def delete(response):
  remove('cropped_image.png')
  return response

if __name__ == "__main__":
    app.run(debug=True)
