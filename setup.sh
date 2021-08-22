mkdir -p ~/.streamlit/
echo "\
[server]\n\
headless = true\n\
port = $PORT\n\
enableCORS = false\n\
\n\
[theme]\n\
primaryColor=\"#F63366\"\n\
backgroundColor=\"#FFFFFF\"\n\
secondaryBackgroundColor=\"#F0F2F6\"\n\
textColor=\"#262730\"\n\
font=\"sans serif\"\n\
\n\
" > ~/.streamlit/config.toml
