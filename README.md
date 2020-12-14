# Leaners Digital Latex -> PNG, microservice

### current status

3 routes available 

- `/wake` => wake up the API incase using serverless

- `/png` => given a latex generates a coresponding png

- `/matrix` => given a 2D aray generates a png of a bmatrix


Uses `wkhtmltopdf` wrapped around by `imgkit`