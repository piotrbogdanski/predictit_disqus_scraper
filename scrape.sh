url="https://www.predictit.org/markets/detail/3698/Who-will-win-the-2020-US-presidential-election"
Path="/home/piotr/projects/lukasz/us_election_predictit/out"

# Create a directory if exists
if [ -d $Path ]
then
    echo "Directory $Path already exists. Removing all files."
    rm $Path/*
else
    mkdir $Path
    echo "Created directory $Path."
fi

# Run market data scrape
echo "Obtaining market data from: " $url
python3 get_predictit_history.py $url $Path


# Get thread ID for Disqus data scrape
echo "Retrieving Disqus thread url from: " $url
python3 get_disqus_thread.py $url
thread_url="$(cat url.txt)"
disqus_key="$(cat disqus_key.txt)"

# Scrape Disqus comments
echo "Scraping comments..."
python3 get_disqus_posts.py "$thread_url" "$disqus_key" $Path -sleep-time 3
