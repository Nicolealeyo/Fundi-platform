# How to Install ngrok on Windows

## Method 1: Direct Download (Easiest)

1. **Download ngrok**:
   - Go to: https://ngrok.com/download
   - Click "Download for Windows"
   - Save the ZIP file (e.g., `ngrok-v3-stable-windows-amd64.zip`)

2. **Extract the ZIP**:
   - Right-click the ZIP file → "Extract All"
   - Extract to a folder like `C:\ngrok\` or `C:\Users\LENOVO\ngrok\`

3. **EASIEST METHOD - Copy to System32 (No PATH setup needed!)**:
   
   **Step-by-step:**
   - Open File Explorer
   - Navigate to where you extracted ngrok (you should see `ngrok.exe`)
   - Right-click on `ngrok.exe` → Select "Copy"
   - Press `Win + R` (Windows key + R)
   - Type: `C:\Windows\System32` and press Enter
   - Right-click in the folder → Select "Paste"
   - If Windows asks for admin permission, click "Continue" or "Yes"
   - **DONE!** Now you can use `ngrok` from anywhere
   
   **Test it:**
   - Open a NEW CMD window (important: must be new!)
   - Type: `ngrok version`
   - If it shows a version number, you're all set!

4. **Alternative Method - Add Custom Folder to PATH**:
   
   If you prefer to keep ngrok in a custom folder:
   
   **Step 1: Create folder and move ngrok**
   - Create folder: `C:\ngrok\`
   - Copy `ngrok.exe` into `C:\ngrok\`
   
   **Step 2: Add to PATH**
   - Press `Win + X` (or right-click Start button)
   - Click "System"
   - Click "Advanced system settings" (on the right)
   - Click "Environment Variables" button (at bottom)
   - Under "System variables" (bottom section), find "Path"
   - Click "Path" → Click "Edit"
   - Click "New" button
   - Type: `C:\ngrok`
   - Click "OK" on all windows
   - **Close and reopen your CMD/PowerShell** (important!)
   
   **Test it:**
   - Open a NEW terminal window
   - Type: `ngrok version`
   - Should work now!

5. **Verify installation**:
   ```cmd
   ngrok version
   ```

## Method 2: Using Chocolatey (If you have it)

```cmd
choco install ngrok
```

## Method 3: Using Scoop (If you have it)

```cmd
scoop install ngrok
```

## After Installation

1. **Configure your authtoken**:
   ```cmd
   ngrok config add-authtoken 36K1KGsmdbEEEVVfJpOqT0nl9ZI_ouBpvBPPWB7WK6ragohc
   ```

2. **Reserve a free static domain** (optional but recommended):
   - Go to: https://dashboard.ngrok.com/cloud-edge/domains
   - Reserve a domain (e.g., `fundi-platform.ngrok-free.app`)

3. **Run ngrok**:
   ```cmd
   # If you have a static domain:
   ngrok http 8000 --domain=your-domain.ngrok-free.app
   
   # Or without static domain (URL changes each time):
   ngrok http 8000
   ```

4. **Update your .env file** with the ngrok URL:
   ```env
   MPESA_CALLBACK_URL=https://your-domain.ngrok-free.app/mpesa/callback/
   ```

## Troubleshooting

- **"ngrok is not recognized"**: 
  - Make sure you restarted your terminal after adding to PATH
  - Or use full path: `C:\ngrok\ngrok.exe http 8000`

- **"Permission denied"**: 
  - Run CMD as Administrator

- **Can't find ngrok.exe**: 
  - Check the extracted folder
  - Make sure you extracted the .exe file, not just the ZIP

