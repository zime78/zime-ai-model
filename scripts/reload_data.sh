#!/bin/bash
echo "Reloading data on running MyBrainAI instance..."
curl -X POST http://localhost:8000/system/reload
echo ""
echo "Done."
