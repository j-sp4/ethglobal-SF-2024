FROM --platform=linux/amd64 node:20-alpine

WORKDIR /app

# Copy package files and install dependencies
COPY ./app/package.json ./app/package-lock.json* ./
RUN npm ci

# Copy the source code and configuration files
COPY ./app .

# Build the Next.js app
RUN npm run generate

EXPOSE 3000

CMD ["npm", "start"]
