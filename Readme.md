# Smartbox PrusaSlicer-settings-prusa-fff

This is a fork of the [Prusaslicer-settings-prusa-fff repo](https://github.com/prusa3d/PrusaSlicer-settings-prusa-fff), updated to include profiles for filaments used by Smartbox Assistive Technology.

[![Fetch Latest PrusaSlicer Config and Release](https://github.com/Smartbox-Assistive-Technology/PrusaSlicer-settings-prusa-fff/actions/workflows/release.yml/badge.svg)](https://github.com/Smartbox-Assistive-Technology/PrusaSlicer-settings-prusa-fff/actions/workflows/release.yml)


## How it works

The script add all the `*.add.in* and `*.rm.ini` files in the [Smartbox](Smartbox) folder to the latest version of the prusa3d/PrusaSlicer-settings-prusa-fff repo, and then creates a new release with the updated files.

Current filaments:

- Overture TPU High-Speed
- Polymaker PolyDissolve S1
- Eono PVB

Past filaments:

- Elegoo Rapid PLA+
- Overture PETG
- Overture PLA
- Sunlu PLA+ 2.0

## Installing profiles

Automatic profile installation:

On Windows, open Powershell and copy-paste the following, then press enter:

```ps
$d="$env:APPDATA\PrusaSlicer\vendor";$p="$d\PrusaResearch.ini";if(-not(Test-Path $d)){Write-Error "Vendor directory missing: $d";exit 1};if(Test-Path $p){Write-Host "Backing up existing config...";Move-Item $p "$p.bak" -Force};Write-Host "Downloading new config...";Invoke-WebRequest "https://github.com/Smartbox-Assistive-Technology/PrusaSlicer-settings-prusa-fff/releases/download/latest/PrusaResearch.ini" -OutFile $p;Write-Host "Operation completed successfully"
```

On Mac, open Terminal and copy-paste the following, then press enter:

```bash
#!/bin/bash

# Define paths
VENDOR_DIR="$HOME/Library/Application Support/PrusaSlicer/vendor"
CONFIG_FILE="$VENDOR_DIR/PrusaResearch.ini"

# Check if vendor directory exists
if [ ! -d "$VENDOR_DIR" ]; then
    echo "Error: Vendor directory missing: $VENDOR_DIR"
    exit 1
fi

# Backup existing config if it exists
if [ -f "$CONFIG_FILE" ]; then
    echo "Backing up existing config..."
    mv -f "$CONFIG_FILE" "$CONFIG_FILE.bak"
fi

# Download new config
echo "Downloading new config..."
curl -L "https://github.com/Smartbox-Assistive-Technology/PrusaSlicer-settings-prusa-fff/releases/download/latest/PrusaResearch.ini" -o "$CONFIG_FILE"

# Check if download was successful
if [ $? -eq 0 ]; then
    echo "Operation completed successfully"
else
    echo "Error: Download failed"
    # Restore backup if it exists
    if [ -f "$CONFIG_FILE.bak" ]; then
        mv -f "$CONFIG_FILE.bak" "$CONFIG_FILE"
        echo "Previous configuration restored"
    fi
    exit 1
fi
```


Manual profile installation:

- Open PrusaSlicer. In the top menu, click on "Help" -> "Show Configuration Folder". This will open a folder in your file explorer.
- Close PruasSlicer.
- Inside the `vendor` folder, you will find a file called `PrusaResearch.ini`. Rename it to `PrusaResearch.ini.bak`.
- Download the profiles from [here](https://github.com/Smartbox-Assistive-Technology/PrusaSlicer-settings-prusa-fff/releases/latest) and save the new `PrusaResearch.ini` file in the `vendor` folder, making sure it is not renamed.
- Reopen PrusaSlicer. Run the configuration assistant, and select the profiles mentioned in the table above.

