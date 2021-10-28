
pip3 install -r requirements.txt
export $(cat .env | xargs)
python3 -c 'from main import main; main("", "")'