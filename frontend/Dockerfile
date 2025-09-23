# frontend/Dockerfile
FROM node:18-alpine

WORKDIR /app

# Install dependencies
COPY package*.json ./
RUN npm install

# Copy source code
COPY . .

# Build Next.js app
RUN npm run build

# Expose the default Next.js port
EXPOSE 3000

# Start the app in production mode
CMD ["npm", "run", "start"]
