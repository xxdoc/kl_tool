nohup node app.js > ./logs/'node-dms-'`date +%y-%m-%d_%H%M%S`'.out' 2>&1 &
nohup python mrq-dashboard.py > ./logs/'mrq-dashboard-'`date +%y-%m-%d_%H%M%S`'.out' 2>&1 &
nohup python mrq-worker.py > ./logs/'mrq-worker-base-'`date +%y-%m-%d_%H%M%S`'.out' 2>&1 &
