FROM node:20-alpine

WORKDIR /app

COPY ./app/package.json ./app/package-lock.json* ./
RUN npm ci

COPY . .

CMD ["npm", "run", "dev"]
