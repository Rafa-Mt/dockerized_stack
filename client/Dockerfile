FROM node:23-alpine

WORKDIR /app

COPY package.json .

RUN npm i
# Use --omit-dev for deployment

RUN npm i -g serve 

COPY . .


EXPOSE 8080

CMD ["npm", "run", "dev"]