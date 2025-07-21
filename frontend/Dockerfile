
FROM node:18-alpine

WORKDIR /app

# npmレジストリミラーを設定
RUN npm config set registry https://registry.npmjs.org/

COPY package*.json ./
RUN npm install

COPY . .

EXPOSE 3000

# 開発モードで起動（HMRを無効化）
ENV NEXT_TELEMETRY_DISABLED=1
CMD ["npm", "run", "dev"]
