# Nodejs
FROM node:23

# Wokdir lol
WORKDIR /app

# Copy every package.json
COPY package*.json ./

# Install dep
RUN npm install

# Copy all app
COPY . .

# Build this
RUN npm run build

# Expose running port
EXPOSE 5173

# Run this
CMD ["npm", "run", "dev"]