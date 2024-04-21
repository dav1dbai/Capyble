const { app, BrowserWindow, ipcMain } = require('electron');
const {path} = require('path')

function createWindow () {
    const win = new BrowserWindow({
        width: 800,
        height: 600,
        webPreferences: {
            preload: path.join(__dirname, 'preload.js')
        }
    });
   
   win.webContents.openDevTools();
   win.loadFile(path.join(__dirname, '../src/index.html'));
    // Or if you use a dev server:
    win.loadURL('http://localhost:3000');
}

app.whenReady().then(() => {
    createWindow();
    
    app.on('activate', () => {
        if (BrowserWindow.getAllWindows().length === 0) createWindow();
    });
});

app.on('window-all-closed', () => {
    if (process.platform !== 'darwin') app.quit();
});

ipcMain.on('toMain', (event, data) => {
  console.log('Received data from renderer:', data);
});
