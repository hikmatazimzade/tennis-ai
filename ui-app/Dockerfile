FROM node:20-alpine

WORKDIR /app

# Copy package files
COPY ui-app/package*.json ./

# Install dependencies
RUN npm ci

# Copy application code
COPY ui-app/ .

# Expose port
EXPOSE 5173

# Run in development mode
CMD ["npm", "run", "dev", "--", "--host", "0.0.0.0"]