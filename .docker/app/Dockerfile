FROM --platform=linux/amd64 node:20-alpine

WORKDIR /app

# Install Python3, make, and g++ for building native modules
RUN apk update && apk add --no-cache python3 make g++ \
    && ln -sf /usr/bin/python3 /usr/bin/python

# Set the PYTHON environment variable for node-gyp
ENV PYTHON=/usr/bin/python3

# Copy package files and install dependencies
COPY ./app/package.json ./app/package-lock.json* ./
RUN npm ci

# Copy the source code and configuration files
COPY ./app .

# Build the Next.js app
RUN npm run generate

EXPOSE 3000

CMD ["npm", "start"]
