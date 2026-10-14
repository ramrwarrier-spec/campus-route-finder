#!/bin/bash
clear
cd "$(dirname "$0")" || cd /Users/ram/.gemini/antigravity/scratch/campus-route-finder
python3 campus_route_finder.py
echo ""
read -p "Press Enter to close this window..."
