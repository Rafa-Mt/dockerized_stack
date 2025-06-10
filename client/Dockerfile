FROM node:23-alpine

WORKDIR /app

COPY package.json .

RUN npm i
# Use --omit-dev for deployment

RUN npm i -g serve 

COPY . .

RUN npm run build

EXPOSE 8080

CMD ["serve", "-s", "dist", "--listen", "8080"]