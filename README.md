# Webpage Wallpaper

Make your wallpaper background a dynamically updating webpage!

This program saves screenshots of a webpage on a schedule. A user's operating system can then be configured to use the screenshots as an updating wallpaper. Meant for use with dashboards or other similar websites.

---

## Setup

### Single User Setup

#### Installation

1. Place the project folder wherever is preferred. It is recommended to use location:
   
   ```bash
   C:\Users\$USERNAME\AppData\Roaming
   ```

2. Download and de-compress the latest version of [mozilla/geckodriver] into the project folder.

3. Edit **config.toml** and set the following:
   
   - **gecko_relative_path**: path of the gecko driver relative to project folder.
   
   - **output_folder**: absolute path of output folder (user choice). If blank, output folder will generate in root.

4. Rename the project folder to whatever is preferred.

5. Create a shortcut to **UPDATER.exe**.

6. Move the shortcut to the folder:
   
   ```bash
   C:\Users\$USERNAME\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Startup
   ```

#### Changing OS Settings

##### Microsoft Windows

1. Go to Settings > Personalization > Background.

2. Set the following settings:
   
   - Background: **Slideshow**.
   
   - Choose albums for your slideshow:
     
     1. Select Browse.
     
     2. Go to the project folder.
     
     3. Select the folder of desired area (once generated).
   
   - Change picture every: **1 minute**.
   
   - Choose a fit: **stretch**.

3. Wait for wallpaper change to confirm function.

##### Other Operating Systems

Set the wallpaper to dynamically update based on either the contained images or the folder containing images.

---

### Multi-User/Server Installation

#### Pre-requesites

- Server compute resource allocation on which to run this program.

- Server network access to the folder locations.

- A publicly accessible network location to which only the server has write access.

#### Installation (Executable)

Steps here are similar to the Single User Setup Installation, however automatic startup configuration will depend on environment.

#### Installation (Project Code)

1. Ensure Python 3.11+ is installed.

2. Install the required external modules using the following command:
   
   ```bash
   pip install schedule selenium
   ```

3. Download and de-compress [mozilla/geckodriver] in the project folder.

4. Place the project folder at the desired location and edit **config.toml** to match.

5. Configure environment to auto-start **UPDATER.py** during initialization.

---

## Configuration Changes

Configuration file changes may be made during execution (without restarting). Keep backups until certain that changes have not adversely affected execution.

### Modify/Add Webpages

1. Edit **config.toml**.

2. Modify according to visible format.

### Updating GeckoDriver

1. Download GeckoDriver from [mozilla/geckodriver].

2. De-compress and place the folder into the project root folder.

3. Open **config.toml**.

4. Edit the variable **gecko_relative_path** so that it matches the path to the new GeckoDriver executable.

### Logging

The logger uses the Python standard logging module and is configured to output the following information:

```textile
date_time - level_name - name - process - module - file_name - function_name - line_number - message
```

The logger may be configured by editing **config_log.toml**.

---

## Notes

### Resource Useage

Program uses 0% CPU and 8-30 MB memory.

### How it Works

An automation testing webdriver is used to get screenshots of each desired webpage on a schedule.

### Update Delay

Wallpaper updates may be delayed several minutes after the update of the webpage due to a combination of the following:

- Program gets webpage screenshot 1-2 minutes after update.

- Wallpaper slideshow changes once per minute.

### Incomplete Screenshots

The tool used to get screenshots simulates a browser with a finite viewport. Because of this, edges of large webpages that extend past the boundaries of the viewport will be cut off. While this is annoying, I am not aware of an accessible tool that can take full webpage screenshots currently.

### Multiple Monitors

On Windows operating systems, the slideshow updates one monitor at a time. This may lead to later updates proportional to the number of monitors used.

---

[mozilla/geckodriver]: https://github.com/mozilla/geckodriver/releases 'Proxy for using W3C WebDriver compatible clients to interact with Gecko-based browsers.'
