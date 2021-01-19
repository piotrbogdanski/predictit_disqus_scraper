url="https://www.predictit.org/markets/detail/7001/Which-party-will-win-the-2021-Virginia-gubernatorial-election"
echo "Opening" $url
python3 get_disqus_thread.py $url
thread_url="$(cat url.txt)"
disqus_key="$(cat disqus_key.txt)"

echo "Scraping comments..."
python3 get_disqus_posts.py "$thread_url" "$disqus_key" "out"
