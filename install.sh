#!/bin/bash

# Kai Installation Script - Complete Setup
# This script installs all system and Python dependencies

set -e

echo "╔════════════════════════════════════════════════════════════╗"
echo "║  Kai - Open-source AI Assistant for Linux                 ║"
echo "║  Complete Installation with Voice Support                  ║"
echo "╚════════════════════════════════════════════════════════════╝"
echo ""

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

# Check if running on Linux
if [[ "$OSTYPE" != "linux-gnu"* ]]; then
    echo -e "${RED}Error: This script is designed for Linux systems${NC}"
    exit 1
fi

echo -e "${CYAN}Step 1: Checking Python version...${NC}"
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}Error: Python 3 is not installed${NC}"
    echo "Install with: sudo apt-get install python3 python3-venv python3-pip"
    exit 1
fi

PYTHON_VERSION=$(python3 -c 'import sys; print(".".join(map(str, sys.version_info[:2])))')
REQUIRED_VERSION="3.11"

if [ "$(printf '%s\n' "$REQUIRED_VERSION" "$PYTHON_VERSION" | sort -V | head -n1)" != "$REQUIRED_VERSION" ]; then
    echo -e "${RED}Error: Python $REQUIRED_VERSION or higher is required (found $PYTHON_VERSION)${NC}"
    exit 1
fi

echo -e "${GREEN}✓ Python $PYTHON_VERSION detected${NC}"
echo ""

# Install system dependencies
echo -e "${CYAN}Step 2: Installing system dependencies...${NC}"
echo "This requires sudo access"

# Check if apt is available
if command -v apt-get &> /dev/null; then
    echo "Installing audio dependencies..."
    sudo apt-get update -qq
    sudo apt-get install -y \
        portaudio19-dev \
        python3-pyaudio \
        mpg123 \
        sox \
        libsox-fmt-mp3 \
        alsa-utils \
        || echo -e "${YELLOW}Warning: Some packages may have failed to install${NC}"
    
    echo -e "${GREEN}✓ System dependencies installed${NC}"
else
    echo -e "${YELLOW}Warning: apt-get not found. Please install manually:${NC}"
    echo "  - portaudio19-dev"
    echo "  - mpg123"
    echo "  - alsa-utils"
fi
echo ""

# Install Ollama
echo -e "${CYAN}Step 3: Checking Ollama...${NC}"
if ! command -v ollama &> /dev/null; then
    echo "Ollama not found. Installing..."
    curl -fsSL https://ollama.com/install.sh | sh
    echo -e "${GREEN}✓ Ollama installed${NC}"
else
    echo -e "${GREEN}✓ Ollama already installed${NC}"
fi

# Start Ollama service
if systemctl is-active --quiet ollama; then
    echo -e "${GREEN}✓ Ollama service is running${NC}"
else
    echo "Starting Ollama service..."
    sudo systemctl start ollama || echo -e "${YELLOW}Warning: Could not start Ollama service${NC}"
fi
echo ""

# Download LLM model
echo -e "${CYAN}Step 4: Checking LLM model...${NC}"
if ollama list | grep -q "llama3.2:3b"; then
    echo -e "${GREEN}✓ Llama 3.2 3B model already downloaded${NC}"
else
    echo "Downloading Llama 3.2 3B model (2GB)..."
    echo "This may take a few minutes..."
    ollama pull llama3.2:3b
    echo -e "${GREEN}✓ Model downloaded${NC}"
fi
echo ""

# Create virtual environment
echo -e "${CYAN}Step 5: Setting up Python environment...${NC}"
if [ -d "venv" ]; then
    echo "Virtual environment already exists"
else
    echo "Creating virtual environment..."
    python3 -m venv venv
fi

source venv/bin/activate
echo -e "${GREEN}✓ Virtual environment activated${NC}"
echo ""

# Upgrade pip
echo -e "${CYAN}Step 6: Upgrading pip...${NC}"
pip install --upgrade pip -q
echo -e "${GREEN}✓ pip upgraded${NC}"
echo ""

# Install Python dependencies
echo -e "${CYAN}Step 7: Installing Python dependencies...${NC}"
echo "This may take a few minutes..."
pip install -r requirements.txt -q
echo -e "${GREEN}✓ Python dependencies installed${NC}"
echo ""

# Install Kai in development mode
echo -e "${CYAN}Step 8: Installing Kai...${NC}"
pip install -e . -q
echo -e "${GREEN}✓ Kai installed${NC}"
echo ""

# Create config directory
echo -e "${CYAN}Step 9: Setting up configuration...${NC}"
mkdir -p ~/.config/kai
echo -e "${GREEN}✓ Config directory created${NC}"
echo ""

# Test installation
echo -e "${CYAN}Step 10: Testing installation...${NC}"
if python -c "import kai; from kai.audio.stt import SpeechRecognizer; from kai.audio.tts_gtts import GoogleTTS" 2>/dev/null; then
    echo -e "${GREEN}✓ All modules imported successfully${NC}"
else
    echo -e "${YELLOW}Warning: Some modules may not have imported correctly${NC}"
fi
echo ""

echo "╔════════════════════════════════════════════════════════════╗"
echo "║              Installation Complete! 🎉                     ║"
echo "╚════════════════════════════════════════════════════════════╝"
echo ""
echo -e "${GREEN}Kai is ready to use!${NC}"
echo ""
echo -e "${CYAN}Quick Start:${NC}"
echo "  1. Activate environment:  ${YELLOW}source venv/bin/activate${NC}"
echo "  2. Test voice:            ${YELLOW}python tests/test_gtts.py${NC}"
echo "  3. Voice demo:            ${YELLOW}python tests/voice_demo.py${NC}"
echo "  4. Full voice mode:       ${YELLOW}python -m kai.cli voice${NC}"
echo "  5. Text mode:             ${YELLOW}python -m kai.cli start${NC}"
echo ""
echo -e "${CYAN}Documentation:${NC}"
echo "  - README.md              - Main documentation"
echo "  - QUICK_REFERENCE.md     - Quick reference card"
echo "  - DEVELOPMENT.md         - Development guide"
echo "  - CHANGELOG.md           - Version history"
echo "  - README-DEB.md          - Debian package info"
echo ""
echo -e "${CYAN}What's Installed:${NC}"
echo "  ✓ Ollama (LLM runtime)"
echo "  ✓ Llama 3.2 3B model"
echo "  ✓ Audio dependencies (portaudio, mpg123)"
echo "  ✓ Python packages (speech recognition, TTS)"
echo "  ✓ Kai assistant"
echo ""
echo -e "${GREEN}Enjoy your AI assistant!${NC} 🚀"
