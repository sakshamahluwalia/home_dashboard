# Stage 1: Build Stage
FROM node:20-alpine AS build

# Set the working directory
WORKDIR /usr/src/app

# Copy package.json and package-lock.json
COPY package*.json ./

# Install dependencies
RUN npm install

# Copy the source code
COPY . .

# Build the TypeScript code
RUN npm run build

# Stage 2: Production Stage
FROM node:20-alpine

WORKDIR /usr/src/app

# Copy the compiled code from the build stage
COPY --from=build /usr/src/app/dist ./dist

# Copy package.json to install only production dependencies
COPY package.json ./

# Install only production dependencies
RUN npm install --only=production

# Expose the port
EXPOSE 3000

# Start the application
CMD ["npm", "run", "docker-start"]
