# [1] BUILD STAGE

# install node and create app dir in container
FROM node:10.13.0-alpine as build-stage
WORKDIR /app

# copy the package.json dependencies and install them
COPY package*.json ./
RUN npm install

# copy all the client app contents into /app
COPY . .

# create build
RUN npm run generate

# [2] PRODUCTION STAGE
FROM nginx:1.19.3-alpine as production-stage
COPY --from=build-stage /app/dist /usr/share/nginx/html
EXPOSE 80
CMD [ "nginx", "-g", "daemon off;" ]