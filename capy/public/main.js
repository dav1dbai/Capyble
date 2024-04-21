const { app, BrowserWindow, ipcMain, screen } = require('electron');
const path = require('path');

let win; // Ensure this is defined outside so it can be accessed globally within the module.
let isFullyVisible = true;  

function createWindow() {
    win = new BrowserWindow({
        width: 300,
        height: 320,
        frame: false,
        backgroundColor: "#F8D6AE",
        resizable: false,
        webPreferences: {
            preload: path.join(__dirname, 'preload.js')
        },
        x: screen.getPrimaryDisplay().bounds.width - 50, // Initially slightly off-screen.
        y: parseInt(screen.getPrimaryDisplay().bounds.height/2),
        icon: path.join(__dirname,'capylogo.icns')
    });

    win.webContents.openDevTools();
    //win.loadFile(path.join(__dirname, '../src/index.html'));
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

ipcMain.on('toggleWindow', (event, command) => {
    if (!win) return;

    const screenWidth = screen.getPrimaryDisplay().bounds.width;
    const windowHeight = screen.getPrimaryDisplay().bounds.height;  // Define window height for easy reference

    if (command === 'open') {
        // Make the window fully visible
        win.setBounds({ x: screenWidth - 300, y: parseInt(windowHeight / 2), width: 300, height: 300 });
        win.show(); // Ensure the window is shown in case it was hidden
    } else if (command === 'close') {
        // Hide a part of the window, making only an eighth visible
        win.setBounds({ x: screenWidth - 50, y: parseInt(windowHeight / 2), width: 50, height: 300 });
        // Optionally, you could hide the window entirely instead:
        // win.hide();
    }
});

