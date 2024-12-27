# Stage 1: Build Stage
FROM node:20-alpine AS build

# Set the working directory
WORKDIR /usr/src/app

# Copy package.json and package-lock.json
COPY package*.json ./

# Install dependencies
RUN yarn install

# Copy the source code
COPY . .

# Build the TypeScript code
RUN yarn build

# Stage 2: Production Stage
FROM node:20-alpine

WORKDIR /usr/src/app

# Copy the compiled code from the build stage
COPY --from=build /usr/src/app/dist ./dist

# Copy package.json to install only production dependencies
COPY package.json ./

# Install only production dependencies
RUN yarn install --production

# Expose the port
EXPOSE ${PORT}

# Accept build arguments
ARG DATA_PIPELINE_URL
ENV DATA_PIPELINE_URL=$DATA_PIPELINE_URL

# Start the application
CMD ["yarn", "docker-start"]
