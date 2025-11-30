# Building Kai Assistant .deb Package

## Prerequisites

Install build tools:
```bash
sudo apt-get install debhelper dh-python python3-all python3-setuptools
```

## Build Package

```bash
./build-deb.sh
```

This creates: `../kai-assistant_1.0.0-1_all.deb`

## Install

```bash
sudo dpkg -i ../kai-assistant_0.9.0-1_all.deb
sudo apt-get install -f  # Fix any missing dependencies
```

## Usage

After installation:
```bash
kai settings      # Open settings GUI
kai voice         # Start voice mode
kai start         # Interactive text mode
```

## Uninstall

```bash
sudo apt-get remove kai-assistant
```
