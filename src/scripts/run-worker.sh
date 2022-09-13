## for GPUs! 
#xvfb-run --server-args="-screen 0 100x150x16" -a -p XSMP /spark-worker
echo Viewable environment launched in tmux session
echo Attach with: tmux attach -t tmux-session
echo Detach with: Ctrl-b, d
tmux new-session -d -s tmux-session xvfb-run --server-args="-screen 0 100x150x16" -a -p XSMP bash /spark-worker "$@"
sleep 10
fluxbox -display :99 &
sleep 10
x11vnc -display :99 -bg -nopw -xkb -viewonly
echo "viewer started, sleeping..."
python3 -u /work/debug.py --silent
