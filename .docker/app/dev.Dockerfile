FROM node:20-alpine

WORKDIR /app

# Install Python3, make, and g++ for building native modules
RUN apk update && apk add --no-cache python3 make g++ \
    && ln -sf /usr/bin/python3 /usr/bin/python

# Set the PYTHON environment variable for node-gyp
ENV PYTHON=/usr/bin/python3

COPY ./app/package.json ./app/package-lock.json* ./
RUN npm install

COPY . .

CMD ["npm", "run", "dev"]
