#!/bin/sh

# Write env.js dynamically
cat <<EOF > /usr/share/nginx/html/env.js
window.env = {
  VITE_BACKEND_URL: "${VITE_BACKEND_URL}"
};
EOF

# Start nginx normally
exec nginx -g "daemon off;"

