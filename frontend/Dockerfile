FROM node:alpine

RUN mkdir -p /usr/src/app
COPY . /usr/src/app
ENV PATH /usr/src/app/node_modules/.bin:$PATH
WORKDIR /usr/src/app

RUN npm install

EXPOSE 3000
ENTRYPOINT ["npm", "start"]
