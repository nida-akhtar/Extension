document.getElementById('summarize-btn').addEventListener('click', () => {
    chrome.tabs.query({ active: true, lastFocusedWindow: true }, (tabs) => {
      let url = tabs[0].url;
  
      fetch('http://127.0.0.1:8000/summarize/?url=' + encodeURIComponent(url))
        .then(response => response.json())
        .then(data => {
          if (data.summary) {
            document.getElementById('summary').innerText = data.summary;
          } else {
            document.getElementById('summary').innerText = 'Error: ' + data.error;
          }
        })
        .catch(error => {
          document.getElementById('summary').innerText = 'Failed to fetch summary.';
          console.error('Error:', error);
        });
    });
  });
  