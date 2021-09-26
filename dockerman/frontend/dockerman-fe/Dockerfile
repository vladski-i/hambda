FROM node:12-buster
ADD . /app
WORKDIR /app
RUN npm install
ENV HOST=0.0.0.0
CMD ["npm", "start"]