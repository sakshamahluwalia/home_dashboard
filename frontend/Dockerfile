# Stage 1: Build Stage
FROM node:20-alpine AS build

WORKDIR /app

# Copy package.json and package-lock.json
COPY package*.json ./

# Install dependencies
RUN yarn install

# Copy the rest of the application code
COPY . .


# Accept build arguments
ARG VITE_API_URL
ENV VITE_API_URL=$VITE_API_URL


# Build the app
RUN yarn build

# Stage 2: Production Stage
FROM nginx:stable-alpine

# Copy the build output to nginx's html directory
COPY --from=build /app/dist /usr/share/nginx/html

# Expose port 80
EXPOSE 80

# Start Nginx server
CMD ["nginx", "-g", "daemon off;"]
