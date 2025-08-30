#!/bin/bash

echo "RAG Chatbot System Launcher"
echo "=========================="
echo

while true; do
    echo "1. Start Web Interface for Document Upload"
    echo "2. Start Chatbot"
    echo "3. Process Documents (Build Index)"
    echo "4. Exit"
    echo
    
    read -p "Enter your choice (1-4): " choice
    
    case $choice in
        1)
            echo
            echo "Starting Web Interface on http://localhost:5000"
            echo "Press Ctrl+C to stop the server"
            echo
            python3 app.py
            ;;
        2)
            echo
            echo "Starting RAG Chatbot..."
            echo
            python3 chatbot.py
            ;;
        3)
            echo
            echo "Processing documents and building index..."
            echo
            python3 process_pdf.py
            echo
            echo "Done! Press Enter to continue..."
            read
            clear
            ;;
        4)
            echo
            echo "Goodbye!"
            exit 0
            ;;
        *)
            echo "Invalid choice. Please try again."
            ;;
    esac
    
    echo
done