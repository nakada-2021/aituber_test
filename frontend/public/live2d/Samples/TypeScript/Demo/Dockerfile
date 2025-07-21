FROM node:20

WORKDIR /app

COPY . .

RUN npm install && npm run build

CMD ["ls", "-l", "build"] 