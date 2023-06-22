FROM node:lts-alpine as builder


WORKDIR /app

COPY package*.json ./

RUN npm install

COPY . .

RUN npm run build


FROM nginx:latest


COPY nginx.conf /etc/nginx/

WORKDIR /static
COPY --from=builder /app/dist ./