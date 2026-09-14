import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

const backendPath = path.resolve(__dirname, '../source/new');
const publicPath = path.resolve(__dirname, 'public/osint-assets');
const generatedFiles = ['data.js', 'data_checkin.js'];
const staticFiles = ['network.html', 'checkin_routes.html'];

function ensureDirectory(directory) {
  fs.mkdirSync(directory, { recursive: true });
}

function copyFile(relativePath) {
  const sourcePath = path.join(backendPath, relativePath);
  const targetPath = path.join(publicPath, relativePath);

  if (!fs.existsSync(sourcePath)) return false;

  ensureDirectory(path.dirname(targetPath));
  fs.copyFileSync(sourcePath, targetPath);
  return true;
}

function syncDirectory(relativePath) {
  const sourceDir = path.join(backendPath, relativePath);
  const targetDir = path.join(publicPath, relativePath);

  if (!fs.existsSync(sourceDir)) return;

  ensureDirectory(targetDir);
  fs.cpSync(sourceDir, targetDir, { recursive: true, force: true });
}

function watchFile(relativePath) {
  const sourcePath = path.join(backendPath, relativePath);
  if (!fs.existsSync(sourcePath)) return;

  fs.watchFile(sourcePath, { interval: 500 }, (current, previous) => {
    if (current.mtimeMs !== previous.mtimeMs) {
      copyFile(relativePath);
    }
  });
}

ensureDirectory(publicPath);

staticFiles.forEach(copyFile);
syncDirectory('map');

// Generated crawl data is copied only when it exists locally. These files are
// intentionally ignored by Git and should never be committed to the repository.
generatedFiles.forEach((file) => {
  copyFile(file);
  watchFile(file);
});

const crawlDataRelativePath = 'CrawCheckin/src/data';
const crawlDataPath = path.join(backendPath, crawlDataRelativePath);
syncDirectory(crawlDataRelativePath);

if (fs.existsSync(crawlDataPath)) {
  fs.watch(crawlDataPath, { recursive: false }, (_eventType, filename) => {
    if (filename?.endsWith('.json')) {
      syncDirectory(crawlDataRelativePath);
    }
  });
}

console.log(`OSINT assets synced to ${publicPath}`);
console.log('Watching generated crawl data. Press Ctrl+C to stop.');

process.on('SIGINT', () => {
  generatedFiles.forEach((file) => {
    fs.unwatchFile(path.join(backendPath, file));
  });
  process.exit(0);
});
