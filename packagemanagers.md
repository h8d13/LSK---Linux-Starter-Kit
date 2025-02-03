# Package Managers for Linux
=====================================

Package managers are essential tools for Linux users, allowing them to easily install, update, and manage software packages on their systems. In this document, we will explore four of the most common package managers for Linux: Flatpak, Snapd, Pacman, and Apt. 

**Do be careful if working from barebones that you will need dependencies for each of them, and they can conflict if you use several of them.**


## Flatpak
------------

Flatpak is a package manager that allows users to install and run applications in a sandboxed environment. This means that applications are isolated from the rest of the system, improving security and reducing the risk of conflicts between packages.

### Basic Usage
Add a hub if not done already.
`flatpak remote-add --if-not-exists flathub https://flathub.org/repo/flathub.flatpakrepo`

* Install a package: `flatpak install <package_name>`
* List installed packages: `flatpak list`
* Update packages: `flatpak update`
* Remove a package: `flatpak uninstall <package_name>`

### Example

* Install the GIMP image editor: `flatpak install org.gimp.GIMP`
* List all installed packages: `flatpak list`

## Snapd & Snap
------------

Snapd is a package manager developed by Canonical, the company behind Ubuntu. It allows users to install and run applications in a sandboxed environment, similar to Flatpak.
Useful is the refresh button on top left.
Snap is the CLI tool. 

### Basic Usage

* Install a package: `snap install <package_name>`
* List installed packages: `snap list`
* Update packages: `snap refresh`
* Remove a package: `snap remove <package_name>`

### Example

* Install the VLC media player: `snap install vlc`
* List all installed packages: `snap list`

## Pacman
------------

Pacman is the package manager for Arch Linux and its derivatives. It is known for its simplicity and flexibility.

### Basic Usage

* Install a package: `pacman -S <package_name>`
* List installed packages: `pacman -Q`
* Update packages: `pacman -Syu`
* Remove a package: `pacman -R <package_name>`

### Example

* Install the Firefox web browser: `pacman -S firefox`
* List all installed packages: `pacman -Q`

## Apt
------------

Apt is the package manager for Debian-based Linux distributions, such as Ubuntu and Linux Mint.

### Basic Usage

* Install a package: `apt install <package_name>`
* List installed packages: `apt list --installed`
* Update packages: `apt update && apt upgrade`
* Remove a package: `apt remove <package_name>`

### Example

* Install the Chromium web browser: `apt install chromium-browser`
* List all installed packages: `apt list --installed`

## Comparison
--------------

| Package Manager | Distribution | Sandbox Support |
| --- | --- | --- |
| Flatpak | Multi-distribution | Yes |
| Snapd | Ubuntu-based | Yes |
| Pacman | Arch Linux-based | No |
| Apt | Debian-based | No |

## Dpkg

For Debian based systems, you can also work directly with dpkg and .deb files. 

* Install a package: `dpkg -i <package_name>.deb`
* Remove a package: `dpkg -r <package_name>`
* Search for packages: `dpkg -S <keyword>`
* List installed packages: `dpkg -l`
* List package details: `dpkg -s <package_name>`
* Install a package with dependencies: `dpkg -i --force-depends <package_name>.deb`
* Remove a package with dependencies: `dpkg -r --force-depends <package_name>`

## AppImage

Open a terminal in the folder you downloaded the app.

`chmod +x Cemu-2.5-x86_64.AppImage`

Boom you can now open it. Again don't like the terminal? 
You can right click > Permissions > Allow executing file as program. Which will do the same as above. 

## GUI Package Managers

If you don't like the terminal: There are solutions for GUIs. 

- Synaptic: A graphical package manager for Debian-based systems 
- Aptitude: Another GUI for apt
- Tasksel: Specific tasks for deb based systems
- Ubuntu Software Center: A graphical package manager for Ubuntu 
- Linux Mint Software Manager: A graphical package manager for Linux Mint 



## Working from source code

You will need make or whatver the project requires to build

Extract the .tar.gz (or whatever compressed format) 
Then 

cd application
./configure (whatever is the config/setup/launch script)
make
make install

