# --- builder: npm ci по package-lock.json и сборка Nuxt ---
FROM node:24.21.0-alpine3.24 AS builder

WORKDIR /app
COPY package.json package-lock.json ./
RUN npm ci --ignore-scripts
COPY . .
RUN npx nuxt prepare && npm run build

# --- runtime: только собранный .output, процесс от пользователя node ---
FROM node:24.21.0-alpine3.24 AS runtime

ENV NODE_ENV=production \
    HOST=0.0.0.0 \
    PORT=3000

WORKDIR /app
COPY --from=builder --chown=root:root /app/.output ./.output

USER node

EXPOSE 3000

CMD ["node", ".output/server/index.mjs"]
