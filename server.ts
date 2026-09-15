import express from "express";
import http from "http";
import path from "path";
import { spawn, ChildProcess } from "child_process";

const app = express();
const PORT = 3000;
const FLASK_PORT = 5000;

let pythonProcess: ChildProcess | null = null;

function startFlask() {
  const restaurantDir = path.join(process.cwd(), "Ahaaram_Restaurant");
  console.log(`[Ahaaram Server] Launching Python Flask backend on port ${FLASK_PORT}...`);

  pythonProcess = spawn("python3", ["app.py"], {
    cwd: restaurantDir,
    env: { ...process.env, PORT: String(FLASK_PORT), PYTHONUNBUFFERED: "1" },
    stdio: "inherit",
  });

  pythonProcess.on("exit", (code, signal) => {
    console.warn(`[Ahaaram Server] Flask process exited (code=${code}, signal=${signal})`);
  });
}

// Start Flask backend
startFlask();

process.on("exit", () => {
  if (pythonProcess) {
    pythonProcess.kill();
  }
});

// Health check endpoint
app.get("/api/health", (_req, res) => {
  res.json({ status: "ok", app: "Ahaaram Multi Cuisine Restaurant" });
});

// Proxy all requests to the Python Flask backend
app.use((req, res) => {
  const options: http.RequestOptions = {
    hostname: "127.0.0.1",
    port: FLASK_PORT,
    path: req.originalUrl,
    method: req.method,
    headers: {
      ...req.headers,
      host: `127.0.0.1:${FLASK_PORT}`,
      "x-forwarded-host": req.headers.host || `localhost:${PORT}`,
      "x-forwarded-proto": "http",
    },
  };

  const proxyReq = http.request(options, (proxyRes) => {
    res.writeHead(proxyRes.statusCode || 200, proxyRes.headers);
    proxyRes.pipe(res);
  });

  proxyReq.on("error", (err) => {
    console.error(`[Ahaaram Proxy Error] ${err.message}`);
    if (!res.headersSent) {
      res.status(502).send(
        `<!DOCTYPE html>
        <html lang="en">
        <head>
          <meta charset="UTF-8">
          <title>Ahaaram Multi Cuisine Restaurant - Starting Up</title>
          <style>
            body { font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background: #1a1918; color: #f9f7f4; display: flex; align-items: center; justify-content: center; height: 100vh; margin: 0; }
            .card { background: #252422; border: 1px solid #c59d5f; padding: 40px; border-radius: 12px; text-align: center; max-width: 480px; box-shadow: 0 10px 30px rgba(0,0,0,0.5); }
            h2 { color: #c59d5f; margin-top: 0; font-family: Georgia, serif; font-size: 1.8rem; }
            p { color: #d0cbc3; line-height: 1.6; }
            .spinner { width: 36px; height: 36px; border: 3px solid rgba(197,157,95,0.3); border-top-color: #c59d5f; border-radius: 50%; animation: spin 1s infinite linear; margin: 24px auto; }
            @keyframes spin { 100% { transform: rotate(360deg); } }
          </style>
        </head>
        <body>
          <div class="card">
            <h2>AHAARAM</h2>
            <div style="font-size: 0.85rem; color: #c59d5f; letter-spacing: 0.15em; margin-bottom: 20px;">MULTI CUISINE RESTAURANT</div>
            <div class="spinner"></div>
            <p>Initializing cuisine database & dining services. Please stand by...</p>
            <script>setTimeout(() => window.location.reload(), 2000);</script>
          </div>
        </body>
        </html>`
      );
    }
  });

  req.pipe(proxyReq);
});

app.listen(PORT, "0.0.0.0", () => {
  console.log(`[Ahaaram Server] Running and listening on port ${PORT}`);
});
